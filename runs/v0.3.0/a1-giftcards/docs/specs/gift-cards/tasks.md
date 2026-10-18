# Implementation Plan: gift-cards

## Overview

Build the ports first (store, ledger, payments, Cart flag), then the three services (purchase, redeem, void), then the API routes. Property tests come after the code they cover. Test fakes come in wave 1; service Verify commands import them, so services wait for them. Checkpoint after each code layer and at the end.

## Tasks

- [x] 1. Ports and models
  - [x] 1.1 Create GiftCard and GiftCardStore
    - Files: `shop/giftcards.py`
    - Kind: code
    - Size: M
    - Do: Add `MAX_BALANCE_CENTS = 50_000`, `CODE_LEN = 16`, `GiftCard` dataclass (`code`, `balance_cents`, `status="active"`), and `GiftCardStore` with `new_code()` (16 chars A-Z0-9, unique, `secrets`), `add()` (ValueError when balance > MAX_BALANCE_CENTS or < 0), `get()`, `lock(code)` (one `threading.Lock` per code), `idempotent: dict[str, dict]`.
    - Do: No expiry logic and no time-based changes.
    - Verify: `uv run --no-project python -c "from shop.giftcards import GiftCardStore, GiftCard; s=GiftCardStore(); c=s.new_code(); assert len(c)==16; s.add(GiftCard(c, 50000)); assert s.get(c).status=='active'; assert s.lock(c) is s.lock(c)"`
    - _Requirements: 2.3, 2.7, 4.1_
  - [x] 1.2 Create Ledger
    - Files: `shop/ledger.py`
    - Kind: code
    - Size: S
    - Do: Add `LedgerUnavailable(Exception)`, frozen `Entry` (`code`, `field`, `old`, `new`, `actor_id`, `at` UTC datetime), and `Ledger` with `entries: list[Entry]`, `manual_refunds: list[dict]`, `append(entry)`.
    - Verify: `uv run --no-project python -c "from shop.ledger import Ledger, Entry; from datetime import datetime, UTC; l=Ledger(); l.append(Entry('A'*16,'balance',None,1000,'u1',datetime.now(UTC))); assert len(l.entries)==1 and l.manual_refunds==[]"`
    - _Requirements: 5.1, 5.4_
  - [x] 1.3 Create PaymentProvider port
    - Files: `shop/payments.py`
    - Kind: code
    - Size: S
    - Do: Add frozen `ChargeResult(status: Literal["ok","declined","timeout"], charge_id: str | None = None)` and `PaymentProvider` Protocol with `charge(amount_cents, ref, timeout_s)`, `refund(charge_id)`, `cancel(ref)`.
    - Verify: `uv run --no-project python -c "from shop.payments import ChargeResult, PaymentProvider; assert ChargeResult('timeout').charge_id is None"`
    - _Requirements: 1.3, 1.6_
  - [x] 1.4 Add open flag to Cart
    - Files: `shop/cart.py`
    - Kind: code
    - Size: S
    - Do: In `Cart.__init__` set `self.open = True`. Change nothing else.
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_cart.py` passes; `Cart(Inventory({})).open is True`.
    - _Requirements: 2.8_
  - [x] 1.5 Create test fakes
    - Files: `tests/fakes.py`
    - Kind: code
    - Size: S
    - Do: Add `FakePaymentProvider(result="ok", refund_fails=False)` that records `charges`, `refunds`, `cancels` lists and returns `ChargeResult` per `result` (charge_id `ch_<n>` on ok). Add `FailingLedger(Ledger)` whose `append` raises `LedgerUnavailable`. Add `make_ctx(**over)` that builds `{"carts", "inventory", "giftcards", "ledger", "payments", "staff_ids"}`.
    - Verify: `uv run --no-project python -c "import sys; sys.path.insert(0,'tests'); from fakes import make_ctx, FakePaymentProvider; c=make_ctx(); r=c['payments'].charge(1000,'r',10); assert r.status=='ok' and c['payments'].charges"`
    - _Requirements: 1.3, 5.2_

- [x] 2. Checkpoint — run `uv run --no-project --with pytest --with hypothesis python -m pytest -q`; typecheck: none

- [x] 3. Services
  - [x] 3.1 Implement purchase.buy
    - Files: `shop/purchase.py`
    - Kind: code
    - Size: L
    - Do: `buy(body, ctx) -> {"status","body"}` per design `purchase` call tree: idempotency replay, 422 `invalid_request` for value not whole dollars in 10–500 (no charge), charge `value*100` with `timeout_s=10`, `cancel(ref)` on timeout, 402 `payment_failed` on declined/timeout with no card.
    - Do: Ledger create entry (`old=None`) before `store.add`; on `LedgerUnavailable` refund the charge, on refund error append `{charge_id, amount_cents, at}` to `ledger.manual_refunds`, return 503 `ledger_unavailable`. Success → 201 `{"code"}`, store response under the key.
    - Verify: `uv run --no-project python -c "import sys; sys.path.insert(0,'tests'); from fakes import make_ctx; from shop.purchase import buy; c=make_ctx(); r=buy({'value_dollars':25,'actor_id':'u1'}, c); assert r['status']==201 and len(r['body']['code'])==16"`
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 1.10, 5.1, 5.2, 5.3, 5.4_
  - [x] 3.2 Implement redeem.apply
    - Files: `shop/redeem.py`
    - Kind: code
    - Size: L
    - Do: `apply(body, ctx)` per design `redeem` call tree: 422 `invalid_request` when code length ≠ 16 or Cart missing or not open; 404 `unknown_card`; under `store.lock(code)`: 409 `card_void`, compute `new_b, due`, ledger balance entry (503 `ledger_unavailable` on failure, no change), commit.
    - Do: Success → 200 `{"balance_cents", "amount_due_cents"}`.
    - Verify: `uv run --no-project python -c "import sys; sys.path.insert(0,'tests'); from fakes import make_ctx; from shop.redeem import apply; from shop.giftcards import GiftCard; from shop.cart import Cart; c=make_ctx(); c['giftcards'].add(GiftCard('A'*16,1000)); c['carts']['1']=Cart(c['inventory']); r=apply({'code':'A'*16,'cart_id':'1','actor_id':'u'},c); assert r['status']==200"`
    - _Requirements: 2.1, 2.2, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.2, 5.1, 5.2_
  - [x] 3.3 Implement void.void
    - Files: `shop/void.py`
    - Kind: code
    - Size: M
    - Do: `void(code, body, ctx)` per design `void` call tree: 403 `forbidden` (no change) when `actor_id` missing or not in `ctx["staff_ids"]`; 404 `unknown_card`; under lock: 409 `card_void` if already void; ledger status entry (503 on failure, no change); set `void`; 200 `{"code","status":"void"}`.
    - Verify: `uv run --no-project python -c "import sys; sys.path.insert(0,'tests'); from fakes import make_ctx; from shop.void import void; from shop.giftcards import GiftCard; c=make_ctx(staff_ids={'s1'}); c['giftcards'].add(GiftCard('A'*16,1000)); assert void('A'*16,{'actor_id':'x'},c)['status']==403; assert void('A'*16,{'actor_id':'s1'},c)['status']==200"`
    - _Requirements: 3.1, 3.3, 3.4, 5.1, 5.2_

- [x] 4. Checkpoint — run `uv run --no-project --with pytest --with hypothesis python -m pytest -q`; typecheck: none

- [x] 5. API routes and service tests
  - [x] 5.1 Route gift-card requests in handle
    - Files: `shop/api.py`
    - Kind: code
    - Size: M
    - Do: Before the `/carts` routes add `POST /gift-cards` → `purchase.buy`, `POST /gift-cards/redeem` → `redeem.apply`, `POST /gift-cards/<code>/void` → `void.void`. Keep existing routes unchanged.
    - Verify: `uv run --no-project python -c "import sys; sys.path.insert(0,'tests'); from fakes import make_ctx; from shop.api import handle; c=make_ctx(); r=handle({'method':'POST','path':'/gift-cards','body':{'value_dollars':10,'actor_id':'u'}},c); assert r['status']==201"`
    - _Requirements: 1.2, 3.1_
  - [x]* 5.2 Property tests for purchase
    - Files: `tests/test_purchase.py`
    - Kind: test
    - Size: M
    - **Property 1: Valid purchase creates a matching card**
    - **Validates: Requirements 1.1, 1.2, 1.5**
    - **Property 2: Invalid purchase value is rejected without a charge**
    - **Validates: Requirements 1.7, 1.8**
    - **Property 3: Failed charge creates no card**
    - **Validates: Requirements 1.3, 1.4, 1.6**
    - **Property 4: Purchase is idempotent per key**
    - **Validates: Requirements 1.9, 1.10**
    - **Property 10: Ledger failure after charge refunds or queues**
    - **Validates: Requirements 5.3, 5.4**
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_purchase.py`
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 1.10, 5.3, 5.4_
  - [x]* 5.3 Property tests for redeem
    - Files: `tests/test_redeem.py`
    - Kind: test
    - Size: L
    - **Property 5: Redemption follows the balance model**
    - **Validates: Requirements 2.1, 2.3, 2.5, 2.6**
    - **Property 6: Concurrent operations never overspend**
    - **Validates: Requirements 2.7**
    - **Property 7: Redemption error precedence**
    - **Validates: Requirements 2.4, 2.8, 2.9, 3.2**
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_redeem.py`; also example tests: 200 redemptions 95th percentile < 2 s (2.2); an untouched card keeps its balance after other operations (4.1).
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.2, 4.1_
  - [x]* 5.4 Property tests for void
    - Files: `tests/test_void.py`
    - Kind: test
    - Size: M
    - **Property 8: Only staff can void**
    - **Validates: Requirements 3.1, 3.3, 3.4**
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_void.py`
    - _Requirements: 3.1, 3.3, 3.4_
  - [x]* 5.5 Property tests for ledger audit
    - Files: `tests/test_ledger_audit.py`
    - Kind: test
    - Size: M
    - **Property 9: Every change is audited, or nothing changes**
    - **Validates: Requirements 5.1, 5.2**
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_ledger_audit.py`
    - _Requirements: 5.1, 5.2_

- [x] 6. Checkpoint — run `uv run --no-project --with pytest --with hypothesis python -m pytest -q`; typecheck: none

- [x] 7. End-to-end
  - [x]* 7.1 API tests for gift-card routes
    - Files: `tests/test_api_giftcards.py`
    - Kind: test
    - Size: M
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_api_giftcards.py` — buy → redeem partial → redeem rest with amount due → staff void → redeem gives 409; existing `/carts` routes still work.
    - _Requirements: 1.2, 3.1_

- [x] 8. Checkpoint — run `uv run --no-project --with pytest --with hypothesis python -m pytest -q`; typecheck: none

## Notes

- `*` = optional, skip for faster MVP
- Test files import fakes with `sys.path` or `from fakes import ...`; pytest `rootdir` puts `tests/` on the path (rootdir conftest-free, `testpaths = ["tests"]`).
- Each test file carries `# Feature: gift-cards, Property N: <title>` per property; Hypothesis `max_examples >= 100`.
- Open Questions F11, F12, F22, F24–F26 are not built; design picks conservative defaults.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.2", "1.3", "1.4"] },
    { "id": 1, "tasks": ["1.5"] },
    { "id": 2, "tasks": ["3.1", "3.2", "3.3"] },
    { "id": 3, "tasks": ["5.1", "5.2", "5.3", "5.4", "5.5"] },
    { "id": 4, "tasks": ["7.1"] }
  ],
  "deps": {
    "1.5": ["1.2", "1.3"],
    "3.1": ["1.1", "1.2", "1.3", "1.5"],
    "3.2": ["1.1", "1.2", "1.4", "1.5"],
    "3.3": ["1.1", "1.2", "1.5"],
    "5.1": ["3.1", "3.2", "3.3"],
    "5.2": ["3.1", "1.5"],
    "5.3": ["3.2", "1.5"],
    "5.4": ["3.3", "1.5"],
    "5.5": ["3.1", "3.2", "3.3", "1.5"],
    "7.1": ["5.1", "1.5"]
  }
}
```

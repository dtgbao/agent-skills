# Implementation Plan: gift-cards

## Overview

Build bottom-up: payment and ledger modules first, then `GiftCardService` with its lock and ledger-first rule, then the `/gift-cards` routes in `shop/api.py`. Property tests follow the code they cover: service properties after the service, route properties after the routes. Hypothesis is pulled in by the test command (`uv run --with hypothesis`), so no setup leaf is needed.

## Tasks

- [x] 1. Core gift card modules
  - [x] 1.1 Add payment protocol and ledger
    - Files: `shop/payments.py`, `shop/ledger.py`
    - Kind: code
    - Size: S
    - Do: Create `shop/payments.py` with `PaymentDeclined`, `PaymentError`, and `PaymentProvider` Protocol (`charge(amount_cents, charge_ref)`, `refund(charge_ref)`) per design.md Payments. Create `shop/ledger.py` with frozen `LedgerEntry(code, field, old, new, actor_id, at)`, `LedgerUnavailable`, and `Ledger` (`entries` list, `fail` flag; `append` raises `LedgerUnavailable` when `fail` is true, else appends).
    - Verify: `python -c "from shop.payments import PaymentProvider, PaymentDeclined, PaymentError; from shop.ledger import Ledger, LedgerEntry, LedgerUnavailable"` exits 0; `Ledger(fail=True).append(...)` raises `LedgerUnavailable`.
    - _Requirements: 5.1, 5.2_
  - [x] 1.2 Implement GiftCardService
    - Files: `shop/gift_cards.py`
    - Kind: code
    - Size: L
    - Do: Create `GiftCard`, `GiftCardError(status, error)`, and `GiftCardService(payments, ledger, clock)` with `purchase`, `redeem`, `void`, `expire_unused` exactly per the design.md call tree. One `threading.Lock` around every read-modify-write. Ledger append before every state change. `EXPIRY = timedelta(days=365)`; expiry entries use actor id `system`. Codes: 16 chars `A–Z0–9` via `secrets`. Refund failures log `charge_ref` with `logging.getLogger("shop.gift_cards").error`.
    - Verify: Quick checks with fakes: purchase(25) → active card, 2500 cents, 16-char code; redeem 3000 on it → balance 0, amount due 500; void with role `shopper` → `GiftCardError(403, "forbidden")`; ledger `fail=True` on purchase → refund called, `GiftCardError(503, "ledger_unavailable")`.
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 2.1, 2.3, 2.4, 2.5, 2.6, 3.1, 3.2, 3.3, 3.4, 4.1, 4.2, 5.1, 5.2, 5.3, 5.4, 5.5_

- [x] 2. Checkpoint — run `uv run --no-project --with pytest --with hypothesis python -m pytest -q`; typecheck: none

- [x] 3. API routes
  - [x] 3.1 Add /gift-cards routes to handle
    - Files: `shop/api.py`
    - Kind: code
    - Size: M
    - Do: Add `POST /gift-cards`, `POST /gift-cards/<code>/redeem` (body `cart_id`, subtotal from `ctx["carts"]`), and `POST /gift-cards/<code>/void` before the `no route` fallback. Make the service with `ctx.setdefault("gift_cards", GiftCardService(ctx["payment_provider"], ctx["ledger"], ctx["clock"]))`. Pass `ctx.get("actor")`. Map `GiftCardError` to `{"status": e.status, "body": {"error": e.error}}`. Keep existing cart routes unchanged.
    - Verify: `handle({"method": "POST", "path": "/gift-cards", "body": {"value_dollars": 50}}, ctx)` with fakes → 201 and a 16-char `code`; unknown code redeem → 404 `unknown_card`; existing `tests/test_cart.py` still passes.
    - _Requirements: 1.2, 2.2, 2.4, 3.1, 3.3, 3.4_

- [x] 4. Checkpoint — run `uv run --no-project --with pytest --with hypothesis python -m pytest -q`; typecheck: none

- [x] 5. Property tests
  - [x]* 5.1 Service property tests
    - Files: `tests/test_gift_cards_props.py`
    - Kind: test
    - Size: M
    - Do: Hypothesis tests against `GiftCardService` with a fake provider, `Ledger`, and fixed clock. Tag comment `Feature: gift-cards, Property N: <title>` per property. `@settings(max_examples=100)` or more.
    - **Property 4: Redemption matches the balance model**
    - **Validates: Requirements 2.1, 2.5, 4.1**
    - **Property 5: Concurrent redemptions equal sequential ones**
    - **Validates: Requirements 2.6**
    - **Property 7: Ledger matches every change**
    - **Validates: Requirements 5.1, 5.2**
    - **Property 8: Ledger failure at creation refunds the charge**
    - **Validates: Requirements 5.3, 5.4, 5.5**
    - **Property 9: Expiry after 365 unused days**
    - **Validates: Requirements 4.2**
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_gift_cards_props.py`
    - _Requirements: 2.1, 2.5, 2.6, 4.1, 4.2, 5.1, 5.2, 5.3, 5.4, 5.5_
  - [x]* 5.2 API property tests
    - Files: `tests/test_gift_cards_api.py`
    - Kind: test
    - Size: M
    - Do: Hypothesis tests through `handle` with fakes in `ctx`. Tag comment per property. Add one example test that 100 redemptions finish in under 2 seconds for 2.2.
    - **Property 1: Purchase creates an active card with the paid balance**
    - **Validates: Requirements 1.1, 1.2, 2.3**
    - **Property 2: Invalid amounts never charge**
    - **Validates: Requirements 1.4**
    - **Property 3: Payment failures create no card**
    - **Validates: Requirements 1.3, 1.5, 1.6**
    - **Property 6: Void rules**
    - **Validates: Requirements 2.4, 3.1, 3.2, 3.3, 3.4**
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_gift_cards_api.py`
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4_

- [x] 6. Checkpoint — run `uv run --no-project --with pytest --with hypothesis python -m pytest -q`; typecheck: none

## Notes

- `*` = optional, skip for faster MVP
- Ledger append always comes before the state change (5.2). Do not reorder.
- Open Questions F9 and F17 are decided in design.md Key design decisions.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1"] },
    { "id": 1, "tasks": ["1.2"] },
    { "id": 2, "tasks": ["3.1", "5.1"] },
    { "id": 3, "tasks": ["5.2"] }
  ],
  "deps": {
    "1.2": ["1.1"],
    "3.1": ["1.2"],
    "5.1": ["1.2"],
    "5.2": ["3.1"]
  }
}
```

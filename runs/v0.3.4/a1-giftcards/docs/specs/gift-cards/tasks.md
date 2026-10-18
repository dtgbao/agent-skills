# Implementation Plan: gift-cards

## Overview

Build bottom-up: payment protocol and ledger, then `GiftCardService` (lock, check order, ledger first), then the `/gift-cards` routes. Property tests follow the code they cover: service properties after the service, route properties after the routes. The test command pulls in Hypothesis (`uv run --with hypothesis`), so there is no setup leaf.

## Tasks

- [x] 1. Core modules
  - [x] 1.1 Add payment protocol and ledger
    - Files: `shop/payments.py`, `shop/ledger.py`
    - Kind: code
    - Size: S
    - Do: Create `shop/payments.py` with `PaymentDeclined`, `PaymentError` and `PaymentProvider` Protocol (`charge(amount_cents) -> str`, `refund(charge_id) -> None`) per design.md Payments. Create `shop/ledger.py` with frozen `LedgerEntry(code, old, new, actor_id, at)`, `LedgerUnavailable`, and dataclass `Ledger(entries=[], fail=False)` whose `append` raises `LedgerUnavailable` when `fail` is true, else appends.
    - Verify: `uv run --no-project python -c "from shop.payments import PaymentProvider, PaymentDeclined, PaymentError; from shop.ledger import Ledger, LedgerEntry, LedgerUnavailable"` exits 0; `Ledger(fail=True).append(e)` raises `LedgerUnavailable`.
    - _Requirements: 5.1, 5.2_
  - [x] 1.2 Implement GiftCardService
    - Files: `shop/gift_cards.py`
    - Kind: code
    - Size: L
    - Do: Create `GiftCard`, `GiftCardError(status, error)` and `GiftCardService(payments, ledger, clock)` with `purchase`, `redeem`, `void` exactly per the design.md call tree and check order. One `threading.Lock` around each read-modify-write. Ledger append before each state change; creation entry `old=None`. Codes: 16 chars `A–Z0–9` via `secrets`.
    - Verify: Quick checks with fakes: purchase(25, shopper) → active, 2500 cents, 16-char code; purchase(25, None) → 401 `actor_required`, no charge; redeem 3000 on a 2500 card → 409 `insufficient_balance`; void by shopper → 403 `forbidden`; ledger `fail=True` on purchase → refund called, 503 `ledger_unavailable`.
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 2.1, 2.3, 2.4, 2.5, 2.6, 3.1, 3.2, 3.3, 4.1, 5.1, 5.2, 5.3, 5.4, 5.5_

- [x] 2. Checkpoint — run `uv run --no-project --with pytest --with hypothesis python -m pytest -q`; typecheck: none

- [x] 3. API routes
  - [x] 3.1 Add /gift-cards routes to handle
    - Files: `shop/api.py`
    - Kind: code
    - Size: M
    - Do: Add `POST /gift-cards`, `POST /gift-cards/<code>/redeem` (body `cart_id`; subtotal from `ctx["carts"][cart_id].subtotal_cents()`; missing cart → 404 `no cart`) and `POST /gift-cards/<code>/void` before the `no route` fallback. Make the service once per `ctx` (`"gift_cards"` key) from `ctx["payment_provider"]`, `ctx["ledger"]`, `ctx["clock"]`. Pass `ctx.get("actor")` to each method. Map `GiftCardError` to `{"status": e.status, "body": {"error": e.error}}`. Leave cart routes unchanged.
    - Verify: with fakes in `ctx`, `POST /gift-cards {"value_dollars": 50}` → 201 + 16-char `code`; redeem of an unknown code → 404 `unknown_card`; void with no actor → 403 `forbidden`; `tests/test_cart.py` still passes.
    - _Requirements: 1.2, 2.2, 2.4, 3.1, 3.3, 5.5_

- [x] 4. Checkpoint — run `uv run --no-project --with pytest --with hypothesis python -m pytest -q`; typecheck: none

- [x] 5. Property tests
  - [x]* 5.1 Service property tests
    - Files: `tests/test_gift_cards_service.py`
    - Kind: test
    - Size: M
    - Do: Hypothesis tests against `GiftCardService` with a fake provider, `Ledger` and fixed UTC clock. Seed cards in `service.cards` where a property needs a given balance. Tag comment `Feature: gift-cards, Property N: <title>` per property; ≥100 examples each.
    - **Property 4: Redemption matches the balance model**
    - **Validates: Requirements 2.1, 2.5**
    - **Property 5: Concurrent redemptions equal a sequential run**
    - **Validates: Requirements 2.6**
    - **Property 6: Over-limit balance is rejected**
    - **Validates: Requirements 2.3**
    - **Property 9: Ledger matches every change**
    - **Validates: Requirements 5.1, 5.2**
    - **Property 10: Ledger failure after a charge refunds it**
    - **Validates: Requirements 5.3, 5.4**
    - **Property 12: Cards stay active until voided**
    - **Validates: Requirements 4.1**
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_gift_cards_service.py`
    - _Requirements: 2.1, 2.3, 2.5, 2.6, 4.1, 5.1, 5.2, 5.3, 5.4_
  - [x]* 5.2 API property tests
    - Files: `tests/test_gift_cards_api.py`
    - Kind: test
    - Size: M
    - Do: Hypothesis tests through `handle` with fakes in `ctx`. Tag comment per property; ≥100 examples each. One example test: 100 redemptions finish within 2 seconds (2.2).
    - **Property 1: Purchase creates an active card with the paid balance**
    - **Validates: Requirements 1.1, 1.2**
    - **Property 2: Invalid amounts never charge**
    - **Validates: Requirements 1.4**
    - **Property 3: Payment failures create no card**
    - **Validates: Requirements 1.3, 1.5**
    - **Property 7: Void rules**
    - **Validates: Requirements 3.1, 3.2, 3.3**
    - **Property 8: Unknown codes**
    - **Validates: Requirements 2.4**
    - **Property 11: Missing Actor fails first**
    - **Validates: Requirements 5.5**
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_gift_cards_api.py`
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 2.2, 2.4, 3.1, 3.2, 3.3, 5.5_

- [x] 6. Checkpoint — run `uv run --no-project --with pytest --with hypothesis python -m pytest -q`; typecheck: none

## Notes

- `*` = optional, skip for faster MVP
- Ledger append always comes before the state change (5.2).
- Open Questions F19, F20 are decided in design.md Key design decisions.

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

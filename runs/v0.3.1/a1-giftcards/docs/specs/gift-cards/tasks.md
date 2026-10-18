# Implementation Plan: gift-cards

## Overview

Build bottom-up. First the two leaf modules (ledger, payments), then the store that uses the ledger, then store property tests and the API routes in parallel, then API property tests. One checkpoint after each code layer.

## Tasks

- [x] 1. Core modules
  - [x] 1.1 Add Ledger and PaymentProvider modules
    - Files: `shop/ledger.py`, `shop/payments.py`
    - Kind: code
    - Size: S
    - Do: Create `LedgerEntry`, `LedgerUnavailable`, `Ledger(fail=False)` with `entries` and `append` per design. Create `PaymentFailed`, `RefundFailed`, `PaymentProvider` Protocol, `FakePaymentProvider(fail_charge=False, fail_refund=False)` with `charges` and `refunds`.
    - Verify: `uv run --no-project --with pytest --with hypothesis python -c "from shop.ledger import Ledger, LedgerEntry, LedgerUnavailable; from shop.payments import FakePaymentProvider, PaymentFailed, RefundFailed"`
    - _Requirements: 5.1, 5.2, 1.3, 5.3_
  - [x] 1.2 Add GiftCardStore
    - Files: `shop/giftcards.py`
    - Kind: code
    - Size: L
    - Do: Create `GiftCard`, `UnknownCard`, `CardVoid`, `InsufficientBalance`, and `GiftCardStore(ledger, now=utc_now)` with `get`, `create`, `redeem`, `void`. All mutations under one `threading.Lock`. Check order in `redeem`: unknown, void, insufficient, ledger append, then commit. Ledger append before every commit; UTC ISO timestamps.
    - Verify: `uv run --no-project --with pytest --with hypothesis python -c "from shop.giftcards import GiftCardStore; from shop.ledger import Ledger; s=GiftCardStore(Ledger()); c=s.create(5000,'a'); assert len(c.code)==16; s.redeem(c.code,1000,'a'); assert s.get(c.code).balance_cents==4000"`
    - _Requirements: 1.1, 2.1, 2.2, 2.4, 2.5, 3.1, 3.2, 3.4, 4.1, 4.2, 5.1, 5.2_
  - [x]* 1.3 Store property tests
    - Files: `tests/test_giftcards.py`
    - Kind: test
    - Size: M
    - **Property 3: Redemption matches a balance model**
    - **Validates: Requirements 2.1, 2.4**
    - **Property 4: Concurrent redemptions never overdraw**
    - **Validates: Requirements 2.5**
    - **Property 6: Ledger records every change or blocks it**
    - **Validates: Requirements 5.1, 5.2**
    - Do: Hypothesis tests per design Testing Strategy, `max_examples>=100`, tag comment `Feature: gift-cards, Property N: <title>` per property.
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_giftcards.py`
    - _Requirements: 2.1, 2.4, 2.5, 5.1, 5.2_

- [x] 2. Checkpoint — run `uv run --no-project --with pytest --with hypothesis python -m pytest -q`; typecheck: none

- [x] 3. API routes
  - [x] 3.1 Add gift card routes to Shop_API
    - Files: `shop/api.py`
    - Kind: code
    - Size: M
    - Do: Add `POST /gift-cards`, `POST /gift-cards/<code>/void`, `POST /carts/<id>/gift-card` per design call tree. Read `ctx["giftcards"]`, `ctx["payments"]`, request `actor`. Map store and payment errors to the status codes in design Error Handling.
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_cart.py` stays green; manual `handle` call returns 201 with a 16-char code.
    - _Requirements: 1.1, 1.2, 1.3, 2.1, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4, 5.2, 5.3_
  - [x]* 3.2 API property and example tests
    - Files: `tests/test_giftcards_api.py`
    - Kind: test
    - Size: M
    - **Property 1: Purchase creates an active card with the paid value**
    - **Validates: Requirements 1.1, 1.2**
    - **Property 2: Failed purchase creates no card**
    - **Validates: Requirements 1.3, 5.3**
    - **Property 5: Void and lookup rules**
    - **Validates: Requirements 2.3, 3.1, 3.2, 3.3, 3.4**
    - Do: Hypothesis tests per design, `max_examples>=100`, tag comments. Examples: 2.2 (1000 redemptions within 2 seconds), 4.1/4.2 (store `now` 13 months later, card stays `active` with balance).
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_giftcards_api.py`
    - _Requirements: 1.1, 1.2, 1.3, 2.2, 2.3, 3.1, 3.2, 3.3, 3.4, 4.1, 4.2, 5.3_

- [x] 4. Checkpoint — run `uv run --no-project --with pytest --with hypothesis python -m pytest -q`; typecheck: none

## Notes

- `*` = optional, skip for faster MVP
- Money is in cents everywhere; purchase range 1000–50000 cents.
- Ledger append runs before the state commit, so a ledger failure never needs rollback.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1"] },
    { "id": 1, "tasks": ["1.2"] },
    { "id": 2, "tasks": ["1.3", "3.1"] },
    { "id": 3, "tasks": ["3.2"] }
  ],
  "deps": {
    "1.2": ["1.1"],
    "1.3": ["1.2"],
    "3.1": ["1.1", "1.2"],
    "3.2": ["3.1"]
  }
}
```

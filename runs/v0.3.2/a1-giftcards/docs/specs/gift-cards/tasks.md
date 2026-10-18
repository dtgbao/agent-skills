# Implementation Plan: gift-cards

## Overview

Build the two ports first (payments, ledger), then the `GiftCards` domain service with the fixed check orders and ledger-first commits, then wire the routes into `shop/api.py`. Property tests cover the service; example tests cover `handle` and the 2.2 latency check.

## Tasks

- [x] 1. Gift card domain
  - [x] 1.1 Add the Payment_Provider port and fake
    - Files: `shop/payments.py`
    - Kind: code
    - Size: S
    - Do: create `PaymentError`, `RefundError`, `PaymentProvider` Protocol (`charge(amount_cents) -> str`, `refund(charge_id) -> None`), and `FakePaymentProvider(fail_charge=False, fail_refund=False)` that records `charges: list[tuple[str, int]]` and `refunds: list[str]` and raises when its flag is set, per design "Payments port".
    - Verify: `uv run --no-project --with pytest --with hypothesis python -c "from shop.payments import FakePaymentProvider as F; p=F(); i=p.charge(1000); p.refund(i); assert p.charges==[(i,1000)] and p.refunds==[i]"`
    - _Requirements: 1.1, 1.3, 1.7, 1.8_
  - [x] 1.2 Add the Ledger port
    - Files: `shop/ledger.py`
    - Kind: code
    - Size: S
    - Do: create frozen `LedgerEntry(code, field, old, new, actor_id, at)`, `LedgerError`, `Ledger` Protocol (`append(entry)`), `ListLedger(list)`, and `FailingLedger` whose `append` raises `LedgerError`, per design "Ledger port".
    - Verify: `uv run --no-project --with pytest --with hypothesis python -c "from shop.ledger import ListLedger, FailingLedger, LedgerError; ListLedger().append(1)"`
    - _Requirements: 5.1, 5.2, 5.3_
  - [x] 1.3 Implement the GiftCards service
    - Files: `shop/giftcards.py`
    - Kind: code
    - Size: L
    - Do: create `GiftCard`, `GiftCardError(http, error)`, constants `MIN_CENTS=1000`, `MAX_CENTS=50000`, `REDEEM_CAP_CENTS=100000`, and `GiftCards(payments, ledger, clock)` with `buy`, `redeem`, `void` exactly per the design pseudocode (check order, ledger-first commit, refund on Ledger failure).
    - Do: codes are 16 chars from `A–Z0–9` via `secrets.choice`, regenerated on collision; Ledger timestamps from `clock()` in UTC; no time-based status change.
    - Verify: `uv run --no-project --with pytest --with hypothesis python -c "from shop.giftcards import GiftCards; from shop.payments import FakePaymentProvider; from shop.ledger import ListLedger; g=GiftCards(FakePaymentProvider(), ListLedger()); c=g.buy(1000,'u'); assert g.redeem(c,400,'u')==600"`
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 2.1, 2.3, 2.4, 2.5, 2.6, 2.7, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 4.1, 4.2, 5.1, 5.2, 5.3_

- [x] 2. Checkpoint — run `uv run --no-project --with pytest --with hypothesis python -m pytest -q`; typecheck: none

- [x] 3. Shop_API routes
  - [x] 3.1 Wire gift card routes into handle
    - Files: `shop/api.py`
    - Kind: code
    - Size: M
    - Do: add `POST /gift-cards` (201 `{"code"}`), `POST /gift-cards/{code}/void` (200 `{"status"}`), `POST /carts/{id}/gift-card` (200 `{"balance_cents"}`) using `ctx["giftcards"]` and `ctx["actor"]`; map `GiftCardError` to `{"status": e.http, "body": {"error": e.error}}`. Keep existing cart routes unchanged.
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_cart.py`
    - _Requirements: 1.2, 2.2, 3.1, 3.5_

- [x] 4. Checkpoint — run `uv run --no-project --with pytest --with hypothesis python -m pytest -q`; typecheck: none

- [x] 5. Tests
  - [x]* 5.1 Property tests for the GiftCards service
    - Files: `tests/test_giftcards_props.py`
    - Kind: test
    - Size: M
    - Do: one Hypothesis test per property, `max_examples ≥ 100`, tag comment `Feature: gift-cards, Property N: <title>`; generators per design Testing Strategy.
    - **Property 1: Purchase creates an active card**
    - **Validates: Requirements 1.1, 1.2**
    - **Property 2: Out-of-range value is rejected without a charge**
    - **Validates: Requirements 1.5, 1.6**
    - **Property 3: Charge failure creates no card**
    - **Validates: Requirements 1.3, 1.4**
    - **Property 4: Ledger failure on purchase refunds**
    - **Validates: Requirements 1.7, 1.8, 5.2**
    - **Property 5: Redemption subtracts the subtotal**
    - **Validates: Requirements 2.1**
    - **Property 6: Insufficient balance leaves balance unchanged**
    - **Validates: Requirements 2.5, 2.6**
    - **Property 7: Redemption check order**
    - **Validates: Requirements 2.3, 2.7, 3.2, 3.7**
    - **Property 8: Unknown code**
    - **Validates: Requirements 2.4, 3.3**
    - **Property 9: Void is idempotent**
    - **Validates: Requirements 3.1, 3.4**
    - **Property 10: Non-staff void is forbidden**
    - **Validates: Requirements 3.5, 3.6**
    - **Property 11: Ledger replays to state**
    - **Validates: Requirements 5.1, 5.2, 5.3**
    - **Property 12: No expiry**
    - **Validates: Requirements 4.1, 4.2**
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_giftcards_props.py`
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 2.1, 2.3, 2.4, 2.5, 2.6, 2.7, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 4.1, 4.2, 5.1, 5.2, 5.3_
  - [x] 5.2 API example tests and latency check
    - Files: `tests/test_giftcards_api.py`
    - Kind: test
    - Size: M
    - Do: through `handle`: buy → 201 + 16-char code; bad value → 400 `bad_value`; redeem → 200 balance; void as staff → 200; void as shopper → 403 `forbidden`; unknown code → 404 `unknown_card`; void card redeem → 409 `card_void`.
    - Do: 2.2 latency: 1000 sequential redemptions through `handle`, assert p95 < 2 seconds.
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_giftcards_api.py`
    - _Requirements: 1.2, 1.5, 2.1, 2.2, 2.4, 3.1, 3.2, 3.5_

- [x] 6. Checkpoint — run `uv run --no-project --with pytest --with hypothesis python -m pytest -q`; typecheck: none

## Notes

- `*` = optional, skip for faster MVP
- Money is integer cents only. 10–500 dollars = 1000–50000 cents; 1000 dollars = 100000 cents.
- Ledger entry is written before any mutation; a Ledger failure must leave state unchanged.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.2"] },
    { "id": 1, "tasks": ["1.3"] },
    { "id": 2, "tasks": ["3.1", "5.1"] },
    { "id": 3, "tasks": ["5.2"] }
  ],
  "deps": {
    "1.3": ["1.1", "1.2"],
    "3.1": ["1.3"],
    "5.1": ["1.3"],
    "5.2": ["3.1"]
  }
}
```

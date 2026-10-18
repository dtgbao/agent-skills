# Implementation Plan: discount-codes

## Overview

Build bottom-up: the pure `shop/discounts.py` module first, then the `Cart` slot and methods, then the API routes. Each code layer has one optional property-test leaf and a checkpoint. Test leaves depend on the code they cover.

## Tasks

- [x] 1. Discount codes module
  - [x] 1.1 Create `shop/discounts.py` with registry and discount math
    - Files: `shop/discounts.py`
    - Kind: code
    - Size: M
    - Do: Add `PERCENT_MAX = 90`, `CODE_RE`, `InvalidCode`/`DuplicateCode` (`ValueError` subclasses), frozen `DiscountCode`, `is_valid_code_string`, `CodeRegistry.register/get`, `discount_cents(code, subtotal_cents, today)` per design "Discounts" pseudocode.
      Expiry text must be strict `YYYY-MM-DD` (regex then `date.fromisoformat`); reject `bool` as int.
    - Verify: `uv run --no-project --with pytest --with hypothesis python -c "from shop.discounts import CodeRegistry, discount_cents"` exits 0
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 4.1, 4.2, 4.5, 4.6, 4.7_
  - [x]* 1.2 Property tests for the registry
    - Files: `tests/test_discounts.py`
    - Kind: test
    - Size: M
    - **Property 1: Registry accepts exactly the valid records**
    - **Validates: Requirements 1.1, 1.2, 1.3, 1.4, 1.6, 1.7, 1.8**
    - **Property 2: Duplicate registration is rejected**
    - **Validates: Requirements 1.5**
    - Do: Hypothesis tests per design Testing Strategy rows 1–2, `max_examples=200`, tag comments; plus examples for percent 0, 1, 90, 91 and expiry `2026-02-30`.
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_discounts.py`
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8_

- [x] 2. Checkpoint — run `uv run --no-project --with pytest --with hypothesis python -m pytest -q`; typecheck: none

- [x] 3. Cart discount slot
  - [x] 3.1 Add `applied_code`, `discount_cents(today)`, `total_cents(today)` to `Cart`
    - Files: `shop/cart.py`
    - Kind: code
    - Size: S
    - Do: In `Cart.__init__` set `self.applied_code = None`. Add `discount_cents(self, today)` → `shop.discounts.discount_cents(self.applied_code, self.subtotal_cents(), today)` and `total_cents(self, today)` → subtotal − discount. Never clear `applied_code` in `add`/`remove`.
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_cart.py` (existing tests stay green)
    - _Requirements: 3.4, 4.3, 4.8_
  - [x]* 3.2 Property tests for discount math and Cart totals
    - Files: `tests/test_cart_discount.py`
    - Kind: test
    - Size: M
    - **Property 3: Discount formula**
    - **Validates: Requirements 4.1, 4.2**
    - **Property 4: Total stays in bounds**
    - **Validates: Requirements 4.3**
    - **Property 5: Zero discount when not eligible**
    - **Validates: Requirements 4.5, 4.6, 4.7**
    - Do: Hypothesis tests per design Testing Strategy rows 3–5, `max_examples=200`, tag comments; test via both `discount_cents` and a `Cart` with `applied_code` set.
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_cart_discount.py`
    - _Requirements: 4.1, 4.2, 4.3, 4.5, 4.6, 4.7_

- [x] 4. Checkpoint — run `uv run --no-project --with pytest --with hypothesis python -m pytest -q`; typecheck: none

- [x] 5. Cart API discount routes
  - [x] 5.1 Add `POST`/`DELETE /carts/<id>/discount` and widen `GET /carts/<id>`
    - Files: `shop/api.py`
    - Kind: code
    - Size: M
    - Do: Per design "Cart_API" pseudocode: check order no cart → 400 → 404 → 410 → 422 → 409 → attach; DELETE always 200 (F7 decision); totals body `subtotal_cents, discount_cents, total_cents, code`.
      Read `ctx["codes"]` and `ctx["clock"]`; GET/DELETE call the clock only when a code is applied. Update the `handle` docstring.
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_cart.py` stays green; manual `handle` call with a fake ctx returns 200 with `discount_cents`
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 3.1, 3.2, 3.3, 3.4, 4.4_
  - [x]* 5.2 Property tests for the API
    - Files: `tests/test_api_discount.py`
    - Kind: test
    - Size: M
    - **Property 6: API status matches the check-order model**
    - **Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 3.1, 3.2**
    - **Property 7: Apply then remove round-trips**
    - **Validates: Requirements 3.3, 4.4**
    - **Property 8: Applied code survives rejection and expiry**
    - **Validates: Requirements 3.4, 4.8**
    - Do: Hypothesis tests per design Testing Strategy rows 6–8, `max_examples=200`, tag comments; build a fresh ctx per example (`carts`, `Inventory`, `CodeRegistry`, fixed `clock`).
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_api_discount.py`
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 3.1, 3.2, 3.3, 3.4, 4.4, 4.8_

- [x] 6. Checkpoint — run `uv run --no-project --with pytest --with hypothesis python -m pytest -q`; typecheck: none

## Notes

- `*` = optional, skip for faster MVP
- `PERCENT_MAX` lives only in `shop/discounts.py`; tests should import it, not hard-code 90.
- `Cart` never reads the clock; callers pass `today`.
- Inventory `reserve` checks against initial stock, not available stock; out of scope here.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1"] },
    { "id": 1, "tasks": ["1.2", "3.1"] },
    { "id": 2, "tasks": ["3.2", "5.1"] },
    { "id": 3, "tasks": ["5.2"] }
  ],
  "deps": {
    "1.2": ["1.1"],
    "3.1": ["1.1"],
    "3.2": ["1.1", "3.1"],
    "5.1": ["1.1", "3.1"],
    "5.2": ["1.1", "3.1", "5.1"]
  }
}
```

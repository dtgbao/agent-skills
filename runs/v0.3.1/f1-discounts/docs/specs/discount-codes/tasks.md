# Implementation Plan: discount-codes

## Overview

Build bottom-up: the pure `shop/discounts.py` module first, then `Cart` code handling, then the API routes. Each layer gets a property test file and a checkpoint. Test leaves are optional (`*`).

## Tasks

- [x] 1. Discounts module
  - [x] 1.1 Create DiscountCode, CodeRegistry and discount_amount
    - Files: `shop/discounts.py`
    - Kind: code
    - Size: M
    - Do: Create `DiscountCode` frozen dataclass (`code`, `kind`, `value`, `expires_on`, `min_subtotal_cents=0`) with `__post_init__` raising `ValueError` per 1.2–1.5; `CODE_RE = [A-Z0-9-]{1,20}`, `PERCENT_MIN, PERCENT_MAX = 1, 50`.
    - Do: Create `CodeRegistry` with `add(dc)` (ValueError on duplicate, keep existing) and `get(code) -> DiscountCode | None`.
    - Do: Create `is_expired(dc, today)` (today > expires_on) and `discount_amount(dc, subtotal_cents, today)` per design pseudocode.
    - Verify: `uv run --no-project --with pytest --with hypothesis python -c "import shop.discounts"` exits 0
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 3.1, 3.2, 3.3, 4.1, 4.2, 4.3_
  - [x]* 1.2 Property tests for discounts module
    - Files: `tests/test_discounts.py`
    - Kind: test
    - Size: M
    - **Property 1: Percent discount is floor of percent of subtotal**
    - **Validates: Requirements 3.1**
    - **Property 2: Fixed discount is capped at subtotal**
    - **Validates: Requirements 3.2**
    - **Property 4: Invalid applied code gives zero discount**
    - **Validates: Requirements 4.1, 4.2, 4.3**
    - **Property 5: Code record validation**
    - **Validates: Requirements 1.1, 1.2, 1.3, 1.4, 1.5**
    - Do: Add example test: duplicate `CodeRegistry.add` raises `ValueError` and `get` returns the first record (1.6).
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_discounts.py`
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 3.1, 3.2, 4.1, 4.2, 4.3_

- [x] 2. Checkpoint — run `uv run --no-project --with pytest --with hypothesis python -m pytest -q`; typecheck: none

- [x] 3. Cart code handling
  - [x] 3.1 Add applied code, discount and total to Cart
    - Files: `shop/cart.py`
    - Kind: code
    - Size: M
    - Do: Add `AlreadyApplied` exception; `Cart.applied_code = None` in `__init__`; `apply_code(dc)` raises `AlreadyApplied` when a code is held; `clear_code()` sets None (no error when none held).
    - Do: Add `discount_cents(today)` calling `shop.discounts.discount_amount(self.applied_code, self.subtotal_cents(), today)` and `total_cents(today) = subtotal - discount`.
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_cart.py` stays green
    - _Requirements: 2.5, 3.3, 3.4, 4.3, 4.4, 5.1, 5.3_
  - [x]* 3.2 Property tests for Cart discount
    - Files: `tests/test_cart_discount.py`
    - Kind: test
    - Size: M
    - **Property 3: Total stays between 0 and subtotal**
    - **Validates: Requirements 3.3, 3.4**
    - Do: Add examples: second `apply_code` raises `AlreadyApplied` and keeps the first (2.5); `clear_code` on empty cart is a no-op (5.3); `discount_cents`/`total_cents` take `today` as argument (4.4).
    - Do: Generate percent `value` from `PERCENT_MIN..PERCENT_MAX` imported from `shop/discounts.py`; no hard-coded bound.
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_cart_discount.py`
    - _Requirements: 2.5, 3.3, 3.4, 4.4, 5.3_

- [x] 4. Checkpoint — run `uv run --no-project --with pytest --with hypothesis python -m pytest -q`; typecheck: none

- [x] 5. API routes
  - [x] 5.1 Add code routes and discount fields to handle
    - Files: `shop/api.py`
    - Kind: code
    - Size: M
    - Do: `POST /carts/<id>/code`: checks in order 5.2 → 2.7 (400 `bad code`) → 2.2 (404 `unknown code`) → 2.3 (410 `code expired`) → 2.4 (422 `minimum not met`) → 2.5 (409 `code already applied`) → 200 `{code, discount_cents, total_cents}`.
    - Do: `DELETE /carts/<id>/code` → `cart.clear_code()`, 200. `GET /carts/<id>` adds `code` (or None), `discount_cents`, `total_cents` using `ctx["today"]`.
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_cart.py` stays green
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 3.5, 5.1, 5.2, 5.3_
  - [x]* 5.2 Property and example tests for code routes
    - Files: `tests/test_api_codes.py`
    - Kind: test
    - Size: M
    - **Property 6: POST code status follows the check order**
    - **Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 5.2**
    - Do: Add examples: 2.1 apply then GET shows code and discount (3.5); DELETE clears (5.1); DELETE with no code returns 200 (5.3); unknown cart on DELETE returns 404 `no cart` (5.2).
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_api_codes.py`
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 3.5, 5.1, 5.2, 5.3_

- [x] 6. Checkpoint — run `uv run --no-project --with pytest --with hypothesis python -m pytest -q`; typecheck: none

## Notes

- `*` = optional, skip for faster MVP
- `ctx["codes"]` and `ctx["today"]` are new ctx keys; tests build them.
- Percent bound lives in `PERCENT_MIN, PERCENT_MAX` in `shop/discounts.py` only.

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
    "3.2": ["3.1"],
    "5.1": ["1.1", "3.1"],
    "5.2": ["5.1"]
  }
}
```

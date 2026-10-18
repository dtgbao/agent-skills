# Implementation Plan: cart-discount-codes

## Overview

Build bottom-up. First `shop/discounts.py` (record, registry, format checks, pure formula), then the Cart code slot, then their property tests. Then the API routes and their property and example tests. A checkpoint follows each layer.

## Tasks

- [x] 1. Discount core and Cart
  - [x] 1.1 Create discounts module
    - Files: `shop/discounts.py`
    - Kind: code
    - Size: M
    - Do: create `DiscountCode` (frozen dataclass), `CodeRegistry.register/get`, `is_well_formed`, `parse_today`, `discount_cents(subtotal, code, today)` per design `### Discounts`. Integer checks reject `bool`. Registry stores upper-case keys; `get` is case-insensitive.
    - Do: `register` raises ValueError on: percent value outside 1–50, fixed value outside 1–10,000,000, bad Code_String/kind/value/minimum (0–10,000,000)/expiry (`YYYY-MM-DD`), duplicate code in any case.
    - Verify: `python -c "from shop.discounts import CodeRegistry, discount_cents, is_well_formed, parse_today"`; existing tests pass.
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 2.10, 3.1, 3.2, 3.3, 3.5, 3.6_
  - [x] 1.2 Add code slot to Cart
    - Files: `shop/cart.py`
    - Kind: code
    - Size: S
    - Do: add `self.code: DiscountCode | None = None`, `attach(code)`, `detach()`, `discount_cents(today)` (calls `discounts.discount_cents`), `total_cents(today)` = `max(0, subtotal - discount)`.
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_cart.py` passes.
    - _Requirements: 3.4, 4.3_
  - [x]* 1.3 Property tests for registry, format, formula
    - Files: `tests/test_discounts.py`
    - Kind: test
    - Size: M
    - **Property 1: Registry accepts exactly the in-bound codes**
    - **Validates: Requirements 1.1, 1.2, 1.3, 1.4, 1.5**
    - **Property 2: Code_String format check**
    - **Validates: Requirements 2.10, 2.2**
    - **Property 3: Discount formula matches the model**
    - **Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5, 3.6**
    - Do: Hypothesis tests, `@settings(max_examples=100)` or more, generators per design Testing Strategy, tag comment `# Feature: cart-discount-codes, Property N: <title>` per property.
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_discounts.py`
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 2.10, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_

- [x] 2. Checkpoint — run `uv run --no-project --with pytest --with hypothesis python -m pytest -q`; typecheck: none

- [x] 3. Shop API
  - [x] 3.1 Add discount routes and totals
    - Files: `shop/api.py`
    - Kind: code
    - Size: M
    - Do: for every `/carts/<id>` route, call `parse_today(ctx.get("today"))` first (ValueError propagates), then cart lookup (404 `no cart`). Add `POST /carts/<id>/discount` with checks in order: 400 `bad code`, 404 `unknown code`, 409 `code already applied`, 422 `code expired`, 422 `minimum not met`, then attach and 200 with totals. Registry = `ctx.get("codes")`, missing → empty.
    - Do: add `DELETE /carts/<id>/discount` (200 with `discount_cents` 0, or 404 `no code applied`). `POST /lines` body = `sku`, `quantity` (int 1–1,000), `unit_price_cents` (int 0–10,000,000), else 400 `bad line` before `cart.add`; 200 returns totals. `GET` adds `discount_code`, `discount_cents`, `total_cents`.
    - Verify: existing tests pass; a manual `handle()` call with a registered code returns 200 with `discount_cents` > 0.
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 4.1, 4.2, 4.3, 4.4, 4.5_
  - [x]* 3.2 API property and example tests
    - Files: `tests/test_api_discounts.py`
    - Kind: test
    - Size: M
    - **Property 4: Apply returns the first failing check**
    - **Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.8**
    - **Property 5: Apply then remove restores the cart**
    - **Validates: Requirements 4.3**
    - **Property 6: Bad clock fails before anything**
    - **Validates: Requirements 2.9**
    - **Property 7: Bad line body is rejected**
    - **Validates: Requirements 4.5**
    - Do: Hypothesis tests (≥100 examples, tag comments) plus example tests for 2.7 (`no cart`), 4.1 (GET fields), 4.2 (lines response fields), 4.4 (`no code applied`).
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_api_discounts.py`
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 4.1, 4.2, 4.3, 4.4, 4.5_

- [x] 4. Checkpoint — run `uv run --no-project --with pytest --with hypothesis python -m pytest -q`; typecheck: none

## Notes

- `*` = optional, skip for faster MVP
- Subtotal uses the `CATALOG` price; body `unit_price_cents` is validated only (design decision for 4.5).
- `ctx["today"]` is a `YYYY-MM-DD` string; `ctx["codes"]` is a `CodeRegistry`.

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
    "1.3": ["1.1", "1.2"],
    "3.1": ["1.1", "1.2"],
    "3.2": ["3.1", "1.2", "1.1"]
  }
}
```

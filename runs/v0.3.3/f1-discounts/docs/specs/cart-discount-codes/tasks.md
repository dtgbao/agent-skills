# Implementation Plan: cart-discount-codes

## Overview

Build bottom up: `shop/discounts.py` first (record, registry, error, `compute_discount`), then the Cart methods, then the API routes. Each code leaf has an optional property or example test leaf after it. A checkpoint runs the full suite after each layer.

## Tasks

- [x] 1. Discount records and registry
  - [x] 1.1 Create `shop/discounts.py`
    - Files: `shop/discounts.py`
    - Kind: code
    - Size: M
    - Do:
      - Add `DiscountError(Exception)`, frozen dataclass `DiscountCode(code_string, kind, value, minimum_subtotal, expiry_date)` with no validation, `CODE_RE = re.compile(r"[A-Z0-9]{1,20}")`, `MAX_CENTS = 10_000_000`.
      - Add `CodeRegistry` with `add(code)` (raise `ValueError` and store nothing on: kind not `percent`/`fixed`; percent value not int 1–50; fixed value not int 1–10,000,000; code string not `CODE_RE.fullmatch`; minimum not int 0–10,000,000; expiry not `datetime.date`; duplicate code string; `bool` is not an int here) and `get(code_string) -> DiscountCode | None` (exact key).
      - Add `compute_discount(code, subtotal, today) -> int`: 0 if code is None, if `today > expiry_date`, or if `subtotal < minimum_subtotal`; percent → `subtotal * value // 100`; fixed → `min(value, subtotal)`.
    - Verify: `uv run --no-project --with pytest --with hypothesis python -c "from datetime import date; from shop.discounts import *; r=CodeRegistry(); c=DiscountCode('SAVE10','percent',10,0,date(2030,1,1)); r.add(c); assert r.get('SAVE10') is c and r.get('save10') is None; assert compute_discount(c,1999,date(2029,1,1))==199"`
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 4.1, 4.2, 4.3, 4.5, 4.6_
  - [x]* 1.2 Property tests for registry and discount function
    - Files: `tests/test_discounts.py`
    - Kind: test
    - Size: M
    - **Property 1: Registry accepts exactly the valid codes**
    - **Validates: Requirements 1.2, 1.3, 1.4, 1.5, 1.7**
    - **Property 2: Add then get round-trip**
    - **Validates: Requirements 1.1, 1.6**
    - **Property 4: Percent formula**
    - **Validates: Requirements 4.1**
    - **Property 5: Fixed formula**
    - **Validates: Requirements 4.2**
    - **Property 6: Inactive code gives zero**
    - **Validates: Requirements 4.3, 4.5, 4.6**
    - Do: Hypothesis tests, `@settings(max_examples=100)` or more, one tag comment `# Feature: cart-discount-codes, Property N: <title>` per property. Generators per design.md Testing Strategy. Percent bound 1–50 (criterion 1.2).
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_discounts.py`
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 4.1, 4.2, 4.3, 4.5, 4.6_

- [x] 2. Checkpoint — run `uv run --no-project --with pytest --with hypothesis python -m pytest -q`; typecheck: none

- [x] 3. Cart discount methods
  - [x] 3.1 Add discount methods to `Cart`
    - Files: `shop/cart.py`
    - Kind: code
    - Size: M
    - Do:
      - Import from `shop.discounts`. Set `self.applied_code = None` in `__init__`.
      - Add `apply_code(code_string, registry, today)`: raise `DiscountError` in this order: `code already applied` (applied_code set), `unknown code` (`registry.get` is None), `expired` (`today > expiry_date`), `below minimum` (`subtotal_cents() < minimum_subtotal`); else set `applied_code`.
      - Add `remove_code()` (set None, no error), `discount_cents(today)` (= `compute_discount(self.applied_code, self.subtotal_cents(), today)`), `total_cents(today)` (= subtotal − discount).
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_cart.py` stays green, plus `uv run --no-project --with pytest --with hypothesis python -c "from datetime import date; from shop.cart import Cart; from shop.inventory import Inventory; from shop.discounts import *; r=CodeRegistry(); r.add(DiscountCode('OFF500','fixed',500,1000,date(2030,1,1))); c=Cart(Inventory({'MUG-01':5})); c.add('MUG-01',1); c.apply_code('OFF500',r,date(2029,1,1)); assert c.total_cents(date(2029,1,1))==700; c.remove_code(); c.remove_code(); assert c.applied_code is None"`
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 3.1, 3.2, 4.3, 4.4, 4.5, 4.6_
  - [x]* 3.2 Property tests for Cart apply, remove, totals
    - Files: `tests/test_cart_discount.py`
    - Kind: test
    - Size: M
    - **Property 3: Discount bounds and total**
    - **Validates: Requirements 4.4**
    - **Property 7: Apply matches the precedence model**
    - **Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7**
    - **Property 8: Remove is idempotent**
    - **Validates: Requirements 3.1, 3.2**
    - Do: Hypothesis tests, `@settings(max_examples=100)` or more, one tag comment per property. Property 7 compares `apply_code` against a small reference model of the 2.7 order. Use a large-stock `Inventory` so `add` never raises `OutOfStock`. Valid percent values 1–50 (criterion 1.2).
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_cart_discount.py`
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 3.1, 3.2, 4.4_

- [x] 4. Checkpoint — run `uv run --no-project --with pytest --with hypothesis python -m pytest -q`; typecheck: none

- [x] 5. API routes
  - [x] 5.1 Add discount routes and GET fields to `handle`
    - Files: `shop/api.py`
    - Kind: code
    - Size: M
    - Do:
      - Update the `ctx` docstring: add `"codes": CodeRegistry, "today": date`. Add `_totals(cart, today)` → `subtotal_cents`, `discount_cents`, `total_cents`.
      - Before the `/lines` branch: `POST .../discount` → 400 `bad code` if `body.get("code")` is not a `str`; call `cart.apply_code(code, ctx["codes"], ctx["today"])`; `DiscountError` → 409 if message is `code already applied`, else 400 `{"error": msg}`; success → 200 `_totals`. `DELETE .../discount` → `remove_code()`, 200 `_totals`.
      - `GET` body → `{"lines", "code" (applied code string or None), **_totals}`.
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q` stays green
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6_
  - [x]* 5.2 Example tests for discount routes
    - Files: `tests/test_api_discount.py`
    - Kind: test
    - Size: S
    - Do: One example test per criterion 5.1–5.6 through `handle` with a fixed `CodeRegistry` and `today`. Cover 400 for `unknown code`, `expired`, `below minimum`, 409 for a second code, 400 `bad code` for missing and non-str `code`, DELETE 200, GET fields incl. `code` null after DELETE.
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_api_discount.py`
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6_

- [x] 6. Checkpoint — run `uv run --no-project --with pytest --with hypothesis python -m pytest -q`; typecheck: none

## Notes

- `*` = optional, skip for faster MVP
- Money is integer cents everywhere. Today is always passed in; the core never reads a clock.
- `Inventory.reserve` checks `qty` against initial stock, not available stock. Out of scope here.

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
    "5.1": ["3.1"],
    "5.2": ["5.1"]
  }
}
```

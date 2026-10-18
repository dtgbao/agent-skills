# Implementation Plan: discount-codes

## Overview

Three layers, bottom up. First `shop/discounts.py`: the record, the `CodeBook`, `AttachRefused`, and `discount_for`. Then the Cart methods. Then the handler guard and routes. Each code leaf has an optional test leaf after it. A checkpoint runs the whole suite after each layer.

## Tasks

- [x] 1. Discounts module
  - [x] 1.1 Write `shop/discounts.py`
    - Files: `shop/discounts.py`
    - Kind: code
    - Size: M
    - Do:
      - Define `CODE_FORMAT = re.compile(r"[A-Z0-9-]{3,16}")`, frozen dataclass `DiscountCode(code, kind, amount, min_subtotal, valid_until)`, and `AttachRefused(Exception)` with a `reason` attribute.
      - `CodeBook.create(code, kind, amount, min_subtotal, valid_until) -> DiscountCode`: raise `ValueError` and store nothing when kind is not `percent`/`fixed`; amount is not an `int` (a `bool` is not an int); percent amount is outside 1–50; fixed amount is outside 1–1,000,000; code is not a `str` matching `CODE_FORMAT` in full; min_subtotal is not an `int` or is outside 0–1,000,000; valid_until is not a `datetime.date`; the code is already in the book. `CodeBook.get(code) -> DiscountCode | None`.
      - `discount_for(dc, subtotal, today) -> int`: 0 when `dc` is None, `today > dc.valid_until`, or `subtotal < dc.min_subtotal`; percent → `subtotal * dc.amount // 100`; fixed → `min(dc.amount, subtotal)`.
    - Verify: `uv run --no-project --with pytest --with hypothesis python -c "from datetime import date; from shop.discounts import *; b=CodeBook(); d=b.create('SPRING-10','percent',10,0,date(2031,3,1)); assert b.get('SPRING-10') is d and b.get('spring-10') is None; assert discount_for(d,2599,date(2031,3,1))==259 and discount_for(d,2599,date(2031,3,2))==0"`
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 4.1, 4.2, 4.3, 4.5, 4.6_
  - [x]* 1.2 Property tests for the discounts module
    - Files: `tests/test_discounts.py`
    - Kind: test
    - Size: M
    - **Property 1: Create accepts exactly valid fields**
    - **Validates: Requirements 1.2, 1.3, 1.4, 1.5, 1.7**
    - **Property 2: Create then get, duplicates keep the first**
    - **Validates: Requirements 1.1, 1.6**
    - **Property 3: Pricing matches the reference model**
    - **Validates: Requirements 4.1, 4.2, 4.3, 4.5, 4.6**
    - Do: Hypothesis tests with `max_examples` at least 100. Put a tag comment `# Feature: discount-codes, Property N: <title>` above each property test. Generators per design.md Testing Strategy rows 1–3.
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_discounts.py`
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 4.1, 4.2, 4.3, 4.5, 4.6_

- [x] 2. Checkpoint — run `uv run --no-project --with pytest --with hypothesis python -m pytest -q`; typecheck: none

- [x] 3. Cart code methods
  - [x] 3.1 Add code methods to `Cart`
    - Files: `shop/cart.py`
    - Kind: code
    - Size: M
    - Do:
      - Import `AttachRefused`, `discount_for` from `shop.discounts`. Set `self.attached = None` in `__init__`.
      - `attach_code(code, code_book, today)`: `dc = code_book.get(code)`; raise `AttachRefused` with reason `code_not_found` (dc is None), then `code_already_attached` (attached is set), then `code_expired` (`today > dc.valid_until`), then `minimum_not_met` (`subtotal_cents() < dc.min_subtotal`); else set `attached = dc`. No write before a raise.
      - `detach_code()` sets `attached = None`. `discount_cents(today)` = `discount_for(self.attached, self.subtotal_cents(), today)`. `amount_due_cents(today)` = subtotal − discount.
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_cart.py` stays green, and `uv run --no-project --with pytest --with hypothesis python -c "from datetime import date; from shop.cart import Cart; from shop.inventory import Inventory; from shop.discounts import *; b=CodeBook(); b.create('KETTLE-5','fixed',500,3000,date(2031,1,1)); c=Cart(Inventory({'KET-01':3})); c.add('KET-01',1); c.attach_code('KETTLE-5',b,date(2030,12,31)); assert c.amount_due_cents(date(2030,12,31))==3499; c.detach_code(); c.detach_code(); assert c.attached is None"`
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 3.1, 3.2, 4.3, 4.4, 4.5, 4.6_
  - [x]* 3.2 Property tests for Cart code methods
    - Files: `tests/test_cart_codes.py`
    - Kind: test
    - Size: M
    - **Property 4: Amount due identity**
    - **Validates: Requirements 4.4**
    - **Property 5: Attach matches the precedence model**
    - **Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7**
    - **Property 6: Detach is idempotent**
    - **Validates: Requirements 3.1, 3.2**
    - Do: Hypothesis tests with `max_examples` at least 100 and one tag comment per property. Property 5 compares `attach_code` with a small reference function of the 2.7 order. Build carts on an `Inventory` with large stock so `add` never raises. Percent amounts are 1–50 (criterion 1.2).
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_cart_codes.py`
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 3.1, 3.2, 4.4_

- [x] 4. Checkpoint — run `uv run --no-project --with pytest --with hypothesis python -m pytest -q`; typecheck: none

- [x] 5. Handler routes
  - [x] 5.1 Add context guard and code routes to `handle`
    - Files: `shop/api.py`
    - Kind: code
    - Size: M
    - Do:
      - Extend the `ctx` docstring with `"code_book": CodeBook, "today": date`. Add `_context_ok(ctx)` (`"code_book" in ctx` and `ctx.get("today")` is a `datetime.date`) and `_prices(cart, today)` (`subtotal_cents`, `discount_cents`, `amount_due_cents`).
      - Inside the `/carts/` branch, before the cart lookup: when the path ends with `/code`, or the method is `GET`, and `not _context_ok(ctx)` → 500 `{"error": "bad_context"}`. `POST /carts` and `POST .../lines` get no guard.
      - After the lookup: `PUT .../code` → 400 `invalid_body` if `body.get("code")` is not a `str`; `attach_code(...)`; `AttachRefused` → 422 `{"error": e.reason}`; else 200 `_prices`. `DELETE .../code` → `detach_code()`, 200 `_prices`. `GET` body → `lines`, `code` (`attached.code` or None), plus `_prices`.
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q` stays green
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7_
  - [x]* 5.2 Handler tests
    - Files: `tests/test_api_codes.py`
    - Kind: test
    - Size: M
    - **Property 7: Bad context gives 500 and changes nothing**
    - **Validates: Requirements 5.6, 5.7**
    - Do: Property 7 with Hypothesis (`max_examples` at least 100, tag comment). Plus one example test each for 5.1–5.5 through `handle` with a fixed `CodeBook` and `today`: 200 attach, 422 per reason, 400 `invalid_body` (missing and non-str), DELETE 200, GET keys with `code` null and set.
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_api_codes.py`
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7_

- [x] 6. Checkpoint — run `uv run --no-project --with pytest --with hypothesis python -m pytest -q`; typecheck: none

## Notes

- `*` = optional, skip for faster MVP
- All money in integer cents. The date always comes from the caller.
- Open Questions F6, F9, F11 are decided in design.md Key design decisions.

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

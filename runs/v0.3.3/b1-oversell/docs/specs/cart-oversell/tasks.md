# Implementation Plan: cart oversell

## Overview

Pin the bug first. The exploration pin reproduces the oversell and fails on current code. The preservation pins hold the five Unchanged items and pass on current code. Then change the check in `Inventory.reserve` to compare with available units. A checkpoint confirms all pins are green. An optional API test then covers the same-cart path and the 409 response, with a final checkpoint.

## Tasks

- [x] 1. Pins
  - [x] 1.1 Write exploration pin for cross-cart oversell
    - Files: `tests/test_oversell_pin.py`
    - Kind: pin
    - Size: S
    - Expect: red
    - Do: Example test: `Inventory({"MUG-01": 5})`, cart A adds 3, cart B adds 3 → `pytest.raises(OutOfStock)`, then `available("MUG-01") == 2`. Example test through `shop.api.handle`: two carts, second `POST /carts/<id>/lines` with qty 3 → status 409. Hypothesis test for Property 1 (stock 1–50, `a` 1–stock, `b` 1–stock, `a + b > stock`), ≥100 examples, tag comment `Feature: cart-oversell, Property 1: Fix check`.
    - **Property 1: Fix check**
    - **Validates: Requirements 2.1, 2.2, 2.3**
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_oversell_pin.py` fails on current code (second add accepted, available -1, status 200)
    - _Requirements: 2.1, 2.2, 2.3_
  - [x] 1.2 Write preservation pins for unchanged behavior
    - Files: `tests/test_oversell_preservation.py`
    - Kind: pin
    - Size: M
    - Expect: green
    - Do: Hypothesis tests for Property 2, one per Unchanged item, ≥100 examples each, tag comment `Feature: cart-oversell, Property 2: Preservation`: 3.1 single qty above stock → `OutOfStock`; 3.2 qty in −10–0 → `ValueError`; 3.3 reserves then releases of any qty 0–100 → `available ≤ initial`; 3.4 `Cart.add` then `Cart.remove` → available back to value before the add; 3.5 reserve sequences with running sum ≤ stock → all accepted, `available == stock - sum`.
    - **Property 2: Preservation**
    - **Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5**
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_oversell_preservation.py` passes on current code
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [x] 2. Fix
  - [x] 2.1 Check reserve against available units
    - Files: `shop/inventory.py`
    - Kind: code
    - Size: S
    - Do: In `Inventory.reserve`, replace `if qty > self._initial[sku]:` with `if qty > self.available(sku):`. Keep the `qty < 1` check first. Change nothing else.
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_oversell_pin.py tests/test_oversell_preservation.py tests/test_cart.py` passes
    - _Requirements: 2.1, 2.2, 2.3_

- [x] 3. Checkpoint — run `uv run --no-project --with pytest --with hypothesis python -m pytest -q`; typecheck: none

- [x] 4. API tests
  - [x]* 4.1 Add API tests for same-cart oversell and 409 body
    - Files: `tests/test_api_oversell.py`
    - Kind: test
    - Size: S
    - Do: Through `shop.api.handle` with stock MUG-01 = 5: one cart posts 3 then 3 → second returns status 409 with body `{"error": "out of stock"}`, GET shows MUG-01 qty 3. Two carts post 3 and 2 → both 200.
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_api_oversell.py` passes
    - _Requirements: 2.3, 3.5_

- [x] 5. Checkpoint — run `uv run --no-project --with pytest --with hypothesis python -m pytest -q`; typecheck: none

## Notes

- `*` = optional, skip for faster MVP
- The exploration pin is red before 2.1 and must be green after it.
- `release` keeps its `max(0, ...)` clamp; that clamp is what holds 3.3.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.2"] },
    { "id": 1, "tasks": ["2.1"] },
    { "id": 2, "tasks": ["4.1"] }
  ],
  "deps": { "2.1": ["1.1", "1.2"], "4.1": ["2.1"] }
}
```

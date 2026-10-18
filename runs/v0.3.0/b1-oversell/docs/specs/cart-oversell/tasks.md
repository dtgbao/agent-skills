# Implementation Plan: cart oversell

## Overview

Pin the bug first: one exploration pin that fails on current code, and preservation pins that pass on current code. Then change the stock check in `Inventory.reserve` to use `available`. An optional Hypothesis test checks Property 1 after the fix. A final checkpoint runs the full suite.

## Tasks

- [x] 1. Pins
  - [x] 1.1 Write exploration pin for two-cart oversell
    - Files: `tests/test_oversell_pin.py`
    - Kind: pin
    - Size: S
    - Expect: red
    - Do: Stock MUG-01 = 5, cart A adds 3. Assert cart B add 3 raises OutOfStock (2.1), available stays 2 (2.2), MUG-01 not in cart B lines (2.3). Through `api.handle`, assert POST /carts/<B>/lines qty 3 returns 409 (2.4).
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_oversell_pin.py`
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 2.1, 2.2, 2.3, 2.4_
  - [x] 1.2 Write preservation pins
    - Files: `tests/test_preservation_pin.py`
    - Kind: pin
    - Size: M
    - Expect: green
    - **Property 2: Preservation**
    - **Validates: Requirements 3.3, 3.5**
    - Do: Example tests for 3.1 (stock 2, reserve 3 → OutOfStock), 3.2 (qty 0 and −1 → ValueError), 3.3 (release more than reserved → available ≤ initial), 3.4 (Cart.remove → available restored), 3.5 (stock 5, A 3, B 2 → available 0), 3.6 (unknown sku → KeyError). Hypothesis test for Property 2, ≥100 examples, tag comment `Feature: cart-oversell, Property 2: Preservation`.
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_preservation_pin.py`
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_

- [x] 2. Fix
  - [x] 2.1 Check reserve against available stock
    - Files: `shop/inventory.py`
    - Kind: code
    - Size: S
    - Do: In `Inventory.reserve`, replace `qty > self._initial[sku]` with `qty > self.available(sku)`. Keep the `qty < 1` check first. Change nothing else.
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_oversell_pin.py tests/test_preservation_pin.py tests/test_cart.py` → all pass
    - _Requirements: 2.1, 2.2, 2.3, 2.4_
  - [x]* 2.2 Property test for fix check
    - Files: `tests/test_inventory_props.py`
    - Kind: test
    - Size: M
    - **Property 1: Fix check**
    - **Validates: Requirements 2.1, 2.2, 2.3**
    - Do: Hypothesis: initial stock 0–50, 1–20 reserves of qty 1–20. Model available; assert OutOfStock iff qty > available before call, available unchanged on raise, available ≥ 0 always. ≥100 examples. Tag comment `Feature: cart-oversell, Property 1: Fix check`.
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_inventory_props.py`
    - _Requirements: 2.1, 2.2, 2.3_

- [x] 3. Checkpoint — run `uv run --no-project --with pytest --with hypothesis python -m pytest -q`; typecheck: none

## Notes

- `*` = optional, skip for faster MVP
- Fix is one line in `shop/inventory.py`. `Cart` and `api` get it through `reserve`.
- Pin 1.1 must fail on current code; pin 1.2 must pass on current code.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.2"] },
    { "id": 1, "tasks": ["2.1"] },
    { "id": 2, "tasks": ["2.2"] }
  ],
  "deps": { "2.1": ["1.1", "1.2"], "2.2": ["2.1"] }
}
```

# Implementation Plan: stock overbooking

## Overview

Write three pin files first, in one wave: one reproduces the overbooking (red on current code), two hold today's behavior for inventory and for cart plus HTTP (green on current code). Then change the guard in `Inventory.reserve` to test against available units. A checkpoint runs the full suite. An optional stateful test then drives random adds and removes across several carts, followed by the final checkpoint.

## Tasks

- [x] 1. Pin tests
  - [x] 1.1 Reproduce overbooking across carts and in one cart
    - Files: `tests/test_overbooking_repro.py`
    - Kind: pin
    - Size: S
    - Expect: red
    - Do: Example `test_two_carts_overbook`: stock MUG-01 = 5, cart A adds 3, cart B adds 3 → expect `OutOfStock`, then `available == 2`. Example `test_one_cart_overbooks`: one cart adds 3 two times → second add raises `OutOfStock`. Hypothesis `test_property_fix_check`: `s` 1–40, `h` 0–`s` reserved first, `q` 1–`s` with `h + q > s` → `OutOfStock` and `available == s - h`; `max_examples=200`; comment `# Feature: stock-overbooking, Property 1: Fix check`.
    - **Property 1: Fix check**
    - **Validates: Requirements 2.1, 2.2, 2.3**
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_overbooking_repro.py` → all 3 tests fail on current code
    - _Requirements: 2.1, 2.2, 2.3_
  - [x] 1.2 Pin inventory behavior that must not change
    - Files: `tests/test_overbooking_keep_inventory.py`
    - Kind: pin
    - Size: M
    - Expect: green
    - Do: Hypothesis tests on `Inventory` only, `max_examples=200` each, comment `# Feature: stock-overbooking, Property 2: Preservation` on each: 3.1 fresh inventory, qty in `s+1`–`s+50` → `OutOfStock`; 3.2 qty in −20–0 → `ValueError`; 3.3 random reserves (catch `OutOfStock`) then releases of 0–200 units → `available ≤ s` after each release; 3.5 split `s` into parts that sum to ≤ `s` → every reserve accepted and `available == s - total`.
    - **Property 2: Preservation**
    - **Validates: Requirements 3.1, 3.2, 3.3, 3.5**
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_overbooking_keep_inventory.py` → all pass on current code
    - _Requirements: 3.1, 3.2, 3.3, 3.5_
  - [x] 1.3 Pin cart and HTTP behavior that must not change
    - Files: `tests/test_overbooking_keep_cart.py`
    - Kind: pin
    - Size: S
    - Expect: green
    - Do: 3.4 Hypothesis: `Cart.add(sku, q)` then `Cart.remove(sku)` → `available` back to its value before the add, `max_examples=200`, comment `# Feature: stock-overbooking, Property 2: Preservation`. 3.6 example: stock 2, cart with MUG-01 qty 1, add qty 3 → `OutOfStock` and `cart.lines == {"MUG-01": 1}`. 3.7 example: via `shop.api.handle`, stock 2, post qty 3 → status 409.
    - **Property 2: Preservation**
    - **Validates: Requirements 3.4, 3.6, 3.7**
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_overbooking_keep_cart.py` → all pass on current code
    - _Requirements: 3.4, 3.6, 3.7_

- [x] 2. Guard fix
  - [x] 2.1 Test reserve against available units
    - Files: `shop/inventory.py`
    - Kind: code
    - Size: S
    - Do: In `Inventory.reserve`, change the guard `qty > self._initial[sku]` to `qty > self.available(sku)`. Leave the `qty < 1` test first and every other line as is.
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_overbooking_repro.py tests/test_overbooking_keep_inventory.py tests/test_overbooking_keep_cart.py tests/test_cart.py` → all pass
    - _Requirements: 2.1, 2.2, 2.3_

- [x] 3. Checkpoint — run `uv run --no-project --with pytest --with hypothesis python -m pytest -q`; typecheck: none

- [x] 4. Stateful test
  - [x]* 4.1 Drive random adds and removes over several carts
    - Files: `tests/test_overbooking_stateful.py`
    - Kind: test
    - Size: M
    - Do: Hypothesis `RuleBasedStateMachine` with 1 inventory (MUG-01 stock 0–10) and 3 carts. Rules: add qty 1–6 to a cart (expect `OutOfStock` exactly when qty > model free units), remove MUG-01 from a cart. Invariant: `available` equals stock minus the sum of cart lines and is never below 0. `max_examples=100`.
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_overbooking_stateful.py` → passes
    - _Requirements: 2.1, 2.2, 3.4_

- [x] 5. Checkpoint — run `uv run --no-project --with pytest --with hypothesis python -m pytest -q`; typecheck: none

## Notes

- `*` = optional, skip for faster MVP
- 1.1 turns green once 2.1 is done; it stays in the suite as a regression test.
- `release` keeps its `max(0, ...)` clamp; 3.3 depends on it.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.2", "1.3"] },
    { "id": 1, "tasks": ["2.1"] },
    { "id": 2, "tasks": ["4.1"] }
  ],
  "deps": { "2.1": ["1.1", "1.2", "1.3"], "4.1": ["2.1"] }
}
```

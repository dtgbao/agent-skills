# Implementation Plan: reserve oversell

## Overview

Pin first, then fix. Wave 0 writes the exploration pin (red on current code: two carts reach available −1) and the preservation pins (green on current code: single over-stock, qty < 1, release cap, remove, exact-fit reserve). Wave 1 changes the one check in `Inventory.reserve` to compare against available units. Checkpoint 3 runs the full suite: all pins green. Optional wave 2 adds an API-level two-cart test.

## Tasks

- [x] 1. Pins
  - [x] 1.1 Pin the two-cart oversell (exploration)
    - Files: `tests/test_oversell_pin.py`
    - Kind: pin
    - Size: M
    - Expect: red
    - Do: Example test of the repro: `Inventory({"MUG-01": 5})`, cart A adds 3, cart B adds 3 → assert `OutOfStock` raised, available == 2, cart B has no MUG-01 line, and `api.handle` POST of qty 3 for cart B returns 409. Add Hypothesis test for Property 1 (≥100 examples): random stock and random reserve sequences across 2–3 carts; any reserve with qty > available raises `OutOfStock` and leaves available unchanged; available never < 0.
    - **Property 1: Fix check**
    - **Validates: Requirements 2.1, 2.2, 2.3, 2.4**
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_oversell_pin.py` fails on current code (available −1, no `OutOfStock`)
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 2.1, 2.2, 2.3, 2.4_
  - [x] 1.2 Pin unchanged reserve and release behavior (preservation)
    - Files: `tests/test_reserve_preserve.py`
    - Kind: pin
    - Size: M
    - Expect: green
    - Do: Example tests: stock 2, add 3 → `OutOfStock` (3.1); reserve qty 0 and −1 → `ValueError` (3.2); release more than reserved → available ≤ initial (3.3); cart with 2 of stock 2 calls `remove` → available 2 (3.4); stock 5, A adds 3, B adds 2 → no raise (3.5), available 0 (3.6). Add Hypothesis test for Property 2 (≥100 examples): random valid sequences (1 ≤ qty ≤ available) of reserve / release / remove; available == stock − held, 0 ≤ available ≤ stock.
    - **Property 2: Preservation**
    - **Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5, 3.6**
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_reserve_preserve.py` passes on current code
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_

- [x] 2. Fix
  - [x] 2.1 Check reserve against available units
    - Files: `shop/inventory.py`
    - Kind: code
    - Size: S
    - Do: In `Inventory.reserve`, replace `if qty > self._initial[sku]:` with `if qty > self.available(sku):`. Keep the `qty < 1` check first. No other change.
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q` all green, including `tests/test_oversell_pin.py`
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 2.1, 2.2, 2.3, 2.4_

- [x] 3. Checkpoint — run `uv run --no-project --with pytest --with hypothesis python -m pytest -q`; typecheck: none

- [x] 4. API coverage
  - [x]* 4.1 Test two carts over the API
    - Files: `tests/test_api_oversell.py`
    - Kind: test
    - Size: S
    - Do: Build ctx with `Inventory({"MUG-01": 5})`; POST /carts twice; POST qty 3 to each cart's /lines. Assert first 200, second 409, GET of second cart shows no MUG-01 line.
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_api_oversell.py` passes
    - _Requirements: 2.4_

- [x] 5. Checkpoint — run `uv run --no-project --with pytest --with hypothesis python -m pytest -q`; typecheck: none

## Notes

- `*` = optional, skip for faster MVP
- Fix is one line. Do not touch `release`, `Cart`, or `api`.
- Exploration pin 1.1 must fail before 2.1 runs and pass after.

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

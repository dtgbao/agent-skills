# Implementation Plan: paginate drops last partial page

## Overview

Pin first, then fix. Exploration pin reproduces the bug (red). Preservation pin locks exact-multiple, guard, empty and out-of-range behavior (green). One-line fix to `total_pages`. Optional boundary tests last.

## Tasks

- [x] 1. Pins
  - [x] 1.1 Exploration pin: last partial page
    - Files: `tests/test_paginate_bug.py`
    - Kind: pin
    - Expect: red
    - Do:
      - Test `total_pages(25, 10) == 3` and `paginate(list(range(25)), 3, 10)` → items 20–24, `total_pages` 3.
      - Hypothesis test for `count % size != 0`, ≥100 examples. Tag `Feature: paginate-last-page, Property 1: Fix check`.
    - **Property 1: Fix check**
    - **Validates: Requirements 2.1, 2.2**
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest tests/test_paginate_bug.py`
    - _Requirements: 1.1, 1.2, 2.1, 2.2_
  - [x] 1.2 Preservation pin: unchanged behavior
    - Files: `tests/test_paginate_preservation.py`
    - Kind: pin
    - Expect: green
    - Do:
      - Examples: 20 items size 10 → 2 pages, page 2 = 10–19; page 0 raises; size 0 raises; empty list → 0 pages; page 4 of 20 items size 10 → empty items.
      - Hypothesis test for exact multiples, guards and out-of-range, ≥100 examples. Tag `Feature: paginate-last-page, Property 2: Preservation`.
    - **Property 2: Preservation**
    - **Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5**
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest tests/test_paginate_preservation.py`
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [x] 2. Fix
  - [x] 2.1 Ceiling division in total_pages
    - Files: `pager/paginate.py`
    - Kind: code
    - Do:
      - Replace `return count // size` with `return -(-count // size)` at line 14.
      - Keep the `size < 1` guard first.
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest`
    - _Requirements: 2.1, 2.2_

- [x] 3. Extra tests
  - [x]* 3.1 Boundary tests
    - Files: `tests/test_paginate_boundary.py`
    - Kind: test
    - Do:
      - Test size 1 (5 items → 5 pages) and size larger than count (3 items, size 10 → 1 page, 3 items).
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest tests/test_paginate_boundary.py`
    - _Requirements: 2.1_

- [x] 4. Checkpoint — run `uv run --no-project --with pytest --with hypothesis python -m pytest`; typecheck: none; ask user on questions

## Notes

- `*` = optional, skip for faster MVP
- Pins are never optional.
- Fix leaf waits on both pins.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.2"] },
    { "id": 1, "tasks": ["2.1"] },
    { "id": 2, "tasks": ["3.1"] }
  ],
  "deps": { "2.1": ["1.1", "1.2"], "3.1": ["2.1"] }
}
```

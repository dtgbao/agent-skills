# Implementation Plan: paginate-last-page-missing

## Overview

Bugfix order. Write the exploration test and the preservation tests first, and run them on the unfixed code. Then fix `total_pages`. Then add the property tests. Final checkpoint reruns every test.

## Tasks

- [ ] 1. Pin defect and existing behavior (unfixed code)
  - [-]* 1.1 Exploration test: red on unfixed code
    - Files: `tests/test_paginate_bug.py`
    - Test A: `paginate(list(range(25)), 3, 10).items == [20, 21, 22, 23, 24]`
    - Test B: `paginate(list(range(25)), 3, 10).total_pages == 3`
    - _Requirements: 1.1, 1.2, 2.1, 2.2_
  - [ ]* 1.2 Preservation tests: green on unfixed code
    - Files: `tests/test_paginate_preservation.py`
    - One test per Unchanged item 3.1–3.8
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8_

- [ ] 2. Checkpoint — run tests, ask user on questions

- [ ] 3. Fix
  - [x] 3.1 Use ceiling division in `total_pages`
    - Files: `pager/paginate.py`
    - `return (count + size - 1) // size`
    - _Requirements: 2.1, 2.2_
  - [ ]* 3.2 Property test: fix check
    - Files: `tests/test_paginate_prop_fix.py`
    - **Property 1: Fix check**
    - **Validates: Requirements 2.1, 2.2**
    - _Requirements: 2.1, 2.2_
  - [ ]* 3.3 Property test: preservation
    - Files: `tests/test_paginate_prop_preserve.py`
    - **Property 2: Preservation**
    - **Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.8**
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.8_

- [ ] 4. Checkpoint — run tests, ask user on questions

## Notes

- `*` = optional, skip for faster MVP
- Tests 1.1 and 1.2 run before 3.1. 1.1 must be red. 1.2 must be green.
- After 3.1, rerun 1.1 and 1.2. Both must be green.
- Run tests: `uv run --no-project --with pytest --with hypothesis python -m pytest`

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.2"] },
    { "id": 1, "tasks": ["3.1"] },
    { "id": 2, "tasks": ["3.2", "3.3"] }
  ]
}
```

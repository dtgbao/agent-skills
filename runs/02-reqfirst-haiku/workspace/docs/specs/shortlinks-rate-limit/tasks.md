# Implementation Plan: shortlinks-rate-limit

## Overview

Add the Redis dependency and the `Clock` protocol first. Then build `RateLimiter` with its property tests. Then wire the limiter into `handle` and add the remaining property tests. Tests follow the code they cover. Property tests share one file, so each runs in its own wave.

## Tasks

- [ ] 1. Setup
  - [ ] 1.1 Add `redis` and `fakeredis` to `pyproject.toml`
    - Dev dependency: `fakeredis` (tests only)
    - _Requirements: 1.7_
  - [ ] 1.2 Add `Clock` protocol, `SystemClock`, `FakeClock` in `shortlinks/clock.py`
    - _Requirements: 1.1, 1.3_

- [ ] 2. RateLimiter
  - [ ] 2.1 Add `Decision` and `RateLimiter` with Lua count script in `shortlinks/ratelimit.py`
    - Fixed 60-second Window, Redis hash `rl:{api_key}`
    - Raises `StorageUnavailable` on error or 100 ms timeout
    - _Requirements: 1.1, 1.2, 1.3, 1.5, 1.6, 1.7, 1.8_
  - [ ]* 2.2 Unit tests for each branch of the count script in `tests/test_ratelimit.py`
    - Use `FakeClock` to test Window reset and Retry-After
    - _Requirements: 1.2, 1.3, 1.5, 1.6_
  - [ ]* 2.3 Property 1 test in `tests/test_properties.py`
    - **Property 1: Limit holds per Window**
    - Hypothesis, 100 examples
    - **Validates: Requirements 1.1, 1.2, 1.6**
  - [ ]* 2.4 Property 2 test in `tests/test_properties.py`
    - **Property 2: Keys are independent**
    - Hypothesis, 100 examples
    - **Validates: Requirements 1.5**
  - [ ]* 2.5 Property 3 test in `tests/test_properties.py`
    - **Property 3: Retry-After is bounded**
    - Hypothesis, 100 examples
    - **Validates: Requirements 1.3**

- [ ] 3. Checkpoint — run tests, ask user on questions

- [ ] 4. API integration
  - [ ] 4.1 Change `handle(request, store, limiter)` in `shortlinks/api.py`; add 429, 503 cases in `tests/test_api.py`; update existing tests for new signature
    - Order: 401 check, then `limiter.check`, then route
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.8_
  - [ ]* 4.2 Property 4 test in `tests/test_properties.py`
    - **Property 4: Refused keys do not count**
    - Hypothesis, 100 examples
    - **Validates: Requirements 1.4**
  - [ ]* 4.3 Property 5 test in `tests/test_properties.py`
    - **Property 5: Storage failure fails closed**
    - Hypothesis, 100 examples
    - **Validates: Requirements 1.8**

- [ ] 5. Checkpoint — run tests, ask user on questions

## Notes

- `*` = optional, skip for faster MVP
- Test leaves are optional but cover every Property in design.md.
- Property tests all write `tests/test_properties.py`, so each runs in its own wave.
- Known gap (design.md, Error Handling): a timed-out count write may still commit.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.2"] },
    { "id": 1, "tasks": ["2.1"] },
    { "id": 2, "tasks": ["2.2", "2.3", "4.1"] },
    { "id": 3, "tasks": ["2.4"] },
    { "id": 4, "tasks": ["2.5"] },
    { "id": 5, "tasks": ["4.2"] },
    { "id": 6, "tasks": ["4.3"] }
  ]
}
```

# Implementation Plan: API key rate limiting

## Overview

Build `RateLimiter` first (constants, `Decision`, clock guard, sliding log, log throttle), then wire it into `handle()`. Each Hypothesis property gets an optional test leaf placed after the code it tests. Unit tests use a `FakeClock`. Work runs in layers: limiter core, API wiring, then integration and property tests.

## Tasks

- [ ] 1. Limiter core
  - [ ] 1.1 Create `shortlinks/ratelimit.py` with `LIMIT`, `WINDOW_SECONDS`, `Decision`, `ClockError`, and `RateLimiter.check` (sliding log, lock, evict, Retry-After clamp)
    - Files: `shortlinks/ratelimit.py`
    - _Requirements: 1.1, 1.2, 1.3, 1.6, 1.7, 2.2_
  - [ ] 1.2 Add the Clock guard to `RateLimiter` (last-seen value, backward clamp, forward-jump `ClockError`)
    - Files: `shortlinks/ratelimit.py`
    - _Requirements: 2.5_
  - [ ] 1.3 Add `_LogThrottle` (one record per 60 s per exception text)
    - Files: `shortlinks/ratelimit.py`
    - _Requirements: 1.8_
  - [ ]* 1.4 Property tests for the limiter: Window count model, key isolation, atomic admission, Retry-After exact, Clock guard, recovery
    - Files: `tests/test_ratelimit.py`
    - **Property 1: Window count model**, **Property 2: Key isolation**, **Property 5: Atomic admission**, **Property 6: Retry-After exact**, **Property 7: Clock guard**, **Property 9: Recovery**
    - **Validates: Requirements 1.1, 1.2, 1.3, 1.6, 2.1, 2.2, 2.4, 2.5, 3.1, 3.2, 3.3**
    - _Requirements: 1.1, 1.2, 1.3, 1.6, 2.1, 2.2, 2.4, 2.5, 3.1, 3.2, 3.3_

- [ ] 2. Checkpoint — run tests, ask user on questions

- [ ] 3. API wiring
  - [ ] 3.1 Wire the limiter into `handle()`: `limiter` argument, 429 Response, `Retry-After` header, fail-open with throttled log
    - Files: `shortlinks/api.py`
    - _Requirements: 1.4, 1.5, 1.8, 1.9, 2.1, 2.3, 2.4_
  - [ ]* 3.2 Integration and property tests for `handle()`: invalid key, every route, fail open, 429 body, per-process scope
    - Files: `tests/test_api.py`
    - **Property 3: Invalid key leaves state unchanged**, **Property 4: Every route counts**, **Property 8: Fail open without state change**
    - **Validates: Requirements 1.4, 1.5, 1.8**
    - _Requirements: 1.4, 1.5, 1.7, 1.8, 1.9, 2.3_

- [ ] 4. Checkpoint — run tests, ask user on questions

## Notes

- `*` = optional, skip for faster MVP
- Python 3.11, Hypothesis ≥100 examples per property. Test files carry `Feature: api-key-rate-limiting, Property N: <title>`.
- Requirement 2.5 (forward-jump rule) can disable the limiter after a 60 s idle gap. See the design risk before task 1.2.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1"] },
    { "id": 1, "tasks": ["1.2"] },
    { "id": 2, "tasks": ["1.3"] },
    { "id": 3, "tasks": ["1.4", "3.1"] },
    { "id": 4, "tasks": ["3.2"] }
  ]
}
```

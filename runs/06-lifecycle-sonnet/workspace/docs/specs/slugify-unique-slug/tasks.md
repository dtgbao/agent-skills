# Implementation Plan: slugify and unique_slug

## Overview

Add dev extras, then implement `slugify`, then `unique_slug` in `textkit/slug.py`. Property tests follow, one file per property, so test leaves run in parallel.

## Tasks

- [ ] 1. Setup
  - [x] 1.1 Declare test dependencies
    - Add `[project.optional-dependencies] dev = ["pytest", "hypothesis"]` to `pyproject.toml`.
    - _Requirements: 1.1_

- [ ] 2. Implementation
  - [x] 2.1 Implement `slugify` in `textkit/slug.py`
    - Pipeline per design. Create the file.
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7_
  - [x] 2.2 Implement `unique_slug` in `textkit/slug.py`
    - Calls `slugify`. Does not mutate `existing`.
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6_

- [ ] 3. Checkpoint — run tests, ask user on questions

- [ ] 4. Property tests
  - [x]* 4.1 Property test: slug format in `tests/test_prop_slug_format.py`
    - **Property 1: Slug format**
    - **Validates: Requirements 1.2, 1.3, 1.4, 1.5, 1.6, 1.7**
    - _Requirements: 1.2, 1.3, 1.4, 1.5, 1.6, 1.7_
  - [x]* 4.2 Property test: idempotence in `tests/test_prop_idempotent.py`
    - **Property 2: Idempotence**
    - **Validates: Requirements 1.2, 1.3, 1.4, 1.5, 1.6, 1.7**
    - _Requirements: 1.2, 1.3, 1.4, 1.5, 1.6, 1.7_
  - [x]* 4.3 Property test: non-ASCII dropped in `tests/test_prop_ascii_only.py`
    - **Property 3: Non-ASCII is dropped**
    - **Validates: Requirements 1.1**
    - _Requirements: 1.1_
  - [x]* 4.4 Property test: smallest free slug in `tests/test_prop_unique_smallest.py`
    - **Property 4: Smallest free slug**
    - **Validates: Requirements 2.1, 2.2, 2.3, 2.5, 2.6**
    - _Requirements: 2.1, 2.2, 2.3, 2.5, 2.6_
  - [x]* 4.5 Property test: no mutation in `tests/test_prop_unique_pure.py`
    - **Property 5: No mutation**
    - **Validates: Requirements 2.4**
    - _Requirements: 2.4_

- [ ] 5. Checkpoint — run tests, ask user on questions

## Notes

- `*` = optional, skip for faster MVP
- Each property file starts with the tag comment `Feature: slugify-unique-slug, Property N: <title>` and uses `max_examples >= 100`.
- Run tests: `uv run --no-project --with pytest --with hypothesis python -m pytest`

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "2.1"] },
    { "id": 1, "tasks": ["2.2", "4.1", "4.2", "4.3"] },
    { "id": 2, "tasks": ["4.4", "4.5"] }
  ]
}
```

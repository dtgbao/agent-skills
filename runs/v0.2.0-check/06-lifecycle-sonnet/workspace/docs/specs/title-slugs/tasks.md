# Implementation Plan: Title slugs

## Overview

Build `slugify`, test it, then build `unique_slug` on top of it and test it. The `unique_slug` code and the `slugify` tests touch different files, so they run in one wave.

## Tasks

- [x] 1. Slugify
  - [x] 1.1 Implement slugify
    - Files: `textkit/slug.py`
    - Kind: code
    - Do: create `slugify(title: str) -> str` and `MAX_LEN = 40`; NFKD, ASCII filter, lowercase, collapse non-alphanumeric runs to `-`, strip `-`, truncate, empty gives "untitled"
    - Verify: `python -c "from textkit.slug import slugify; print(slugify('Café au lait!'))"` prints `cafe-au-lait`
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6_
  - [x]* 1.2 Test slugify
    - Files: `tests/test_slug.py`
    - Kind: test
    - Do: example tests for 1.2 and 1.5; Hypothesis tests for properties 1–3, `max_examples=100`; tag comments `Feature: title-slugs, Property N: <title>`
    - **Property 1: Slug shape**
    - **Validates: Requirements 1.1, 1.3**
    - **Property 2: Slug length**
    - **Validates: Requirements 1.4**
    - **Property 3: Slug idempotence**
    - **Validates: Requirements 1.6**
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest tests/test_slug.py`
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6_

- [x] 2. Checkpoint — run `uv run --no-project --with pytest --with hypothesis python -m pytest`; typecheck: none

- [x] 3. Unique slug
  - [x] 3.1 Implement unique_slug
    - Files: `textkit/unique.py`
    - Kind: code
    - Do: create `unique_slug(title, existing)`; import `slugify` and `MAX_LEN` from `textkit.slug`; try suffix `-2`, `-3`, … with base cut to fit; do not mutate `existing`
    - Verify: `python -c "from textkit.unique import unique_slug; print(unique_slug('Hi', {'hi'}))"` prints `hi-2`
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_
  - [x]* 3.2 Test unique_slug
    - Files: `tests/test_unique_slug.py`
    - Kind: test
    - Do: example tests for 2.5; Hypothesis tests for properties 4–5, `max_examples=100`; tag comments `Feature: title-slugs, Property N: <title>`
    - **Property 4: Uniqueness**
    - **Validates: Requirements 2.1, 2.2, 2.4**
    - **Property 5: Unique slug length**
    - **Validates: Requirements 2.3**
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest tests/test_unique_slug.py`
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

- [x] 4. Checkpoint — run `uv run --no-project --with pytest --with hypothesis python -m pytest`; typecheck: none

## Notes

- `*` = optional, skip for faster MVP
- Typecheck: none configured in this project.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1"] },
    { "id": 1, "tasks": ["1.2", "3.1"] },
    { "id": 2, "tasks": ["3.2"] }
  ],
  "deps": { "1.2": ["1.1"], "3.1": ["1.1"], "3.2": ["3.1"] }
}
```

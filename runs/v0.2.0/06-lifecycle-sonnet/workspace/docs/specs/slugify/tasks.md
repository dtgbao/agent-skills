# Implementation Plan: slugify

## Overview

Code `slugify`, then `unique_slug`, then tests. Test leaves run in parallel.

## Tasks

- [x] 1. Slug functions
  - [x] 1.1 Implement slugify
    - Files: `textkit/slug.py`
    - Kind: code
    - Do:
      - Create `slugify(title: str) -> str` and `MAX_LEN = 40`
      - NFKD, ASCII, lowercase, hyphen runs, cut to 40, strip hyphens, empty → `untitled`
    - Verify: `python -c "from textkit.slug import slugify; assert slugify('Héllo  World') == 'hello-world'"`
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_
  - [x] 1.2 Implement unique_slug
    - Files: `textkit/unique.py`
    - Kind: code
    - Do:
      - Create `unique_slug(title: str, existing: set[str]) -> str` using `slugify`
      - Suffix `-2`, `-3`, ...; trim base so total ≤ 40; never mutate `existing`
    - Verify: `python -c "from textkit.unique import unique_slug; assert unique_slug('a', {'a'}) == 'a-2'"`
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

- [ ] 2. Checkpoint — run `uv run --no-project --with pytest --with hypothesis python -m pytest`; typecheck: none; ask user on questions

- [x] 3. Tests
  - [x] 3.1 Test slugify
    - Files: `tests/test_slugify.py`
    - Kind: test
    - Do:
      - Example tests for accents, `untitled`
      - Hypothesis properties, `max_examples=100`
    - **Property 1: Slug shape**
    - **Validates: Requirements 1.1, 1.3**
    - **Property 2: Slugify idempotent**
    - **Validates: Requirements 1.5**
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest tests/test_slugify.py`
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_
  - [x]* 3.2 Test unique_slug
    - Files: `tests/test_unique_slug.py`
    - Kind: test
    - Do:
      - Example tests for free slug and taken slug
      - Hypothesis properties, `max_examples=100`
    - **Property 3: Unique result**
    - **Validates: Requirements 2.2, 2.3, 2.4**
    - **Property 4: Empty set equals slugify**
    - **Validates: Requirements 2.5**
    - Verify: `uv run --no-project --with pytest --with hypothesis python -m pytest tests/test_unique_slug.py`
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

- [ ] 4. Checkpoint — run `uv run --no-project --with pytest --with hypothesis python -m pytest`; typecheck: none; ask user on questions

## Notes

- `*` = optional, skip for faster MVP

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1"] },
    { "id": 1, "tasks": ["1.2"] },
    { "id": 2, "tasks": ["3.1", "3.2"] }
  ],
  "deps": { "1.2": ["1.1"], "3.1": ["1.1"], "3.2": ["1.1", "1.2"] }
}
```

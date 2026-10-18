# Design Document: paginate-last-page-missing

## Overview

`total_pages` uses floor division, so a partial last page is not counted. `paginate` then treats the last page as out of range and returns an empty page. The fix changes `total_pages` to ceiling division. `paginate` needs no change.

**Key design decisions:**
- Fix in `total_pages` only: it is the single source of the page count (`pager/paginate.py:14`). `paginate` already slices the last partial page correctly (`pager/paginate.py:24-25`).
- Integer ceiling `(count + size - 1) // size`: no float, no `math` import, exact for all ints.

## Root Cause

`total_pages` returns `count // size` (floor). Evidence:

- `pager/paginate.py:14`: `return count // size`. 25 // 10 = 2, so page count is one short when `count % size != 0`. Explains Current 1.2.
- `pager/paginate.py:21-23`: `pages = total_pages(...)`; `if page > pages: return Page(items=[], ...)`. Page 3 > 2, so the empty page is returned. Explains Current 1.1.

Bug condition: `size >= 1 and len(items) % size != 0`.

## Fix

Component: `total_pages` (`pager/paginate.py`).

```python
def total_pages(count: int, size: int) -> int
```

Change: `return count // size` → `return (count + size - 1) // size`.

Constraints: keep the `size < 1` ValueError (`:12-13`) and the `page < 1` ValueError (`:19-20`). Keep `Page` fields and `paginate` signature unchanged.

_Requirements: 2.1, 2.2, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8_

### Call-tree change

```diff
 paginate(items, page, size)            # pager/paginate.py:17
   page < 1 -> ValueError               # :19
   total_pages(len(items), size)        # :21
     size < 1 -> ValueError             # :12
-    return count // size               # :14
+    return (count + size - 1) // size  # :14
   page > pages -> Page(items=[])       # :22  unchanged
   items[start:start + size]            # :24-25 unchanged
```

## Validation Properties

- Property 1 — Fix check: *for any* `items`, `size >= 1`, where `len(items) % size != 0`, and any `page` in `1..ceil(len/size)`, `paginate` SHALL return `total_pages == ceil(len/size)` and `items == items[(page-1)*size : page*size]`.
  **Validates: Requirements 2.1, 2.2**
- Property 2 — Preservation: *for any* `items`, `size >= 1`, `page >= 1`, where `len(items) % size == 0`, `paginate` SHALL return `total_pages == len(items) // size`. *For any* `page < 1` or `size < 1`, `paginate` SHALL raise `ValueError`. *For any* `page > total_pages`, `paginate` SHALL return `items == []`.
  **Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.8**

## Regression Strategy

Example tests pin each Unchanged item on the unfixed code (green before the fix, green after). The exploration test pins the defect (red before, green after). Item 3.7 (25 items, page 2) pins the full page next to the partial page.

## Testing Strategy

- Exploration test: `tests/test_paginate_bug.py`, one test per Expected item 2.1 and 2.2.
- Preservation tests: `tests/test_paginate_preservation.py`, one test per Unchanged item 3.1–3.8.
- Property 1 and Property 2: Hypothesis, `max_examples=100`. Tag comment `Feature: paginate-last-page-missing, Property N: <title>`.
- Run: `uv run --no-project --with pytest --with hypothesis python -m pytest` from the project root.

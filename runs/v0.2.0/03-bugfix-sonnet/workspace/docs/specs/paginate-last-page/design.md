# Design Document: paginate drops last partial page

## Root Cause

`total_pages` floors the page count: `count // size` (`pager/paginate.py:14`). 25 items, size 10 → 2, not 3. `paginate` trusts that total and returns an empty page for any page above it (`pager/paginate.py:22-23`). Explains 1.1 (floor result) and 1.2 (page 3 > 2 → empty). Exact multiples hide the defect: `count // size` equals the ceiling.

## Fix

Change `total_pages` to ceiling division. One component changes: `total_pages` in `pager/paginate.py`.

- Constraint: the `size < 1` guard (line 12-13) stays first, so size 0 still raises, not `ZeroDivisionError`.
- Constraint: `count == 0` stays 0.
- `paginate` needs no change. Its page guard (line 19-20) and out-of-range branch (line 22-23) stay as they are.

### Call-tree Change

```diff
 paginate (pager/paginate.py:17)
   guard page < 1 → ValueError
   total_pages (pager/paginate.py:11)
     guard size < 1 → ValueError
-    return count // size
+    return -(-count // size)
   if page > pages → empty Page
   slice items[start:start + size]
```

## Correctness Properties

### Property 1: Fix check

*For any* `count >= 1`, `size >= 1` where `count % size != 0`, `total_pages(count, size)` SHALL equal `count // size + 1`, and the last page of `paginate(range(count), count // size + 1, size)` SHALL hold the `count % size` trailing items.

**Validates: Requirements 2.1, 2.2**

### Property 2: Preservation

*For any* `count >= 0`, `size >= 1` where `count % size == 0`, `total_pages(count, size)` SHALL equal `count // size`. For any `page < 1` or `size < 1`, `paginate` SHALL raise `ValueError`. For any page above `total_pages`, `paginate` SHALL return an empty items list.

**Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5**

## Regression Strategy

Pins live in two new files. Hypothesis tags follow `shared/correctness.md`.

- Exploration pin (`tests/test_paginate_bug.py`, red before fix): 25 items size 10 → `total_pages` 3 (2.1); page 3 → items 20–24 (2.2); Property 1.
- Preservation pin (`tests/test_paginate_preservation.py`, green before fix):
  - 20 items size 10: `total_pages` 2, page 2 = 10–19 (3.1)
  - page 0 raises `ValueError` (3.2)
  - size 0 raises `ValueError` (3.3)
  - empty list → `total_pages` 0 (3.4)
  - page 4 of 20 items size 10 → empty items (3.5)
  - Property 2.

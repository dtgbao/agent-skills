# Bugfix Requirements Document

## Introduction

`paginate` drops the last partial page. When the item count is not a multiple of the page size, `total_pages` rounds down. The last page then falls past `total_pages` and comes back empty. Callers lose the trailing items.

Repro:
1. Start state: `items = list(range(25))`.
2. Input: `paginate(items, 3, 10)`.
3. Observed: `Page(items=[], page=3, total_pages=2)`.
4. Expected: `Page(items=[20, 21, 22, 23, 24], page=3, total_pages=3)`.

## Bug Analysis

### Current Behavior (Defect)

1.1 WHEN `paginate` is called with 25 items, page 3, size 10 THEN the system returns `items == []`
1.2 WHEN `paginate` is called with 25 items, page 3, size 10 THEN the system returns `total_pages == 2`

### Expected Behavior (Correct)

2.1 WHEN `paginate` is called with 25 items, page 3, size 10 THE SYSTEM SHALL return `items == [20, 21, 22, 23, 24]`
2.2 WHEN `paginate` is called with 25 items, page 3, size 10 THE SYSTEM SHALL return `total_pages == 3`

### Unchanged Behavior (Regression Prevention)

3.1 WHEN `paginate` is called with 20 items, page 2, size 10 THE SYSTEM SHALL CONTINUE TO return `total_pages == 2`
3.2 WHEN `paginate` is called with 20 items, page 2, size 10 THE SYSTEM SHALL CONTINUE TO return `items == [10, ..., 19]`
3.3 WHEN `paginate` is called with page 0 THE SYSTEM SHALL CONTINUE TO raise `ValueError`
3.4 WHEN `paginate` is called with size 0 THE SYSTEM SHALL CONTINUE TO raise `ValueError`
3.5 WHEN `paginate` is called with an empty list, page 1, size 10 THE SYSTEM SHALL CONTINUE TO return `total_pages == 0`
3.6 WHEN `paginate` is called with an empty list, page 1, size 10 THE SYSTEM SHALL CONTINUE TO return `items == []`
3.7 WHEN `paginate` is called with 25 items, page 2, size 10 THE SYSTEM SHALL CONTINUE TO return `items == [10, ..., 19]`
3.8 WHEN `paginate` is called with a page number above `total_pages` (25 items, page 4, size 10) THE SYSTEM SHALL CONTINUE TO return `items == []`

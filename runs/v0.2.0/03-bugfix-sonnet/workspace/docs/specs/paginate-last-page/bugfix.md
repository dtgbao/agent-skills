# Bugfix Requirements Document

## Introduction

`paginate` drops the last partial page. `total_pages` uses floor division, so a count that is not a multiple of the page size loses one page. Page numbers above the wrong total return an empty page, so trailing items are unreachable.

Repro: `paginate(list(range(25)), 3, 10)`.

- Starting state: 25 items, page size 10.
- Observed: `Page(items=[], page=3, total_pages=2)`.
- Expected: `Page(items=[20, 21, 22, 23, 24], page=3, total_pages=3)`.

## Bug Analysis

### Current Behavior (Defect)

1.1 WHEN `total_pages` is called with 25 items and size 10 THEN the system returns 2
1.2 WHEN `paginate` is called with 25 items, page 3, size 10 THEN the system returns an empty page

### Expected Behavior (Correct)

2.1 WHEN `total_pages` is called with 25 items and size 10 THE SYSTEM SHALL return 3
2.2 WHEN `paginate` is called with 25 items, page 3, size 10 THE SYSTEM SHALL return items 20–24 with `total_pages` 3

### Unchanged Behavior (Regression Prevention)

3.1 WHEN the item count is an exact multiple of size (20 items, size 10) THE SYSTEM SHALL CONTINUE TO return `total_pages` 2 and items 10–19 for page 2
3.2 WHEN `paginate` is called with page below 1 THE SYSTEM SHALL CONTINUE TO raise `ValueError`
3.3 WHEN `paginate` or `total_pages` is called with size below 1 THE SYSTEM SHALL CONTINUE TO raise `ValueError`
3.4 WHEN the item list is empty THE SYSTEM SHALL CONTINUE TO return `total_pages` 0
3.5 WHEN the page number is above `total_pages` THE SYSTEM SHALL CONTINUE TO return an empty items list

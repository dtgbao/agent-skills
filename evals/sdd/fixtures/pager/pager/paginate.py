from dataclasses import dataclass


@dataclass(frozen=True)
class Page:
    items: list
    page: int
    total_pages: int


def total_pages(count: int, size: int) -> int:
    if size < 1:
        raise ValueError("size must be >= 1")
    return count // size


def paginate(items: list, page: int, size: int) -> Page:
    """Return 1-based page `page` of `items`."""
    if page < 1:
        raise ValueError("page must be >= 1")
    pages = total_pages(len(items), size)
    if page > pages:
        return Page(items=[], page=page, total_pages=pages)
    start = (page - 1) * size
    return Page(items=items[start:start + size], page=page, total_pages=pages)

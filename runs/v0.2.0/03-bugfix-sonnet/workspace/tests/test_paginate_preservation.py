import pytest
from hypothesis import given, settings, strategies as st

from pager.paginate import paginate, total_pages


def test_exact_multiple():
    p = paginate(list(range(20)), 2, 10)
    assert total_pages(20, 10) == 2
    assert p.total_pages == 2
    assert p.items == list(range(10, 20))


def test_page_zero_raises():
    with pytest.raises(ValueError):
        paginate(list(range(20)), 0, 10)


def test_size_zero_raises():
    with pytest.raises(ValueError):
        paginate(list(range(20)), 1, 0)
    with pytest.raises(ValueError):
        total_pages(20, 0)


def test_empty_list_zero_pages():
    assert total_pages(0, 10) == 0
    assert paginate([], 1, 10).total_pages == 0


def test_page_beyond_total_is_empty():
    assert paginate(list(range(20)), 4, 10).items == []


# Feature: paginate-last-page, Property 2: Preservation
@settings(max_examples=100)
@given(
    count=st.integers(min_value=0, max_value=1000),
    size=st.integers(min_value=1, max_value=100),
    extra=st.integers(min_value=1, max_value=50),
    bad_page=st.integers(min_value=-1000, max_value=0),
    bad_size=st.integers(min_value=-1000, max_value=0),
)
def test_preservation(count, size, extra, bad_page, bad_size):
    items = list(range(count))
    # 3.1, 3.4: exact multiples keep floor total; empty list gives 0
    if count % size == 0:
        pages = count // size
        assert total_pages(count, size) == pages
        for n in range(1, pages + 1):
            p = paginate(items, n, size)
            assert p.total_pages == pages
            assert p.items == items[(n - 1) * size:n * size]
        # 3.5: page above total_pages returns empty items
        assert paginate(items, pages + extra, size).items == []
    # 3.5: page above the true page count (fix-independent) returns empty items
    true_pages = -(-count // size)
    assert paginate(items, true_pages + extra, size).items == []
    # 3.2: page below 1 raises
    with pytest.raises(ValueError):
        paginate(items, bad_page, size)
    # 3.3: size below 1 raises
    with pytest.raises(ValueError):
        paginate(items, 1, bad_size)
    with pytest.raises(ValueError):
        total_pages(count, bad_size)

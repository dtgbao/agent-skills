import pytest
from pager.paginate import paginate


def test_exact_multiple():
    p = paginate(list(range(20)), 2, 10)
    assert p.items == list(range(10, 20)) and p.total_pages == 2


def test_page_zero_raises():
    with pytest.raises(ValueError):
        paginate([1, 2], 0, 10)

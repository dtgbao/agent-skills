from hypothesis import given, settings, strategies as st

from pager.paginate import paginate, total_pages


def test_total_pages_partial_last_page():
    assert total_pages(25, 10) == 3


def test_paginate_last_partial_page():
    p = paginate(list(range(25)), 3, 10)
    assert p.items == [20, 21, 22, 23, 24]
    assert p.total_pages == 3


# Feature: paginate-last-page, Property 1: Fix check
@settings(max_examples=100)
@given(count=st.integers(min_value=1, max_value=1000), size=st.integers(min_value=1, max_value=100))
def test_fix_check(count, size):
    if count % size == 0:
        return
    last = count // size + 1
    assert total_pages(count, size) == last
    p = paginate(list(range(count)), last, size)
    assert p.total_pages == last
    assert p.items == list(range(count))[-(count % size):]

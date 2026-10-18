from pager.paginate import paginate, total_pages


def test_size_one_gives_one_page_per_item():
    items = list(range(5))
    assert total_pages(5, 1) == 5
    for n in range(1, 6):
        p = paginate(items, n, 1)
        assert p.total_pages == 5
        assert p.items == [n - 1]


def test_size_larger_than_count_gives_single_page():
    items = [0, 1, 2]
    assert total_pages(3, 10) == 1
    p = paginate(items, 1, 10)
    assert p.total_pages == 1
    assert p.items == [0, 1, 2]

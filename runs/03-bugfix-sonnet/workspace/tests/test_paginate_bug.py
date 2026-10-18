from pager.paginate import paginate


def test_last_partial_page_items():
    # Requirements 2.1 (defect 1.1)
    assert paginate(list(range(25)), 3, 10).items == [20, 21, 22, 23, 24]


def test_last_partial_page_total_pages():
    # Requirements 2.2 (defect 1.2)
    assert paginate(list(range(25)), 3, 10).total_pages == 3

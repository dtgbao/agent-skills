"""Hidden acceptance suite for f3 (bulk pricing, owner answers in ../f3-answers.md). The builder never sees it."""
import pytest
from hypothesis import given, settings, strategies as st

from shop.api import handle
from shop.cart import Cart
from shop.inventory import Inventory

PRICE = {"TEA-01": 450, "MUG-01": 1200, "KET-01": 3999}


def new_cart():
    return Cart(Inventory({"TEA-01": 100, "MUG-01": 100, "KET-01": 100}))


def subtotal(*lines):
    c = new_cart()
    for sku, qty in lines:
        c.add(sku, qty)
    return c.subtotal_cents()


@pytest.mark.parametrize("qty,want", [(9, 4050), (10, 4050), (19, 7695), (20, 7650), (40, 15300)])
def test_tiers_tea(qty, want):
    assert subtotal(("TEA-01", qty)) == want


def test_lines_count_separately():
    assert subtotal(("MUG-01", 10), ("TEA-01", 5)) == 10800 + 2250


def test_whole_cart_does_not_count():
    assert subtotal(("TEA-01", 5), ("MUG-01", 5)) == 2250 + 6000


def test_line_rounds_down_once():
    assert subtotal(("KET-01", 13)) == 46788


def test_line_rounds_down_top_tier():
    assert subtotal(("KET-01", 21)) == 71382


def test_units_add_up_across_adds():
    c = new_cart()
    c.add("TEA-01", 6)
    c.add("TEA-01", 4)
    assert c.subtotal_cents() == 4050


def test_api_lines_subtotal():
    ctx = {"carts": {}, "inventory": Inventory({"TEA-01": 100})}
    cid = handle({"method": "POST", "path": "/carts", "body": {}}, ctx)["body"]["cart_id"]
    r = handle({"method": "POST", "path": f"/carts/{cid}/lines", "body": {"sku": "TEA-01", "qty": 20}}, ctx)
    assert r["body"]["subtotal_cents"] == 7650
    g = handle({"method": "GET", "path": f"/carts/{cid}", "body": {}}, ctx)
    assert g["body"]["subtotal_cents"] == 7650


@settings(max_examples=100, deadline=None)
@given(st.integers(1, 40), st.integers(1, 40), st.integers(1, 40))
def test_bulk_property(tea, mug, ket):
    def line(sku, q):
        pct = 15 if q >= 20 else 10 if q >= 10 else 0
        return PRICE[sku] * q * (100 - pct) // 100
    want = line("TEA-01", tea) + line("MUG-01", mug) + line("KET-01", ket)
    assert subtotal(("TEA-01", tea), ("MUG-01", mug), ("KET-01", ket)) == want

"""Hidden acceptance suite for f2 (checkout quote: shipping + tax modules + API). The builder never sees it."""
import pytest
from hypothesis import given, settings, strategies as st

from shop.api import handle
from shop.inventory import Inventory
from shop.shipping import shipping_cents
from shop.tax import tax_cents


@pytest.mark.parametrize("sub,express,want", [(4999, False, 499), (5000, False, 0), (1, False, 499),
                                               (4999, True, 1999), (5000, True, 1500), (100000, True, 1500)])
def test_shipping(sub, express, want):
    assert shipping_cents(sub, express) == want


@pytest.mark.parametrize("sub,region,want", [(10000, "CA", 725), (450, "CA", 32), (999, "NY", 39),
                                              (7998, "NY", 319), (12345, "OR", 0)])
def test_tax(sub, region, want):
    assert tax_cents(sub, region) == want


def test_tax_unknown_region():
    with pytest.raises(ValueError):
        tax_cents(1000, "TX")


def ctx():
    return {"carts": {}, "inventory": Inventory({"TEA-01": 100, "MUG-01": 100, "KET-01": 100})}


def call(c, method, path, body=None):
    return handle({"method": method, "path": path, "body": body or {}}, c)


def cart(c, *lines):
    cid = call(c, "POST", "/carts")["body"]["cart_id"]
    for sku, qty in lines:
        call(c, "POST", f"/carts/{cid}/lines", {"sku": sku, "qty": qty})
    return cid


def quote(c, cid, **body):
    return call(c, "POST", f"/carts/{cid}/quote", body)


def test_quote_standard():
    c = ctx()
    r = quote(c, cart(c, ("TEA-01", 2)), region="CA")
    assert r["status"] == 200
    b = r["body"]
    assert (b["subtotal_cents"], b["shipping_cents"], b["tax_cents"], b["total_cents"]) == (900, 499, 65, 1464)


def test_quote_express_free_standard():
    c = ctx()
    b = quote(c, cart(c, ("KET-01", 2)), region="NY", express=True)["body"]
    assert (b["subtotal_cents"], b["shipping_cents"], b["tax_cents"], b["total_cents"]) == (7998, 1500, 319, 9817)


def test_quote_express_defaults_false():
    c = ctx()
    assert quote(c, cart(c, ("MUG-01", 1)), region="OR")["body"]["shipping_cents"] == 499


def test_quote_unknown_region():
    c = ctx()
    assert quote(c, cart(c, ("MUG-01", 1)), region="TX")["status"] == 400


def test_quote_empty_cart():
    c = ctx()
    assert quote(c, cart(c), region="CA")["status"] == 400


def test_quote_unknown_cart():
    assert quote(ctx(), "999", region="CA")["status"] == 404


@settings(max_examples=100, deadline=None)
@given(st.integers(0, 15), st.integers(0, 15), st.integers(1, 5), st.sampled_from(["CA", "NY", "OR"]), st.booleans())
def test_quote_total_property(tea, mug, ket, region, express):
    c = ctx()
    b = quote(c, cart(c, ("TEA-01", tea), ("MUG-01", mug), ("KET-01", ket)) if tea and mug
              else cart(c, ("KET-01", ket)), region=region, express=express)["body"]
    sub = b["subtotal_cents"]
    rate = {"CA": 725, "NY": 400, "OR": 0}[region]
    ship = (0 if sub >= 5000 else 499) + (1500 if express else 0)
    assert (b["shipping_cents"], b["tax_cents"]) == (ship, sub * rate // 10000)
    assert b["total_cents"] == sub + ship + sub * rate // 10000

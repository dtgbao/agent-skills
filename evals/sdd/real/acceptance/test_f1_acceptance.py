"""Hidden acceptance suite for f1 (final state: percent 1-50). The builder never sees it.

Run from the project root:
  uv run --no-project --with pytest --with hypothesis python -m pytest -q -p no:cacheprovider <this file>
"""
from datetime import date

import pytest
from hypothesis import given, settings, strategies as st

from shop.api import handle
from shop.inventory import Inventory

TODAY = date(2026, 10, 19)


def ctx():
    return {"carts": {}, "inventory": Inventory({"TEA-01": 100, "MUG-01": 100, "KET-01": 100}),
            "codes": {}, "today": TODAY}


def call(c, method, path, body=None):
    return handle({"method": method, "path": path, "body": body or {}}, c)


def cart(c, *lines):
    cid = call(c, "POST", "/carts")["body"]["cart_id"]
    for sku, qty in lines:
        assert call(c, "POST", f"/carts/{cid}/lines", {"sku": sku, "qty": qty})["status"] == 200
    return cid


def code(c, **body):
    return call(c, "POST", "/codes", body)["status"]


def apply(c, cid, text):
    return call(c, "POST", f"/carts/{cid}/code", {"code": text})


@pytest.mark.parametrize("body", [{"percent": 10}, {"percent": 1}, {"percent": 50}, {"amount_cents": 500},
                                  {"amount_cents": 1, "min_subtotal_cents": 0, "expires": "2026-12-31"}])
def test_create_valid(body):
    assert code(ctx(), code="X", **body) == 201


@pytest.mark.parametrize("body", [{"percent": 0}, {"percent": 51}, {"percent": 90}, {"percent": 91},
                                  {"amount_cents": 0}, {"percent": 10, "amount_cents": 100}, {},
                                  {"percent": 10, "min_subtotal_cents": -1}])
def test_create_invalid(body):
    assert code(ctx(), code="X", **body) == 400


def test_percent_discount():
    c = ctx()
    code(c, code="SAVE10", percent=10)
    r = apply(c, cart(c, ("TEA-01", 2)), "SAVE10")
    assert r["status"] == 200
    assert (r["body"]["subtotal_cents"], r["body"]["discount_cents"], r["body"]["total_cents"]) == (900, 90, 810)


def test_percent_rounds_down():
    c = ctx()
    code(c, code="P15", percent=15)
    assert apply(c, cart(c, ("TEA-01", 1)), "P15")["body"]["discount_cents"] == 67


def test_fixed_discount():
    c = ctx()
    code(c, code="F5", amount_cents=500)
    r = apply(c, cart(c, ("MUG-01", 1)), "F5")
    assert (r["body"]["discount_cents"], r["body"]["total_cents"]) == (500, 700)


def test_fixed_never_above_subtotal():
    c = ctx()
    code(c, code="BIG", amount_cents=5000)
    r = apply(c, cart(c, ("TEA-01", 2)), "BIG")
    assert (r["body"]["discount_cents"], r["body"]["total_cents"]) == (900, 0)


def test_unknown_code():
    c = ctx()
    assert apply(c, cart(c, ("TEA-01", 1)), "NOPE")["status"] == 400


def test_expired_code():
    c = ctx()
    code(c, code="OLD", percent=10, expires="2026-10-18")
    assert apply(c, cart(c, ("TEA-01", 1)), "OLD")["status"] == 400


def test_code_valid_on_expiry_day():
    c = ctx()
    code(c, code="TODAY", percent=10, expires="2026-10-19")
    assert apply(c, cart(c, ("TEA-01", 1)), "TODAY")["status"] == 200


def test_minimum_not_met():
    c = ctx()
    code(c, code="MIN", percent=10, min_subtotal_cents=1000)
    assert apply(c, cart(c, ("TEA-01", 2)), "MIN")["status"] == 400


def test_minimum_met_exactly():
    c = ctx()
    code(c, code="MIN", percent=10, min_subtotal_cents=900)
    assert apply(c, cart(c, ("TEA-01", 2)), "MIN")["status"] == 200


def test_second_code_conflict():
    c = ctx()
    code(c, code="A", percent=10)
    code(c, code="B", percent=20)
    cid = cart(c, ("TEA-01", 2))
    assert apply(c, cid, "A")["status"] == 200
    assert apply(c, cid, "B")["status"] == 409


def test_get_cart_shows_discount():
    c = ctx()
    code(c, code="SAVE10", percent=10)
    cid = cart(c, ("TEA-01", 2))
    apply(c, cid, "SAVE10")
    body = call(c, "GET", f"/carts/{cid}")["body"]
    assert (body["discount_cents"], body["total_cents"]) == (90, 810)


def test_get_cart_without_code():
    c = ctx()
    body = call(c, "GET", f"/carts/{cart(c, ('MUG-01', 1))}")["body"]
    assert (body["discount_cents"], body["total_cents"]) == (0, 1200)


def test_apply_to_unknown_cart():
    c = ctx()
    code(c, code="A", percent=10)
    assert apply(c, "999", "A")["status"] == 404


@settings(max_examples=100, deadline=None)
@given(st.integers(1, 20), st.integers(1, 20), st.integers(1, 50))
def test_percent_property(tea, mug, pct):
    c = ctx()
    code(c, code="P", percent=pct)
    r = apply(c, cart(c, ("TEA-01", tea), ("MUG-01", mug)), "P")
    sub = 450 * tea + 1200 * mug
    assert (r["body"]["discount_cents"], r["body"]["total_cents"]) == (sub * pct // 100, sub - sub * pct // 100)

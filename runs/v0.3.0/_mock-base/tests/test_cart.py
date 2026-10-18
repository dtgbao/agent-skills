import pytest
from shop.cart import Cart
from shop.inventory import Inventory, OutOfStock


def test_subtotal():
    cart = Cart(Inventory({"TEA-01": 10, "MUG-01": 2}))
    cart.add("TEA-01", 2)
    cart.add("MUG-01", 1)
    assert cart.subtotal_cents() == 2 * 450 + 1200


def test_single_reserve_over_stock_fails():
    with pytest.raises(OutOfStock):
        Cart(Inventory({"MUG-01": 2})).add("MUG-01", 3)


def test_release_on_remove():
    inv = Inventory({"MUG-01": 2})
    cart = Cart(inv)
    cart.add("MUG-01", 2)
    cart.remove("MUG-01")
    assert inv.available("MUG-01") == 2

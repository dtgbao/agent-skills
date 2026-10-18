from shop.catalog import CATALOG
from shop.inventory import Inventory


class Cart:
    def __init__(self, inventory: Inventory) -> None:
        self.inventory = inventory
        self.lines: dict[str, int] = {}

    def add(self, sku: str, qty: int) -> None:
        if sku not in CATALOG:
            raise KeyError(sku)
        self.inventory.reserve(sku, qty)
        self.lines[sku] = self.lines.get(sku, 0) + qty

    def remove(self, sku: str) -> None:
        qty = self.lines.pop(sku, 0)
        if qty:
            self.inventory.release(sku, qty)

    def subtotal_cents(self) -> int:
        return sum(CATALOG[sku].price_cents * qty for sku, qty in self.lines.items())

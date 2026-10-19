class OutOfStock(Exception):
    pass


class Inventory:
    """Stock per sku. reserve() holds units for a cart until release()."""

    def __init__(self, stock: dict[str, int]) -> None:
        self._initial = dict(stock)
        self._reserved: dict[str, int] = {sku: 0 for sku in stock}

    def available(self, sku: str) -> int:
        return self._initial[sku] - self._reserved[sku]

    def reserve(self, sku: str, qty: int) -> None:
        if qty < 1:
            raise ValueError("qty must be >= 1")
        if qty > self._initial[sku]:
            raise OutOfStock(sku)
        self._reserved[sku] += qty

    def release(self, sku: str, qty: int) -> None:
        self._reserved[sku] = max(0, self._reserved[sku] - qty)

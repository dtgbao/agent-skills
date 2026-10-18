from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    sku: str
    name: str
    price_cents: int


CATALOG = {
    "TEA-01": Product("TEA-01", "Green tea", 450),
    "MUG-01": Product("MUG-01", "Mug", 1200),
    "KET-01": Product("KET-01", "Kettle", 3999),
}

Add a checkout quote to carts. Put the shipping rules in a new module `shop/shipping.py` with `shipping_cents(subtotal_cents: int, express: bool) -> int`, and the tax rules in a new module `shop/tax.py` with `tax_cents(subtotal_cents: int, region: str) -> int`. Then add the API route in `shop/api.py`.

- Shipping: 0 when the subtotal is 5000 cents or more, else 499. Express adds 1500 to that value (also when standard shipping is 0).
- Tax: on the subtotal only, not on shipping. Rates: `"CA"` 7.25 %, `"NY"` 4 %, `"OR"` 0 %. Tax = subtotal × rate, rounded down to whole cents. For another region, `tax_cents` raises `ValueError`.
- API: `POST /carts/<id>/quote` with body `{"region": <text>, "express": <bool, default false>}`. Success: status 200, body with `subtotal_cents`, `shipping_cents`, `tax_cents` and `total_cents` (subtotal + shipping + tax). Unknown region: status 400. Empty cart (subtotal 0): status 400. Unknown cart: status 404.

# mockshop

Tiny shop core used to evaluate the `sdd` plugin. Pure Python, no framework.

- `shop/catalog.py` — products (sku → name, unit price in cents)
- `shop/inventory.py` — stock per sku, reservations
- `shop/cart.py` — cart lines, subtotal in cents
- `shop/api.py` — `handle(request, ctx)`: dict in, dict out

Test: `uv run --no-project --with pytest --with hypothesis python -m pytest -q`
Typecheck: none.

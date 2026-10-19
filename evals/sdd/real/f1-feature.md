Add discount codes to carts, through the API in `shop/api.py` (`handle(request, ctx)`). `ctx` also holds `"codes"` (a dict, the code store) and `"today"` (a `datetime.date`).

- Create a code: `POST /codes` with body `{"code": <text>, "percent": <int>}` or `{"code": <text>, "amount_cents": <int>}`, plus optional `"min_subtotal_cents"` (int, default 0) and `"expires"` (`"YYYY-MM-DD"`). Exactly one of `percent` and `amount_cents`. `percent` is 1–90. `amount_cents` is 1 or more. `min_subtotal_cents` is 0 or more. Valid: status 201. Invalid: status 400.
- Apply a code: `POST /carts/<id>/code` with body `{"code": <text>}`. Success: status 200, body with `subtotal_cents`, `discount_cents` and `total_cents`. Status 400 when the code is unknown, when it is expired (`today` is after `expires`), or when the subtotal is below `min_subtotal_cents`. A cart holds at most one code: a second apply gives status 409.
- `GET /carts/<id>` also returns `discount_cents` and `total_cents`.
- A percent code takes `subtotal * percent // 100` off. A fixed code takes `amount_cents` off, but never more than the subtotal.

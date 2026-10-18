# Design Document: cart oversell

## Root Cause

`Inventory.reserve` compares the request with the initial stock, not with the units still available (`shop/inventory.py:17`):

```python
if qty > self._initial[sku]:
    raise OutOfStock(sku)
self._reserved[sku] += qty
```

- 1.1: cart B asks for 3. 3 ≤ 5 (initial), so no error. The 3 units cart A holds are not counted.
- 1.2: `_reserved` grows to 6. `available()` returns `5 - 6 = -1` (`shop/inventory.py:11`).
- 1.3: `Cart.add` (`shop/cart.py:13`) gets no error, so `handle` returns 200 (`shop/api.py:25`). The 409 branch (`shop/api.py:23`) never runs.

Neighbor paths that share the faulty check: two adds of the same sku from one cart (`shop/cart.py:13`), and every API add (`shop/api.py:17`).

## Fix

Change one component: `Inventory.reserve` in `shop/inventory.py`.

- Compare `qty` with `self.available(sku)`, not `self._initial[sku]`.
- Keep the `qty < 1` check first, so `ValueError` wins over `OutOfStock` (3.2).
- Raise before any state change, so a refused reserve leaves `_reserved` as it was (2.2).
- `release`, `Cart`, and `handle` stay unchanged. `Cart.add` already calls `reserve` before it updates `lines`, so a refused add leaves the cart lines as they were. `handle` already maps `OutOfStock` to 409 (2.3).

Since `available = initial - reserved`, the new check is stricter than the old one: a single reserve above the initial stock still fails (3.1).

### Call-tree Change

```diff
 handle POST /carts/<id>/lines          (shop/api.py:17)
   Cart.add(sku, qty)                   (shop/cart.py:10)
     Inventory.reserve(sku, qty)        (shop/inventory.py:14)
       if qty < 1 -> ValueError
-      if qty > _initial[sku] -> OutOfStock
+      if qty > available(sku) -> OutOfStock
       _reserved[sku] += qty
     lines[sku] += qty
-  -> 200
+  OutOfStock -> 409                    (when cumulative qty > stock)
```

## Correctness Properties

Framework: Hypothesis (Python, `pyproject.toml`).

### Property 1: Fix check

*For any* initial stock `s` in 1–50 and a first reserve `a` in 1–`s` by cart A, a second reserve `b` in 1–`s` by cart B with `a + b > s`, the Inventory SHALL raise `OutOfStock` for `b`, keep available at `s - a`, and the API SHALL return status 409 for `b`.

**Validates: Requirements 2.1, 2.2, 2.3**

### Property 2: Preservation

*For any* initial stock `s` in 0–50 and any sequence of reserves whose running sum stays at or below `s`, the Inventory SHALL accept each reserve and report available as `s` minus the sum; qty < 1 SHALL raise `ValueError`; a single qty above `s` SHALL raise `OutOfStock`; any release SHALL keep available at or below `s`; `Cart.remove` SHALL return the line's units to available.

**Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5**

## Regression Strategy

- Exploration pin (red before fix): `tests/test_oversell_pin.py`. Property 1 plus the example from the repro (stock 5, 3 + 3) through `Cart` and through `handle`. Fails on current code.
- Preservation pins (green before fix): `tests/test_oversell_preservation.py`. Property 2, one test per Unchanged item:
  - 3.1 single reserve above stock → `OutOfStock`
  - 3.2 qty in −10–0 → `ValueError`
  - 3.3 reserves then releases of any qty → available ≤ initial
  - 3.4 `Cart.remove` → available back to value before the add
  - 3.5 reserve sequences with sum ≤ stock → all accepted, available = stock − sum
- Existing `tests/test_cart.py` stays green.

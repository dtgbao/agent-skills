# Design Document: cart oversell

## Root Cause

`shop/inventory.py:16` checks `qty > self._initial[sku]`. It compares one request to the initial stock and ignores units that other carts already hold in `self._reserved[sku]`. `shop/inventory.py:18` then adds qty to the reserved total with no bound.

- 1.1: cart B asks 3, 3 ≤ 5, check passes, no OutOfStock.
- 1.2: reserved becomes 6, `available` (`shop/inventory.py:11`) = 5 − 6 = −1.
- 1.3: `Cart.add` (`shop/cart.py:13-14`) appends the line because reserve did not raise.
- 1.4: `shop/api.py:20` calls `cart.add`, no exception, so `shop/api.py:27` returns 200.

Neighbor paths on the same check: one cart that adds the same sku twice (`shop/cart.py:14` sums lines), and every API add. `release` (`shop/inventory.py:20-21`) is not faulty.

## Fix

Component: `Inventory.reserve` only. Compare qty to `self.available(sku)`, not to `self._initial[sku]`.

Constraints:
- Keep the `qty < 1` check first (ValueError before OutOfStock).
- On OutOfStock, change no state (reserved total stays the same), so `Cart.add` adds no line.
- No change to `Cart`, `api.handle`, or `release`. They get the fix through `reserve`.

### Call-tree Change

```diff
 api.handle POST /carts/<id>/lines
   Cart.add(sku, qty)
     Inventory.reserve(sku, qty)
       if qty < 1: raise ValueError
-      if qty > self._initial[sku]: raise OutOfStock
+      if qty > self.available(sku): raise OutOfStock
       self._reserved[sku] += qty
     self.lines[sku] += qty
   except OutOfStock -> 409
```

## Correctness Properties

### Property 1: Fix check

*For any* initial stock 0–50 and any sequence of 1–20 reserves with qty 1–20 across carts, `Inventory` SHALL raise OutOfStock exactly when qty is greater than `available` before the call, leave `available` unchanged on that raise, and keep `available` ≥ 0 after every call.

**Validates: Requirements 2.1, 2.2, 2.3**

### Property 2: Preservation

*For any* sequence of reserves that each fit `available`, and any releases, `Inventory` SHALL accept every reserve, lower `available` by qty, and keep `available` ≤ initial stock after every release.

**Validates: Requirements 3.3, 3.5**

## Regression Strategy

- Exploration pin (red before fix): `tests/test_oversell_pin.py` — two-cart repro for 2.1, 2.2, 2.3, and API 409 for 2.4.
- Preservation pins (green before fix): `tests/test_preservation_pin.py` — 3.1 (one reserve over stock → OutOfStock), 3.2 (qty 0 and −1 → ValueError), 3.3 (release over reserved, available ≤ initial), 3.4 (Cart.remove restores available), 3.5 (fit-exact add → available 0), 3.6 (unknown sku → KeyError), and Property 2 with Hypothesis.
- Fix check: `tests/test_inventory_props.py` — Property 1 with Hypothesis, after the fix.
- Existing `tests/test_cart.py` stays green.

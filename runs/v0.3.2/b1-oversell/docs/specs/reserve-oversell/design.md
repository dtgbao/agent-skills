# Design Document: reserve oversell

## Root Cause

`Inventory.reserve` checks the request against initial stock, not against units still free.

- `shop/inventory.py:18` — `if qty > self._initial[sku]` ignores `self._reserved[sku]`. Cart B asks 3 of stock 5: 3 > 5 is false, so no `OutOfStock` (1.1).
- `shop/inventory.py:20` — reserved goes 3 → 6, so `available` (`shop/inventory.py:13`) = 5 − 6 = −1 (1.2).
- `shop/cart.py:13-14` — `Cart.add` writes the line only after `reserve` returns. No raise → cart B gets line 3 (1.3).
- `shop/api.py:18,23` — the 409 branch needs `OutOfStock`. No raise → status 200 (1.4).

Neighbor paths on the same code: `Cart.add` and `POST /carts/<id>/lines` both go through `reserve`, so one fix covers all four Current items. `release` (`shop/inventory.py:23`) and `Cart.remove` do not read the check; they stay as they are.

## Fix

- Component: `Inventory.reserve` only (`shop/inventory.py`).
- Change: compare `qty` to `self.available(sku)` instead of `self._initial[sku]`.
- Constraints:
  - Keep the `qty < 1` → `ValueError` check first (3.2).
  - Raise before any state change, so `_reserved` and cart lines stay as they were (2.2, 2.3).
  - `qty == available` still passes (3.5, 3.6). Single over-stock reserve still fails, since available ≤ initial (3.1).
  - No change to `release`, `Cart`, or `api` (3.3, 3.4, 2.4 via existing 409 branch).

### Call-tree Change

```diff
 api.handle POST /carts/<id>/lines
   Cart.add(sku, qty)
     Inventory.reserve(sku, qty)
       if qty < 1: raise ValueError
-      if qty > _initial[sku]: raise OutOfStock
+      if qty > available(sku): raise OutOfStock
       _reserved[sku] += qty
     lines[sku] += qty
   except OutOfStock -> 409
```

## Correctness Properties

### Property 1: Fix check

*For any* initial stock s ≥ 0 and sequence of reserves on one SKU from one or more carts, where a reserve asks qty > available, `Inventory` SHALL raise `OutOfStock` and leave available unchanged, so available never goes below 0; `Cart.add` SHALL leave that cart's lines unchanged and `api.handle` SHALL return 409.

**Validates: Requirements 2.1, 2.2, 2.3, 2.4**

### Property 2: Preservation

*For any* initial stock s ≥ 0 and sequence of reserve / release / remove calls where every reserve asks 1 ≤ qty ≤ available, `Inventory` SHALL accept each reserve and SHALL keep available = s − (sum of held units), with 0 ≤ available ≤ s; qty < 1 SHALL raise `ValueError`; a single reserve with qty > s SHALL raise `OutOfStock`.

**Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5, 3.6**

## Regression Strategy

Test framework: pytest + Hypothesis (README test command).

- Exploration pin (red before fix): `tests/test_oversell_pin.py` — example of the repro (2.1–2.4) plus Property 1 over random reserve sequences. Fails on current code with available −1.
- Preservation pins (green before fix): `tests/test_reserve_preserve.py` — examples for 3.1–3.6 plus Property 2 over random valid sequences. Existing `tests/test_cart.py` (subtotal, single over-stock, release on remove) stays as is.
- After fix: both files and `tests/test_cart.py` green.

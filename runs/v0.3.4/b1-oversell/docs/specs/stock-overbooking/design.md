# Design Document: stock overbooking

## Root Cause

The guard in `Inventory.reserve` tests the request against the full stock and ignores units that are already held:

- `shop/inventory.py:18` — `if qty > self._initial[sku]:`
- `shop/inventory.py:20` — `self._reserved[sku] += qty` then runs for any qty up to the full stock.
- `shop/inventory.py:13` — `available()` is `_initial - _reserved`, so it goes negative when `_reserved` passes `_initial`.

How this explains each Current item:

| Item | Trace |
|---|---|
| 1.1 | Cart B asks for 3. Guard tests 3 > 5: false. No raise. |
| 1.2 | `_reserved` becomes 3 + 3 = 6. `available` = 5 − 6 = −1. |
| 1.3 | Same cart, second `add` → `reserve(3)` (`shop/cart.py:13`). Guard tests 3 > 5 again: false. |

Paths that share the guard: every `Cart.add` (`shop/cart.py:13`), and the HTTP add route (`shop/api.py:18`), which turns `OutOfStock` into 409 at `shop/api.py:23-24`.

## Fix

One component changes: `Inventory.reserve` (`shop/inventory.py:15-20`).

```diff
 def reserve(sku, qty)
   if qty < 1
     raise ValueError
-  if qty > initial[sku]
+  if qty > available(sku)
     raise OutOfStock
   reserved[sku] += qty
```

Constraints:

- The `qty < 1` test stays first, so qty 0 or less still gives `ValueError` (3.2).
- The raise comes before the `+=`, so a refused reserve changes no state (2.2).
- `available(sku) ≤ initial[sku]` always holds, so the new guard refuses every request the old guard refused (3.1).
- `release`, `Cart`, and `handle` do not change. `Cart.add` calls `reserve` before it writes `lines` (`shop/cart.py:13-14`), so 3.6 holds. `handle` keeps its 409 branch (3.7).

### Call-tree Change

```diff
 handle(POST /carts/<id>/lines)              shop/api.py:16
   Cart.add(sku, qty)                        shop/cart.py:10
     Inventory.reserve(sku, qty)             shop/inventory.py:15
-      guard: qty > _initial[sku]            -> passes when other carts hold units
+      guard: qty > available(sku)           -> OutOfStock when held + qty > stock
+    (OutOfStock: lines not written)
-  return 200
+  except OutOfStock -> return 409           shop/api.py:23
```

## Correctness Properties

Framework: Hypothesis (`pyproject.toml`, Python).

### Property 1: Fix check

*For any* stock `s` in 1–40, units `h` in 0–`s` already held by other carts or the same cart, and a request `q` in 1–`s` with `h + q > s`, `Inventory.reserve` SHALL raise `OutOfStock` and `available` SHALL stay `s − h`.

**Validates: Requirements 2.1, 2.2, 2.3**

### Property 2: Preservation

*For any* stock `s` in 0–40 and any request outside the bug condition (qty < 1, a single qty above `s`, a running total ≤ `s`, any release, any remove, an add refused for stock), the system SHALL act as it does today: `ValueError` for qty < 1; `OutOfStock` for a single qty above `s`; accept each reserve while the total ≤ `s`; `available ≤ s` after releases; `Cart.remove` raises `available` by the line qty; a refused add leaves `lines` unchanged; the HTTP route returns 409 for a refused add.

**Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7**

## Regression Strategy

| Pin | File | Expect | Items |
|---|---|---|---|
| exploration | `tests/test_overbooking_repro.py` | red before fix | 2.1, 2.2, 2.3 (Property 1 + repro example + same-cart example) |
| preservation, inventory | `tests/test_overbooking_keep_inventory.py` | green before fix | 3.1, 3.2, 3.3, 3.5 |
| preservation, cart + HTTP | `tests/test_overbooking_keep_cart.py` | green before fix | 3.4, 3.6, 3.7 |

Existing `tests/test_cart.py` stays green with no edits.

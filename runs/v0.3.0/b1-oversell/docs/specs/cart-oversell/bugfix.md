# Bugfix Requirements Document

## Introduction

Two carts can reserve more units than are in stock. `Inventory.reserve` checks the requested qty against the initial stock, not against the units still available. Each single add passes, so the sum of reservations can exceed stock and `available` goes negative. Impact: the shop sells units it does not have.

Repro:
1. Start: `inv = Inventory({"MUG-01": 5})`, `a = Cart(inv)`, `b = Cart(inv)`.
2. `a.add("MUG-01", 3)` → succeeds, available 2.
3. `b.add("MUG-01", 3)` → succeeds (wrong).
4. `inv.available("MUG-01")` → `-1` (wrong).

Same path through the API: `POST /carts/<b>/lines {"sku": "MUG-01", "qty": 3}` returns 200 instead of 409.

## Bug Analysis

### Current Behavior (Defect)

1.1 WHEN stock of MUG-01 is 5 and cart A holds 3 units and cart B adds 3 units of MUG-01 THEN the system accepts the add without raising OutOfStock
1.2 WHEN stock of MUG-01 is 5 and cart A holds 3 units and cart B adds 3 units of MUG-01 THEN the system reports available of MUG-01 as -1
1.3 WHEN stock of MUG-01 is 5 and cart A holds 3 units and cart B adds 3 units of MUG-01 THEN the system records 3 units of MUG-01 in cart B lines
1.4 WHEN stock of MUG-01 is 5 and cart A holds 3 units and the API receives POST /carts/<B>/lines with sku MUG-01 and qty 3 THEN the system returns status 200

### Expected Behavior (Correct)

2.1 WHEN stock of MUG-01 is 5 and cart A holds 3 units and cart B adds 3 units of MUG-01 THE SYSTEM SHALL raise OutOfStock
2.2 WHEN stock of MUG-01 is 5 and cart A holds 3 units and cart B adds 3 units of MUG-01 THE SYSTEM SHALL keep available of MUG-01 at 2
2.3 WHEN stock of MUG-01 is 5 and cart A holds 3 units and cart B adds 3 units of MUG-01 THE SYSTEM SHALL keep MUG-01 absent from cart B lines
2.4 WHEN stock of MUG-01 is 5 and cart A holds 3 units and the API receives POST /carts/<B>/lines with sku MUG-01 and qty 3 THE SYSTEM SHALL return status 409

### Unchanged Behavior (Regression Prevention)

3.1 WHEN one reserve asks for more units than the initial stock of an empty inventory THE SYSTEM SHALL CONTINUE TO raise OutOfStock
3.2 WHEN a reserve asks for qty less than 1 THE SYSTEM SHALL CONTINUE TO raise ValueError
3.3 WHEN release asks for more units than are reserved THE SYSTEM SHALL CONTINUE TO keep available at or below the initial stock
3.4 WHEN Cart.remove is called for a sku the cart holds THE SYSTEM SHALL CONTINUE TO release all units of that line to the inventory
3.5 WHEN stock of MUG-01 is 5 and cart A holds 3 units and cart B adds 2 units of MUG-01 THE SYSTEM SHALL CONTINUE TO accept the add and report available as 0
3.6 WHEN a cart adds a sku that is not in the catalog THE SYSTEM SHALL CONTINUE TO raise KeyError

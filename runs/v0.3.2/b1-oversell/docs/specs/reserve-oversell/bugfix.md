# Bugfix Requirements Document

## Introduction

Two carts can reserve more units of one SKU than are in stock. `Inventory.reserve` compares the requested qty to the initial stock, not to the units still available. Impact: the shop oversells, and `available` goes negative.

Repro:
1. Starting state: `inv = Inventory({"MUG-01": 5})`, cart A and cart B both use `inv`.
2. Input: cart A `add("MUG-01", 3)`, then cart B `add("MUG-01", 3)`.
3. Observed: both adds succeed. `inv.available("MUG-01") == -1`. Cart B holds `{"MUG-01": 3}`. Via `api.handle`, the second `POST /carts/<id>/lines` returns status 200.

Expected: the second add is refused with `OutOfStock`, and `available` stays 2.

Must hold (from user): one reserve over stock still raises `OutOfStock`; qty < 1 raises `ValueError`; release never makes available exceed initial stock; `Cart.remove` releases its units.

## Bug Analysis

### Current Behavior (Defect)

1.1 WHEN stock of MUG-01 is 5, cart A holds 3, and cart B adds 3 THEN the system completes the add without raising OutOfStock
1.2 WHEN stock of MUG-01 is 5, cart A holds 3, and cart B adds 3 THEN the system reports available for MUG-01 as -1
1.3 WHEN stock of MUG-01 is 5, cart A holds 3, and cart B adds 3 THEN the system records a MUG-01 line of 3 in cart B
1.4 WHEN stock of MUG-01 is 5, cart A holds 3, and cart B posts qty 3 to /carts/<id>/lines THEN the system returns status 200

### Expected Behavior (Correct)

2.1 WHEN stock of MUG-01 is 5, cart A holds 3, and cart B adds 3 THE SYSTEM SHALL raise OutOfStock
2.2 WHEN stock of MUG-01 is 5, cart A holds 3, and cart B adds 3 THE SYSTEM SHALL report available for MUG-01 as 2
2.3 WHEN stock of MUG-01 is 5, cart A holds 3, and cart B adds 3 THE SYSTEM SHALL record no MUG-01 line in cart B
2.4 WHEN stock of MUG-01 is 5, cart A holds 3, and cart B posts qty 3 to /carts/<id>/lines THE SYSTEM SHALL return status 409

### Unchanged Behavior (Regression Prevention)

3.1 WHEN stock of MUG-01 is 2 and one cart adds 3 THE SYSTEM SHALL CONTINUE TO raise OutOfStock
3.2 WHEN a reserve asks for qty less than 1 THE SYSTEM SHALL CONTINUE TO raise ValueError
3.3 WHEN a release asks for more units than are reserved THE SYSTEM SHALL CONTINUE TO report available no greater than the initial stock
3.4 WHEN a cart holding 2 MUG-01 of stock 2 calls remove for MUG-01 THE SYSTEM SHALL CONTINUE TO report available for MUG-01 as 2
3.5 WHEN stock of MUG-01 is 5, cart A holds 3, and cart B adds 2 THE SYSTEM SHALL CONTINUE TO complete the add without raising OutOfStock
3.6 WHEN stock of MUG-01 is 5, cart A holds 3, and cart B adds 2 THE SYSTEM SHALL CONTINUE TO report available for MUG-01 as 0

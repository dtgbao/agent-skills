# Bugfix Requirements Document

## Introduction

Two carts can together reserve more units than are in stock. The inventory then reports a negative available count, so the shop sells units it does not have.

Repro:

1. Starting state: `Inventory({"MUG-01": 5})`, cart A and cart B on that inventory.
2. Input: cart A adds 3 MUG-01. Cart B adds 3 MUG-01.
3. Observed: both adds succeed. `available("MUG-01")` returns -1. Through the API, the second `POST /carts/<id>/lines` returns status 200.

Expected (implied by the input): the second add fails with `OutOfStock`, the API returns status 409, and available stays 2.

Must hold (from user): one reserve over stock still raises `OutOfStock`; qty < 1 raises `ValueError`; release never makes available exceed initial stock; `Cart.remove` releases its units.

The same check runs for two adds from one cart, so one cart can also oversell. The fix covers both paths.

## Bug Analysis

### Current Behavior (Defect)

1.1 WHEN stock of MUG-01 is 5, cart A holds 3 MUG-01, and cart B adds 3 MUG-01 THEN the system accepts the add without an error
1.2 WHEN stock of MUG-01 is 5, cart A holds 3 MUG-01, and cart B adds 3 MUG-01 THEN the system reports available for MUG-01 as -1
1.3 WHEN stock of MUG-01 is 5, cart A holds 3 MUG-01, and cart B posts 3 MUG-01 to `/carts/<id>/lines` THEN the system returns status 200

### Expected Behavior (Correct)

2.1 WHEN stock of MUG-01 is 5, cart A holds 3 MUG-01, and cart B adds 3 MUG-01 THE SYSTEM SHALL raise `OutOfStock`
2.2 WHEN stock of MUG-01 is 5, cart A holds 3 MUG-01, and cart B adds 3 MUG-01 THE SYSTEM SHALL keep available for MUG-01 at 2
2.3 WHEN stock of MUG-01 is 5, cart A holds 3 MUG-01, and cart B posts 3 MUG-01 to `/carts/<id>/lines` THE SYSTEM SHALL return status 409

### Unchanged Behavior (Regression Prevention)

3.1 WHEN one reserve asks for more units than the initial stock of a sku THE SYSTEM SHALL CONTINUE TO raise `OutOfStock`
3.2 WHEN a reserve asks for a qty less than 1 THE SYSTEM SHALL CONTINUE TO raise `ValueError`
3.3 WHEN release is called with any qty THE SYSTEM SHALL CONTINUE TO keep available at or below the initial stock of that sku
3.4 WHEN `Cart.remove` is called for a sku the cart holds THE SYSTEM SHALL CONTINUE TO return that line's units to available
3.5 WHEN the sum of all reserves for a sku stays at or below its initial stock THE SYSTEM SHALL CONTINUE TO accept each reserve

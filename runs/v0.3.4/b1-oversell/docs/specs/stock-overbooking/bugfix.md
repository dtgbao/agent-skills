# Bugfix Requirements Document

## Introduction

`Inventory.reserve` lets the units held by all carts go above the stock of a sku. The shop then promises units it does not have, and `available()` goes below zero.

Repro steps:

- Start: `inv = Inventory({"MUG-01": 5})`; `a = Cart(inv)`; `b = Cart(inv)`.
- Do: `a.add("MUG-01", 3)`, then `b.add("MUG-01", 3)`.
- See: no error on either add; `inv.available("MUG-01") == -1`.

The input implies the expected result: the add by cart B fails with `OutOfStock`, and the 2 free units stay free.

The user named these behaviors that must not change: a single reserve above stock raises `OutOfStock`; qty below 1 raises `ValueError`; `release` never lifts available above the initial stock; `Cart.remove` gives its units back.

Investigation found the same check on two more paths: one cart that adds the same sku twice, and the HTTP add route `POST /carts/<id>/lines`, which maps `OutOfStock` to status 409.

## Bug Analysis

### Current Behavior (Defect)

1.1 WHEN MUG-01 has stock 5 and cart A has reserved 3 units THEN the system lets cart B reserve 3 more units with no `OutOfStock`
1.2 WHEN MUG-01 has stock 5 and cart A has reserved 3 units and cart B reserves 3 units THEN the system returns -1 from `available("MUG-01")`
1.3 WHEN MUG-01 has stock 5 and one cart adds 3 units two times THEN the system accepts the second add with no `OutOfStock`

### Expected Behavior (Correct)

2.1 WHEN MUG-01 has stock 5 and cart A has reserved 3 units THE SYSTEM SHALL raise `OutOfStock` for a reserve of 3 more units by cart B
2.2 WHEN MUG-01 has stock 5 and cart A has reserved 3 units and cart B tries to reserve 3 units THE SYSTEM SHALL return 2 from `available("MUG-01")`
2.3 WHEN MUG-01 has stock 5 and one cart adds 3 units two times THE SYSTEM SHALL raise `OutOfStock` for the second add

### Unchanged Behavior (Regression Prevention)

3.1 WHEN no units of a sku are reserved and one reserve asks for more units than its stock THE SYSTEM SHALL CONTINUE TO raise `OutOfStock`
3.2 WHEN a reserve asks for 0 or fewer units THE SYSTEM SHALL CONTINUE TO raise `ValueError`
3.3 WHEN `release` runs with any number of units THE SYSTEM SHALL CONTINUE TO return at most the initial stock from `available`
3.4 WHEN `Cart.remove` runs for a sku in the cart THE SYSTEM SHALL CONTINUE TO raise `available` by the qty of that line
3.5 WHEN the running total of reserves for a sku stays at or below its stock THE SYSTEM SHALL CONTINUE TO accept each reserve
3.6 WHEN `Cart.add` raises `OutOfStock` THE SYSTEM SHALL CONTINUE TO leave the lines of that cart unchanged
3.7 WHEN an add through `POST /carts/<id>/lines` raises `OutOfStock` THE SYSTEM SHALL CONTINUE TO return status 409

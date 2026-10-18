# Analyst round 1 (FULL) — raw hand-back from agent a2b56d0a3c28a7a5e

```
ID: F1
TYPE: ASSUMPTION
SEVERITY: high
AFFECTS: Requirement 2.1, 2.3, 4.6, 5.1, 5.5
QUOTE: "Current_Date: the calendar date that the caller passes in for each operation."
ISSUE: `shop.api.handle(request, ctx)` has no date field in `request` or `ctx`, and `Cart` has no date parameter. The spec does not say where Current_Date comes from.
OPTIONS:
  A) 5.6: NEEDS_OWNER: Which key gives Current_Date to the Handler (for example `ctx["today"]` as a `datetime.date`), and how does Cart receive it?
CHECK: gaps=1 shall=0 asserts=0 owner=sole

ID: F2
TYPE: ASSUMPTION
SEVERITY: high
AFFECTS: Requirement 1.1, 2.1, 2.2, 5.1
QUOTE: "Code_Book: the set of Discount_Codes the Operator has created, one per Code."
ISSUE: The Code_Book has no owner or access path. `ctx` holds only `carts` and `inventory`, and `Cart(inventory)` has no link to a Code_Book. The Operator has no named create interface.
OPTIONS:
  A) 5.7: NEEDS_OWNER: Where does the Code_Book live (for example `ctx["code_book"]`), and what is the name of the Operator create function?
CHECK: gaps=1 shall=0 asserts=0 owner=sole

ID: F3
TYPE: INCONSISTENCY
SEVERITY: high
AFFECTS: Requirement 4.1, 4.2, 4.5, 4.6
QUOTE: "WHILE the Subtotal is less than the Attached_Code's Min_Subtotal, THE Cart SHALL report Discount_Amount = 0 cents."
ISSUE: With a percent or fixed Attached_Code and a Subtotal below Min_Subtotal (or an expired code), 4.1/4.2 give a positive Discount_Amount and 4.5/4.6 give 0. Both hold at once.
OPTIONS:
  A) 4.5: WHILE the Subtotal is less than the Attached_Code's Min_Subtotal, THE Cart SHALL report Discount_Amount = 0 cents, overriding 4.1 and 4.2, and 4.6 likewise overrides them when Current_Date is after Valid_Until.
  B) 4.7: WHEN the Cart reports a price and the Attached_Code has Subtotal below Min_Subtotal or Current_Date after Valid_Until, THE Cart SHALL set Attached_Code to none and report Discount_Amount = 0 cents.
CHECK: gaps=1 shall=1 asserts=1 owner=none

ID: F4
TYPE: EDGE
SEVERITY: medium
AFFECTS: Requirement 2.2, 2.3, 2.4, 2.5, 5.2
QUOTE: "IF the Cart already has an Attached_Code, THEN THE Cart SHALL refuse the attach with reason `code_already_attached`."
ISSUE: Several refusal conditions can hold in one attach (for example expired, below minimum, and already attached). The spec does not say which reason wins, so the 422 body is not defined.
OPTIONS:
  A) 2.7: IF more than one refusal condition holds, THEN THE Cart SHALL refuse with the first reason in the order `code_not_found`, `code_already_attached`, `code_expired`, `minimum_not_met`.
  B) 2.7: IF more than one refusal condition holds, THEN THE Cart SHALL refuse with the first reason in the order `code_not_found`, `code_expired`, `minimum_not_met`, `code_already_attached`.
CHECK: gaps=1 shall=1 asserts=1 owner=none

ID: F5
TYPE: EDGE
SEVERITY: medium
AFFECTS: Requirement 1.1, 1.2, 1.3
QUOTE: "WHEN the Operator creates a Discount_Code whose fields are all in range, THE Code_Book SHALL hold that Discount_Code under its Code."
ISSUE: A Kind other than `percent` or `fixed` has no rule. Amount that is not an integer also has no rule. Neither is "in range" nor covered by 1.2 or 1.3.
OPTIONS:
  A) 1.7: IF the Kind is not `percent` or `fixed`, or the Amount is not an integer, THEN THE Code_Book SHALL refuse the Discount_Code and stay unchanged.
CHECK: gaps=1 shall=1 asserts=1 owner=none

ID: F6
TYPE: AMBIGUITY
SEVERITY: low
AFFECTS: Requirement 5.5
QUOTE: "with `code` null when the Cart has no Attached_Code"
ISSUE: The type of `code` when a code is attached is not stated: the Code string or the full record.
OPTIONS:
  A) 5.5: WHEN the Handler gets `GET /carts/<id>`, THE Handler SHALL add `code` (the Attached_Code's Code string, or null if none), `discount_cents`, and `amount_due_cents` to the existing body.
CHECK: gaps=1 shall=1 asserts=1 owner=none
```

## Orchestrator CHECK audit (spec-analyze step 3 repair)
| Finding | CHECK line | Literal rule (`gaps=1 shall=1 asserts=1`) | Real defect? | Repair |
|---|---|---|---|---|
| F1 | `shall=0 asserts=0 owner=sole` | fails literally | no: NEEDS_OWNER has no SHALL by design | none (treated as pass; logged issue) |
| F2 | `shall=0 asserts=0 owner=sole` | fails literally | no | none (same) |
| F3 | `gaps=1 shall=1 asserts=1` | passes | yes: option A changes 4.5 and 4.6 (two criteria, two assertions) | split into F3a (4.5) and F3b (4.6); both take A's text per criterion |
| F4 | pass | pass | no | none |
| F5 | pass | pass | no | none |
| F6 | pass | pass | no | none (low → deferred) |

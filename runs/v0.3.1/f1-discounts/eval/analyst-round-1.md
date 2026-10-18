# Analyst round 1 (FULL) — raw output

Delivered via SubagentHandback message (not in the Agent tool result).

```
Agent: spec-analyst subagent, running as claude-sonnet-5-5. Tools: Read, Glob, Grep, SubagentHandback.

ID: F1
TYPE: INCONSISTENCY
SEVERITY: high
AFFECTS: Requirement 3.1, Requirement 3.2, Requirement 4.1, Requirement 4.2
QUOTE: "WHILE a Cart holds a `percent` Applied_Code, THE Cart SHALL compute Discount_Amount as floor(Subtotal × `value` / 100) cents."
ISSUE: 3.1 and 3.2 give a non-zero Discount_Amount for any held code. 4.1 and 4.2 give 0 for the same state when the minimum is unmet or the code is expired. Both cannot hold.
OPTIONS:
  A) 4.3: WHILE a Cart holds an Applied_Code that is below its `min_subtotal_cents` or expired, THE Cart SHALL compute Discount_Amount as 0 cents, and this SHALL take precedence over 3.1 and 3.2.
  B) 3.1: WHILE a Cart holds an unexpired `percent` Applied_Code and Subtotal ≥ its `min_subtotal_cents`, THE Cart SHALL compute Discount_Amount as floor(Subtotal × `value` / 100) cents.

ID: F2
TYPE: EDGE
SEVERITY: medium
AFFECTS: Requirement 2.2, Requirement 2.3, Requirement 2.4, Requirement 2.5
QUOTE: "IF the Cart already holds an Applied_Code, THEN THE API SHALL return status 409 with error `code already applied` and keep the existing Applied_Code."
ISSUE: A request can meet several error conditions at once, for example an expired code that also fails the minimum, or a second code that is unknown. The spec does not say which status wins.
OPTIONS:
  A) 2.6: IF a request meets more than one of 2.2–2.5, THEN THE API SHALL return the status of the first met condition in the order 2.2, 2.3, 2.4, 2.5.
  B) 2.6: IF a request meets more than one of 2.2–2.5, THEN THE API SHALL return the status of the first met condition in the order 2.5, 2.2, 2.3, 2.4.

ID: F3
TYPE: FAILURE
SEVERITY: medium
AFFECTS: Requirement 2.1, Requirement 2.2
QUOTE: "WHEN a shopper sends `POST /carts/<id>/code` with a known, unexpired `code`"
ISSUE: No criterion covers a body with no `code` key or a `code` that is not a string. The existing `shop/api.py` returns 400 for bad input, for example `bad qty`. This case would raise `KeyError` or `TypeError` instead.
OPTIONS:
  A) 2.6: IF the `POST /carts/<id>/code` body has no `code` or a `code` that is not a string, THEN THE API SHALL return status 400 with error `bad code`.
  B) 2.6: IF the `POST /carts/<id>/code` body has no `code` or a `code` that is not a string, THEN THE API SHALL return status 404 with error `unknown code`.

ID: F4
TYPE: ASSUMPTION
SEVERITY: medium
AFFECTS: Requirement 4.2, Requirement 3.1, Requirement 3.2
QUOTE: "IF Today is after the Applied_Code's `expires_on`, THEN THE Cart SHALL compute Discount_Amount as 0 cents."
ISSUE: `Cart` in `shop/cart.py` has no access to `ctx["today"]`, and it does not hold a Discount_Code. The spec does not say how `Cart` gets Today or the code `value`.
OPTIONS:
  A) NEEDS_OWNER: How does Cart receive Today? Options are a `today` argument on its discount method, or Cart holding a reference to `ctx`.

ID: F5
TYPE: EDGE
SEVERITY: medium
AFFECTS: Requirement 5.1
QUOTE: "WHEN a shopper sends `DELETE /carts/<id>/code`, THE API SHALL clear the Applied_Code and return status 200."
ISSUE: A DELETE on a Cart that holds no Applied_Code is not specified. The status could be 200 (idempotent) or an error.
OPTIONS:
  A) 5.3: WHEN a shopper sends `DELETE /carts/<id>/code` to a Cart with no Applied_Code, THE API SHALL return status 200 and leave the Cart unchanged.
  B) 5.3: IF a shopper sends `DELETE /carts/<id>/code` to a Cart with no Applied_Code, THEN THE API SHALL return status 404 with error `no code`.

ID: F6
TYPE: EDGE
SEVERITY: medium
AFFECTS: Requirement 1.1
QUOTE: "WHEN an operator creates a Discount_Code with a `code` of 1–20 characters from A–Z, 0–9 and `-`, THE Code_Registry SHALL store it under that `code`."
ISSUE: The spec does not say what happens when the `code` already exists in the Code_Registry (overwrite or reject). A Cart's Applied_Code would change if the record were overwritten.
OPTIONS:
  A) 1.6: IF a Discount_Code has a `code` already in the Code_Registry, THEN THE Code_Registry SHALL reject it with `ValueError` and keep the existing record.
  B) 1.6: WHEN a Discount_Code has a `code` already in the Code_Registry, THE Code_Registry SHALL replace the stored record with the new one.

ID: F7
TYPE: EDGE
SEVERITY: low
AFFECTS: Requirement 1.1, Requirement 1.2, Requirement 1.3, Requirement 1.4, Requirement 1.5
QUOTE: "IF a Discount_Code has a `code` that does not match the format in 1.1, THEN THE Code_Registry SHALL reject it with `ValueError`."
ISSUE: `expires_on` has no validation rule, although the other fields do. A non-date value would fail later, when the code is applied.
OPTIONS:
  A) 1.6: IF a Discount_Code has an `expires_on` that is not a `datetime.date`, THEN THE Code_Registry SHALL reject it with `ValueError`.
```

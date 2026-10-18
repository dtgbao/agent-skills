# Analyst VERIFY 1 (1.7, 2.7, 4.5, 4.6 + Glossary) — raw hand-back from agent ac5e28b8f1b7b0014

```
ID: F8
TYPE: FAILURE
SEVERITY: medium
AFFECTS: Glossary Code_Book, Glossary Current_Date, Requirement 5.1, 5.2, 5.5
QUOTE: "The Handler reads it from `ctx["today"]`." / "held in `ctx["code_book"]`"
ISSUE: The code in shop/api.py documents ctx as only `carts` and `inventory`. The spec does not say what the Handler does when `ctx["today"]` or `ctx["code_book"]` is missing, or when `ctx["today"]` is not a `datetime.date`.
OPTIONS:
  A) 5.6: IF `ctx["today"]` is missing or not a `datetime.date`, or `ctx["code_book"]` is missing, on a request to a route in Requirement 5, THEN THE Handler SHALL answer status 500 with body `{"error": "bad_context"}` and leave every Cart unchanged.
  B) 5.6: IF `ctx["today"]` is missing or not a `datetime.date`, or `ctx["code_book"]` is missing, on a request to a route in Requirement 5, THEN THE Handler SHALL raise `KeyError` or `TypeError` to its caller.
CHECK: gaps=1 shall=1 asserts=1 owner=none

ID: F9
TYPE: EDGE
SEVERITY: low
AFFECTS: Requirement 1.5, 1.7, Glossary Min_Subtotal, Glossary Valid_Until
QUOTE: "IF the Kind is not `percent` or `fixed`, or the Amount is not an integer, THEN THE Code_Book SHALL refuse the Discount_Code and stay unchanged."
ISSUE: 1.7 covers a non-integer Amount only. A non-integer Min_Subtotal and a Valid_Until that is not a `datetime.date` are not covered. 1.5 checks the range only.
OPTIONS:
  A) 1.8: IF the Min_Subtotal is not an integer or the Valid_Until is not a `datetime.date`, THEN THE Code_Book SHALL refuse the Discount_Code with `ValueError` and stay unchanged.
CHECK: gaps=1 shall=1 asserts=1 owner=none

Notes: 1.7, 2.7, 4.5, 4.6 and the Glossary entries Code_Book, Current_Date and Cart code methods are consistent with each other and with 2.1 to 2.6, 4.1 to 4.4 and 5.1 to 5.5. 2.7 matches the reason strings in 2.2 to 2.5. 4.5 and 4.6 override 4.1 and 4.2 without conflict.
```

## Orchestrator CHECK audit
| Finding | CHECK line | Literal rule | Real defect? | Repair |
|---|---|---|---|---|
| F8 | pass | pass | yes: option A has 2 assertions (status 500 + carts unchanged) | split A into 5.6 (status 500) and 5.7 (carts unchanged) |
| F9 | pass | pass | no | none (low → deferred) |

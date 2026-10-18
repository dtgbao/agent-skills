# Analyst round 1 (FULL)

Raw output (hand-back message from agent a635cfec3dbed0e37):

```
ID: F1
TYPE: ASSUMPTION
SEVERITY: high
AFFECTS: Requirement 2.1, 2.2, 2.3, 2.4, 2.5, 4.5, 4.6
QUOTE: "THE Cart SHALL reject the apply with error `unknown code` and keep its Applied_Code unchanged."
ISSUE: `Cart.__init__(inventory)` takes no Code_Registry and no Today. The spec does not say how Cart gets them, what the apply and remove methods are called, how an error is signalled (exception class or return value), or the type of `ctx["today"]` and Expiry_Date (`datetime.date` or ISO string).
OPTIONS:
  A) 2.6: NEEDS_OWNER: Give the Cart method names and signatures for apply and remove. Say how Cart receives Code_Registry and Today. Say how it signals the four apply errors (exception class or return value). Say whether `ctx["today"]` and Expiry_Date are `datetime.date` or ISO strings.

ID: F2
TYPE: AMBIGUITY
SEVERITY: medium
AFFECTS: Requirement 2.2, 2.3, 2.4, 2.5, 5.2, 5.3
QUOTE: "IF the Cart already has an Applied_Code, THEN THE Cart SHALL reject the apply with error `code already applied`"
ISSUE: One apply can fail several criteria at once. The spec does not say which error wins, so the API status (400 or 409) is undefined.
OPTIONS:
  A) 2.7: WHEN an apply fails more than one of 2.2–2.5, THE Cart SHALL return the error in this order: `code already applied`, `unknown code`, `expired`, `below minimum`.
  B) 2.8: WHEN an apply fails more than one of 2.2–2.5, THE Cart SHALL return the error in this order: `unknown code`, `expired`, `below minimum`, `code already applied`.

ID: F3
TYPE: ASSUMPTION
SEVERITY: medium
AFFECTS: Requirement 1.1–1.5, 5.1
QUOTE: "THE Code_Registry SHALL store it so a lookup by that Code_String returns it."
ISSUE: No `Code_Registry` exists in `shop/`. The spec names no class, no add or lookup method, and no type for `ctx["codes"]`.
OPTIONS:
  A) 1.6: NEEDS_OWNER: Give the Code_Registry type and its add and lookup method names and signatures. Say whether `ctx["codes"]` is a plain dict or a registry object. Say which module holds it.

ID: F4
TYPE: EDGE
SEVERITY: medium
AFFECTS: Requirement 1.1–1.4
QUOTE: "IF the Code_String is not 1–20 characters of `A–Z` and `0–9`, or the Minimum_Subtotal is not an integer from 0 to 10,000,000, THEN THE Code_Registry SHALL reject the code with a `ValueError`."
ISSUE: No criterion rejects a Discount_Kind other than `percent` or `fixed`, or an Expiry_Date that is not a calendar date.
OPTIONS:
  A) 1.7: IF the Discount_Kind is not `percent` or `fixed`, or the Expiry_Date is not a calendar date, THEN THE Code_Registry SHALL reject the code with a `ValueError` and store nothing.
  B) 1.8: IF the Discount_Kind is not `percent` or `fixed`, THEN THE Code_Registry SHALL reject the code with a `ValueError`; THE Code_Registry SHALL NOT check the Expiry_Date type.

ID: F5
TYPE: EDGE
SEVERITY: medium
AFFECTS: Requirement 2.1, 2.2, 5.2, 5.6
QUOTE: "WHEN a shopper applies a Code_String that the Code_Registry holds"
ISSUE: Case-sensitivity and trimming of shopper input are unspecified.
OPTIONS:
  A) 2.9: WHEN a shopper applies text that is not an exact, case-sensitive match to a stored Code_String, THE Cart SHALL reject the apply with error `unknown code`.
  B) 2.10: WHEN a shopper applies a Code_String, THE Cart SHALL look it up after removing surrounding whitespace and converting it to uppercase.
```

Note: AFFECTS lists shortened by orchestrator for F2–F5 (ids kept); text otherwise verbatim. F4 option B has 2 SHALLs (checklist breach; repaired by not choosing it).

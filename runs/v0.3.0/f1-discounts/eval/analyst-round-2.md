# Analyst round 2 (FULL) — raw output

Model: Sonnet 5.5 (claude-sonnet-5-5)

ID: F5
TYPE: INCONSISTENCY
SEVERITY: medium
AFFECTS: Requirement 3.1, 3.2, 3.5, 3.6
QUOTE: "WHILE the Cart holds a Discount_Code and the Subtotal is below its Minimum_Subtotal, THE Cart SHALL set Discount_Amount to 0 cents."
ISSUE: 3.1 and 3.2 set a non-zero Discount_Amount for any held code. 3.5 and 3.6 set 0 in the same state. No rule says which one wins.
OPTIONS:
  A) 3.1: WHILE the Cart holds a `percent` Discount_Code whose Minimum_Subtotal is met and whose Expiry_Date is not before Today, THE Cart SHALL set Discount_Amount to floor(Subtotal × Discount_Value ÷ 100) cents.
     3.2: WHILE the Cart holds a `fixed` Discount_Code whose Minimum_Subtotal is met and whose Expiry_Date is not before Today, THE Cart SHALL set Discount_Amount to the smaller of Discount_Value and Subtotal, in cents.
  B) 3.7: IF 3.5 or 3.6 applies, THEN THE Cart SHALL set Discount_Amount to 0 cents, overriding 3.1 and 3.2.

ID: F6
TYPE: AMBIGUITY
SEVERITY: medium
AFFECTS: Requirement 2.1
QUOTE: "a body `code` that names a usable Discount_Code"
ISSUE: "usable" is not defined. It overlaps with the 404, 409, and 422 checks in 2.3 to 2.6.
OPTIONS:
  A) 2.1: WHEN the Shopper sends `POST /carts/<id>/discount` with a body `code` and no error in criteria 2.2 to 2.7 applies, THE Shop_API SHALL attach the code to the Cart and return status 200 with `subtotal_cents`, `discount_cents`, and `total_cents`.

ID: F7
TYPE: AMBIGUITY
SEVERITY: medium
AFFECTS: Requirement 2.2, 1.4, Glossary Code_String
QUOTE: "IF the body `code` is missing or does not match the Code_String format, THEN THE Shop_API SHALL return status 400"
ISSUE: The Code_String format lists `A–Z` but also says matching ignores letter case. It is unclear whether lower-case input such as `save10` is a valid format or a `bad code`. It is also unclear whether a non-string `code` value gives `bad code`.
OPTIONS:
  A) 2.10: THE Shop_API SHALL treat a body `code` as well-formed only when it is a string of 1–20 characters from `A–Z`, `a–z`, `0–9`, `-`, and SHALL otherwise return `bad code`.
  B) 2.10: THE Shop_API SHALL treat a body `code` as well-formed only when it is a string of 1–20 characters from `A–Z`, `0–9`, `-`, and SHALL otherwise return `bad code`.

ID: F8
TYPE: EDGE
SEVERITY: medium
AFFECTS: Requirement 2.9, 2.8, 3.6, 4.1, 4.2
QUOTE: "IF `ctx[\"today\"]` is missing or is not a `YYYY-MM-DD` date, THEN THE Shop_API SHALL raise a ValueError and leave every Cart unchanged."
ISSUE: 2.9 covers only the apply endpoint. 3.6 needs Today for GET cart and POST lines, but no rule covers a bad `today` there. It is also unclear whether 2.9 is checked before the no-cart and bad-code errors in 2.8.
OPTIONS:
  A) 2.9: IF `ctx["today"]` is missing or is not a `YYYY-MM-DD` date, THEN THE Shop_API SHALL raise a ValueError before any other check, for every request that reads a Cart, and leave every Cart unchanged.
  B) 2.9: IF `ctx["today"]` is missing or invalid on `POST /carts/<id>/discount`, THEN THE Shop_API SHALL raise a ValueError after the 2.8 order checks pass, and leave every Cart unchanged.

ID: F9
TYPE: ASSUMPTION
SEVERITY: low
AFFECTS: Requirement 1.1, 4.1, Glossary Code_Registry
QUOTE: "the operator-defined map from Code_String to Discount_Code, passed in `ctx`."
ISSUE: The `ctx` key for the Code_Registry is not named. The Operator registration call is not named. The shape of each item in `lines` is not defined. Design must guess all three.
OPTIONS:
  A) NEEDS_OWNER: Which `ctx` key holds the Code_Registry (for example `ctx["codes"]`), what is the registration function name, and what fields does each `lines` item have?

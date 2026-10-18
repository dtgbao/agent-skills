# Analyst VERIFY 1 (ids 1.6, 1.7, 2.2, 2.6, 2.7 + Glossary)

```
ID: F6
TYPE: ASSUMPTION
SEVERITY: medium
AFFECTS: Requirement 1.1, 1.2, 1.7, Glossary Code_Registry
QUOTE: "`add(code: DiscountCode) -> None`"
ISSUE: The Glossary names the class `DiscountCode`, but no such class exists in shop/ and the Glossary does not define it. Its constructor, field names and module are not stated. The Code_Registry validates the fields (1.2-1.7), so the class must accept invalid values without raising.
OPTIONS:
  A) 1.8: NEEDS_OWNER: What are the module, constructor signature and field names of `DiscountCode` (for example `shop.discounts.DiscountCode(code_string, kind, value, minimum_subtotal, expiry_date)`)? Does the constructor accept invalid values so that only `CodeRegistry.add` raises `ValueError`?

No other defects found in 1.6, 1.7, 2.2, 2.6, 2.7 or the checked Glossary entries (Expiry_Date, Today, Code_Registry, DiscountError, Cart discount methods).
```

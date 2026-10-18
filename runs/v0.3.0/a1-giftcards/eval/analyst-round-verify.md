# Analyst verify pass (mode VERIFY 1.1, 1.3–1.10, 2.1–2.9, 3.3, 3.4, 5.3, 5.4; next id F24)

Model: Sonnet 5.5 (claude-sonnet-5-5). Tools: Read, Glob, Grep, SubagentHandback.

ID: F24
TYPE: EDGE
SEVERITY: medium
AFFECTS: Requirement 1.9, 1.10
QUOTE: "WHEN the Shop_API receives a purchase request with an idempotency key that it already processed, THE Shop_API SHALL return the first result."
ISSUE: Two cases are not defined: a duplicate key that arrives while the first request is still in progress, and a duplicate key with a different value. "idempotency key" is not in the Glossary and has no stated retention period.
OPTIONS:
  A) 1.11: IF a purchase request has an idempotency key that is in progress or was used with a different value, THEN THE Shop_API SHALL return HTTP 409 with error `idempotency_conflict` and not charge the Payment_Provider.
  B) 1.11: WHEN a purchase request has an idempotency key that is in progress, THE Shop_API SHALL wait for the first request to finish and return its result.

ID: F25
TYPE: EDGE
SEVERITY: medium
AFFECTS: Requirement 2.1, 2.5, 2.7
QUOTE: "WHEN a shopper applies an `active` Gift_Card code to a Cart with a subtotal not above the Gift_Card balance, THE Shop_API SHALL subtract the Cart subtotal from the Gift_Card balance."
ISSUE: The criteria do not say whether the Cart is marked as paid after a redemption. A repeated request for the same Cart, such as a retry or double click, could subtract the balance twice.
OPTIONS:
  A) 2.10: WHEN a redemption succeeds, THE Shop_API SHALL record the amount applied on the Cart and reject a second redemption on that Cart with HTTP 409 and error `cart_already_paid`.
  B) 2.10: NEEDS_OWNER: may one Cart take several Gift_Cards, and how is a repeated request for the same Cart and code handled?

ID: F26
TYPE: FAILURE
SEVERITY: medium
AFFECTS: Requirement 5.3, 5.4, 1.6
QUOTE: "IF the refund of a charge fails, THEN THE Shop_API SHALL record the charge for manual refund."
ISSUE: The place of the record, the data kept, and the HTTP response are not defined. The "cancel or refund" choice in 1.6 is also open. A refund failure after a ledger failure could give a different response than 503.
OPTIONS:
  A) 5.4: IF the refund of a charge fails, THEN THE Shop_API SHALL store the charge id, amount, and UTC timestamp in a manual-refund queue and still return the original error.
  B) 5.4: NEEDS_OWNER: where do finance staff see the manual refund list, and who owns it?

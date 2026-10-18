# Analyst round 2 (mode FULL, deferred F11 F12 F13, next id F14)

Running as Sonnet 5.5 (claude-sonnet-5-5). Tools: Read, Glob, Grep, SubagentHandback.

ID: F14
TYPE: INCONSISTENCY
SEVERITY: medium
AFFECTS: Requirement 2.1, 2.5, 2.7
QUOTE: "THE Shop_API SHALL subtract the Cart subtotal from the Gift_Card balance."
ISSUE: 2.1 subtracts the full subtotal without a condition. When the subtotal exceeds the balance, this gives a negative balance. 2.5 and 2.7 require 0.
OPTIONS:
  A) 2.1: WHEN a shopper applies an `active` Gift_Card code to a Cart with a subtotal not above the Gift_Card balance, THE Shop_API SHALL subtract the Cart subtotal from the Gift_Card balance.
  B) 2.1: WHEN a shopper applies an `active` Gift_Card code to a Cart, THE Shop_API SHALL subtract the lesser of the Cart subtotal and the Gift_Card balance from the Gift_Card balance.

ID: F15
TYPE: INCONSISTENCY
SEVERITY: medium
AFFECTS: Requirement 2.4, 2.8
QUOTE: "IF the code is not 16 characters or the Cart is not open, THEN THE Shop_API SHALL return HTTP 422 with error `invalid_request`."
ISSUE: A code that is not 16 characters also matches no Gift_Card. 2.4 requires 404 and 2.8 requires 422. The check order is not defined.
OPTIONS:
  A) 2.4: IF the code is 16 characters and does not match any Gift_Card, THEN THE Shop_API SHALL return HTTP 404 with error `unknown_card`.
  B) 2.8: IF the code is not 16 characters or the Cart is not open, THEN THE Shop_API SHALL return HTTP 422 with error `invalid_request` before any Gift_Card lookup.

ID: F16
TYPE: FAILURE
SEVERITY: high
AFFECTS: Requirement 1.3, 1.4, 5.3
QUOTE: "IF the Payment_Provider declines the charge or does not respond within 10 seconds, THEN THE Shop_API SHALL create no Gift_Card."
ISSUE: After a timeout, the charge can still succeed at the Payment_Provider. The shopper pays and gets no card. Nothing requires a refund or void of a late charge.
OPTIONS:
  A) 1.6: IF the Payment_Provider does not respond within 10 seconds, THEN THE Shop_API SHALL cancel or refund any charge that the Payment_Provider later confirms for that purchase.
  B) NEEDS_OWNER: Does the Payment_Provider support charge cancel by idempotency key? What is the retry limit for the cancel?

ID: F17
TYPE: EDGE
SEVERITY: medium
AFFECTS: Requirement 1.1
QUOTE: "WHEN a shopper buys a Gift_Card with a whole-dollar value from 10 to 500 dollars inclusive, THE Shop_API SHALL charge the Payment_Provider that value."
ISSUE: No criterion covers a value below 10, above 500, or not a whole dollar. No criterion covers a missing value. The status code and error are not defined.
OPTIONS:
  A) 1.6: IF the purchase value is not a whole-dollar value from 10 to 500 dollars inclusive, THEN THE Shop_API SHALL return HTTP 422 with error `invalid_request` and not charge the Payment_Provider.

ID: F18
TYPE: FAILURE
SEVERITY: medium
AFFECTS: Requirement 5.3
QUOTE: "IF the ledger write for a new Gift_Card fails after the Payment_Provider charge, THEN THE Shop_API SHALL refund the charge."
ISSUE: The result is not defined if the refund fails. The response to the shopper is not defined. 5.2 says 503, but no criterion says whether the refund outcome changes it.
OPTIONS:
  A) 5.4: IF the refund of a charge fails, THEN THE Shop_API SHALL record the charge for manual refund and return HTTP 503 with error `ledger_unavailable`.
  B) NEEDS_OWNER: Where must a failed refund be recorded, and who handles it?

ID: F19
TYPE: EDGE
SEVERITY: medium
AFFECTS: Requirement 3.1
QUOTE: "WHEN a staff member voids a Gift_Card through the Merchant_Portal, THE Shop_API SHALL set the Gift_Card status to `void`."
ISSUE: A void request from a non-staff caller, or without an actor id, is not defined. Shop_API could void a card for any caller.
OPTIONS:
  A) 3.3: IF a void request has no staff actor id, THEN THE Shop_API SHALL return HTTP 403 with error `forbidden` and not change the Gift_Card.
  B) NEEDS_OWNER: How does Shop_API check that an actor id belongs to staff?

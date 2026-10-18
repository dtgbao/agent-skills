# Analyst round 3 (mode FULL, deferred F11 F12 F13, next id F20)

Model: Sonnet 5.5 (claude-sonnet-5-5). Tools: Read, Glob, Grep, SubagentHandback.

ID: F20
TYPE: EDGE
SEVERITY: medium
AFFECTS: Requirement 2.4, 2.8, 3.2
QUOTE: "WHILE a Gift_Card is `void`, THE Shop_API SHALL reject redemption with HTTP 409 and error `card_void`."
ISSUE: One request can break several rules, for example a void card with a closed Cart. The check order, and so the error code, is not defined.
OPTIONS:
  A) 2.9: THE Shop_API SHALL check redemption requests in this order: `invalid_request` (422), `unknown_card` (404), `card_void` (409), and return the first error that applies.
  B) 2.9: THE Shop_API SHALL check redemption requests in this order: `unknown_card` (404), `card_void` (409), `invalid_request` (422), and return the first error that applies.

ID: F21
TYPE: EDGE
SEVERITY: medium
AFFECTS: Requirement 1.1, 2.1
QUOTE: "WHEN a shopper buys a Gift_Card with a whole-dollar value from 10 to 500 dollars inclusive, THE Shop_API SHALL charge the Payment_Provider that value."
ISSUE: A repeated purchase request, or a repeated redemption request for the same Cart, is not defined. A network retry can charge twice or subtract twice.
OPTIONS:
  A) 1.9: WHEN the Shop_API receives a purchase request with an idempotency key that it already processed, THE Shop_API SHALL return the first result and SHALL NOT charge the Payment_Provider again.
  B) NEEDS_OWNER: Must purchase and redemption requests carry an idempotency key? How long must the Shop_API keep keys?

ID: F22
TYPE: EDGE
SEVERITY: low
AFFECTS: Requirement 5.1, 1.5
QUOTE: "THE Shop_API SHALL append a ledger entry with the code, old value, new value, actor id, and UTC timestamp."
ISSUE: A new Gift_Card has no old value. The actor id for a shopper purchase or redemption is not defined.
OPTIONS:
  A) 5.5: WHEN a Gift_Card is created, THE Shop_API SHALL write a ledger entry with old value 0 and the shopper account id as actor id.
  B) NEEDS_OWNER: What are the old value and the actor id in the ledger entry for card creation and shopper redemption?

ID: F23
TYPE: EDGE
SEVERITY: medium
AFFECTS: Requirement 3.1, 3.3, 3.4
QUOTE: "IF a void request has no staff actor id, THEN THE Shop_API SHALL return HTTP 403 with error `forbidden`."
ISSUE: Only a missing actor id is covered. An actor id that is not a staff member, or a void request that does not come from the Merchant_Portal, is not defined.
OPTIONS:
  A) 3.3: IF a void request has no staff actor id or the actor id does not belong to a staff member, THEN THE Shop_API SHALL return HTTP 403 with error `forbidden`.
  B) NEEDS_OWNER: How does the Shop_API check that an actor id belongs to staff?

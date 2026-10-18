# Analyst round 1 (FULL) — raw output

ID: F1
TYPE: INCONSISTENCY
SEVERITY: high
AFFECTS: Requirement 4.1, Requirement 4.2
QUOTE: "THE Shop_API SHALL keep Gift_Card balances forever; Gift_Cards never expire."
ISSUE: 4.1 says cards never expire. 4.2 voids a card after 12 months unused, which removes its value. Both cannot hold.
OPTIONS:
  A) 4.2: WHEN a Gift_Card has had no redemption for 12 months, THE Shop_API SHALL keep its status `active` and its balance unchanged.
  B) 4.1: THE Shop_API SHALL keep a Gift_Card `active` until it is voided by staff or reaches 12 months without redemption.

ID: F2
TYPE: ASSUMPTION
SEVERITY: medium
AFFECTS: Requirement 3.1
QUOTE: "WHEN a staff member voids a Gift_Card through the Merchant_Portal, THE Shop_API SHALL set the Gift_Card status to `void`."
ISSUE: Merchant_Portal is not in the Glossary. shop/api.py has no void route or staff identity, so design cannot tell how the void request reaches Shop_API.
OPTIONS:
  A) NEEDS_OWNER: What is Merchant_Portal, and what route and staff authentication does Shop_API use for void requests (for example `POST /gift-cards/{code}/void`)?

ID: F3
TYPE: AMBIGUITY
SEVERITY: medium
AFFECTS: Requirement 2.2
QUOTE: "THE Shop_API SHALL redeem gift cards promptly."
ISSUE: "promptly" has no measurable target.
OPTIONS:
  A) 2.2: THE Shop_API SHALL return the response to a redemption request within 2 seconds for 95% of requests.
  B) 2.2: Delete this criterion. Latency is outside the feature scope.

ID: F4
TYPE: CONFLICT
SEVERITY: medium
AFFECTS: Requirement 2.3, Requirement 1.1
QUOTE: "THE Shop_API SHALL accept Gift_Cards with a balance up to 1000 dollars."
ISSUE: Purchase limits value to 10–500 dollars and no requirement raises a balance, so a balance above 500 cannot exist. 2.3 also does not say what happens above 1000.
OPTIONS:
  A) 2.3: IF a Gift_Card balance is above 1000 dollars, THEN THE Shop_API SHALL reject redemption with HTTP 422 and error `balance_too_high`.
  B) 2.3: Delete this criterion. The 500-dollar purchase cap in 1.1 already bounds balance.

ID: F5
TYPE: EDGE
SEVERITY: high
AFFECTS: Requirement 2.1
QUOTE: "THE Shop_API SHALL subtract the Cart subtotal from the Gift_Card balance."
ISSUE: The spec does not say what happens when the subtotal is above the balance. A negative balance, a partial payment, and a rejection are all possible. Two concurrent redemptions of one card are also unspecified.
OPTIONS:
  A) 2.5: IF the Cart subtotal is greater than the Gift_Card balance, THEN THE Shop_API SHALL return HTTP 422 with error `insufficient_balance` and leave the balance unchanged.
  B) 2.5: IF the Cart subtotal is greater than the Gift_Card balance, THEN THE Shop_API SHALL set the balance to 0 and return the remaining amount in cents in the response.

ID: F6
TYPE: FAILURE
SEVERITY: medium
AFFECTS: Requirement 1.1
QUOTE: "THE Shop_API SHALL charge the Payment_Provider and create an `active` Gift_Card with that balance."
ISSUE: The spec gives no behavior for a failed or timed-out charge, or for a value outside 10–500 dollars. The spec does not say whether a card is created when the charge fails.
OPTIONS:
  A) 1.3: IF the Payment_Provider charge fails, THEN THE Shop_API SHALL return HTTP 402 with error `payment_failed` and create no Gift_Card.
  B) 1.3: IF the value is outside 10–500 dollars, THEN THE Shop_API SHALL return HTTP 400 with error `bad_value` and not charge the Payment_Provider.

ID: F7
TYPE: EDGE
SEVERITY: medium
AFFECTS: Requirement 3.1, Requirement 2.4
QUOTE: "WHEN a staff member voids a Gift_Card through the Merchant_Portal, THE Shop_API SHALL set the Gift_Card status to `void`."
ISSUE: The spec does not say what happens when staff void an unknown code or a card that is already `void`.
OPTIONS:
  A) 3.3: IF the code does not match any Gift_Card, THEN THE Shop_API SHALL return HTTP 404 with error `unknown_card` for a void request.
  B) 3.3: WHEN a staff member voids a Gift_Card that is already `void`, THE Shop_API SHALL return HTTP 200 and write no ledger entry.

ID: F8
TYPE: EDGE
SEVERITY: medium
AFFECTS: Requirement 5.1, Requirement 4.2, Requirement 1.2
QUOTE: "THE Shop_API SHALL append a ledger entry with the code, old value, new value, actor id, and UTC timestamp."
ISSUE: Card creation has no old value. The 12-month auto-void has no human actor. The spec also does not define "unused" in 4.2.
OPTIONS:
  A) 5.3: WHEN a Gift_Card is created or changed by the system, THE Shop_API SHALL write old value `null` for creation and actor id `system` for system changes in the ledger entry.
  B) NEEDS_OWNER: Which actor id and old value does the ledger record for card creation and for system-initiated changes?

ID: F9
TYPE: ASSUMPTION
SEVERITY: low
AFFECTS: Requirement 5.1, Requirement 5.2
QUOTE: "THE Shop_API SHALL append a ledger entry"
ISSUE: "ledger" and "actor id" are not in the Glossary, and no storage or format is given. Existing code has no ledger.
OPTIONS:
  A) NEEDS_OWNER: What is the Ledger store (name, location) and where does Shop_API get the actor id?

Model: Sonnet 5.5 (claude-sonnet-5-5).

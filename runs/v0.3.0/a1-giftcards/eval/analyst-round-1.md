# Analyst round 1 (mode FULL, next id F1)

Model: claude-sonnet-5-5 (Sonnet 5.5). Tools: Read, Glob, Grep, SubagentHandback.

ID: F1
TYPE: INCONSISTENCY
SEVERITY: high
AFFECTS: Requirement 4.1, 4.2
QUOTE: "THE Shop_API SHALL keep Gift_Card balances forever; Gift_Cards never expire."
ISSUE: 4.1 says cards never expire. 4.2 voids unused cards after 12 months, which removes the balance. Both cannot hold. Also the Requirement 4 story says the card keeps its value.
OPTIONS:
  A) 4.2: Delete this criterion. (4.1 stays. Cards never expire.)
  B) 4.1: THE Shop_API SHALL keep Gift_Card balances until the Gift_Card status is set to `void`.

ID: F2
TYPE: ASSUMPTION
SEVERITY: high
AFFECTS: Requirement 3.1
QUOTE: "WHEN a staff member voids a Gift_Card through the Merchant_Portal"
ISSUE: Merchant_Portal is not in the Glossary. Its interface to Shop_API and staff authentication are not defined.
OPTIONS:
  A) Glossary: **Merchant_Portal**: the staff web app that calls Shop_API with a staff actor id.
  B) 3.1: WHEN a staff member voids a Gift_Card, THE Shop_API SHALL set the Gift_Card status to `void`.

ID: F3
TYPE: AMBIGUITY
SEVERITY: medium
AFFECTS: Requirement 2.2
QUOTE: "THE Shop_API SHALL redeem gift cards promptly."
ISSUE: "promptly" has no measurable target.
OPTIONS:
  A) 2.2: THE Shop_API SHALL respond to a redemption request within 2 seconds for 95 percent of requests.
  B) A) NEEDS_OWNER: What response time limit and percentile apply to redemption?

ID: F4
TYPE: INCONSISTENCY
SEVERITY: high
AFFECTS: Requirement 1.1, 2.3
QUOTE: "THE Shop_API SHALL accept Gift_Cards with a balance up to 1000 dollars."
ISSUE: Purchase allows 10-500 dollars, so no card can hold more than 500 dollars. The 1000 limit has no source. The text does not say what happens above 1000.
OPTIONS:
  A) 2.3: THE Shop_API SHALL accept Gift_Cards with a balance up to 500 dollars.
  B) 1.1: Change the purchase range to 10–1000 dollars.

ID: F5
TYPE: EDGE
SEVERITY: high
AFFECTS: Requirement 2.1
QUOTE: "THE Shop_API SHALL subtract the Cart subtotal from the Gift_Card balance."
ISSUE: The case where the subtotal is more than the balance is not defined. The balance would go negative. The case where the subtotal is 0 or the Cart is empty is also not defined.
OPTIONS:
  A) 2.5: WHEN the Cart subtotal exceeds the Gift_Card balance, THE Shop_API SHALL subtract the full balance, set the balance to 0, and return the remaining amount due in cents.
  B) 2.5: IF the Cart subtotal exceeds the Gift_Card balance, THEN THE Shop_API SHALL reject the redemption with HTTP 422 and error `insufficient_balance`.

ID: F6
TYPE: EDGE
SEVERITY: high
AFFECTS: Requirement 2.1, 3.2, 5.1
QUOTE: "WHEN a shopper applies an `active` Gift_Card code to a Cart, THE Shop_API SHALL subtract the Cart subtotal from the Gift_Card balance."
ISSUE: Two requests that use the same card at the same time can both read the same balance. This causes double spend. A redeem that runs at the same time as a void is also not defined. Ledger old/new values would be wrong.
OPTIONS:
  A) 2.6: THE Shop_API SHALL apply concurrent redemptions and voids on one Gift_Card in sequence, so that the balance never falls below 0.
  B) A) NEEDS_OWNER: Which concurrency rule applies to one Gift_Card (lock, optimistic version check, or other)?

ID: F7
TYPE: FAILURE
SEVERITY: high
AFFECTS: Requirement 1.1, 1.2
QUOTE: "THE Shop_API SHALL charge the Payment_Provider and create an `active` Gift_Card with that balance."
ISSUE: No behavior is given when the charge is declined or times out. No behavior is given when the card is created but the response is lost (a retry could charge twice). An out-of-range value is not handled.
OPTIONS:
  A) 1.3: IF the Payment_Provider declines or times out after 10 seconds, THEN THE Shop_API SHALL create no Gift_Card and return HTTP 402 with error `payment_failed`.
  B) 1.4: IF the value is outside 10–500 dollars, THEN THE Shop_API SHALL return HTTP 422 with error `invalid_amount` and make no charge.

ID: F8
TYPE: EDGE
SEVERITY: medium
AFFECTS: Requirement 1.1
QUOTE: "a value of 10–500 dollars"
ISSUE: The text does not say if the bounds are inclusive. It does not say if cents or fractional dollars are allowed. Balance is stored in cents.
OPTIONS:
  A) 1.1: WHEN a shopper buys a Gift_Card with a whole-dollar value from 10 to 500 dollars inclusive, THE Shop_API SHALL charge the Payment_Provider and create an `active` Gift_Card with that balance.
  B) A) NEEDS_OWNER: Are cent values allowed, and are the bounds inclusive?

ID: F9
TYPE: FAILURE
SEVERITY: medium
AFFECTS: Requirement 1.1, 1.2, 5.1, 5.2
QUOTE: "IF the ledger write fails, THEN THE Shop_API SHALL reject the change with HTTP 503 and error `ledger_unavailable`."
ISSUE: Card creation is a status/balance change, so it needs a ledger entry. If the ledger fails after the charge, the shopper is charged with no card. No refund rule exists. Also the "old value" for a new card is not defined.
OPTIONS:
  A) 5.3: IF the ledger write fails after a Payment_Provider charge, THEN THE Shop_API SHALL refund the charge and return HTTP 503 with error `ledger_unavailable`.
  B) 5.3: WHEN a Gift_Card is created, THE Shop_API SHALL record the old value as null in the ledger entry.

ID: F10
TYPE: EDGE
SEVERITY: medium
AFFECTS: Requirement 2.1, 2.4, 3.2
QUOTE: "IF the code does not match any Gift_Card, THEN THE Shop_API SHALL return HTTP 404 with error `unknown_card`."
ISSUE: A malformed code (not 16 characters) is not defined. A Cart that does not exist or is not open is not defined. Repeated applying of the same code to the same Cart is not defined. Repeated bad guesses of codes (brute force) are not limited.
OPTIONS:
  A) 2.5: IF the code is not 16 characters or the Cart is not open, THEN THE Shop_API SHALL return HTTP 422 with error `invalid_request`.
  B) 2.6: IF one client sends more than 10 failed redemption requests in 1 minute, THEN THE Shop_API SHALL return HTTP 429 with error `rate_limited`.

ID: F11
TYPE: EDGE
SEVERITY: low
AFFECTS: Requirement 3.1
QUOTE: "THE Shop_API SHALL set the Gift_Card status to `void`."
ISSUE: Voiding a card that is already `void` or unknown is not defined. The remaining balance after a void is not defined (kept, set to 0, or refunded). Void is one way; there is no un-void.
OPTIONS:
  A) 3.3: IF the Gift_Card is already `void` or the code is unknown, THEN THE Shop_API SHALL return HTTP 404 with error `unknown_card` or HTTP 409 with error `card_void`, and change nothing.
  B) A) NEEDS_OWNER: What happens to the balance when a card is voided?

ID: F12
TYPE: ASSUMPTION
SEVERITY: low
AFFECTS: Requirement 5.1
QUOTE: "actor id"
ISSUE: "actor id" and "ledger" are not in the Glossary. The actor for a shopper, a staff member, or the system job (expiry) is not defined.
OPTIONS:
  A) Glossary: **Ledger**: the append-only record of Gift_Card changes. **Actor_Id**: the id of the shopper or staff member, or `system` for automatic changes.
  B) A) NEEDS_OWNER: What value is the actor id for shopper and system changes?

ID: F13
TYPE: AMBIGUITY
SEVERITY: low
AFFECTS: Requirement 4.2
QUOTE: "WHEN a Gift_Card is unused for 12 months"
ISSUE: "unused" and the start of the 12 months are not defined (from creation, or from last redemption). No time zone is given. Applies only if 4.2 is kept after F1.
OPTIONS:
  A) 4.2: WHEN 12 months pass since the last redemption, or since creation if never redeemed, THE Shop_API SHALL set the Gift_Card status to `void`.
  B) A) NEEDS_OWNER: When does the 12-month period start?

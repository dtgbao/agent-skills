# Analyst round 1 (FULL) — raw output

Delivered as a SubagentHandback message (not in the Agent tool result).

```
Model: claude-sonnet-5-5. Tools: Read, Glob, Grep, SubagentHandback.

ID: F1
TYPE: ASSUMPTION
SEVERITY: medium
AFFECTS: Requirement 3.1
QUOTE: "WHEN a staff member voids a Gift_Card through the Merchant_Portal, THE Shop_API SHALL set the Gift_Card status to `void`."
ISSUE: Merchant_Portal is not in the Glossary. shop/api.py has no void route or staff identity, so design cannot tell how a void request arrives.
OPTIONS:
  A) NEEDS_OWNER: What is Merchant_Portal, and which route, method, and staff credential does it use to send a void request to Shop_API?

ID: F2
TYPE: INCONSISTENCY
SEVERITY: high
AFFECTS: Requirement 4.1, 4.2
QUOTE: "Gift_Cards never expire." / "WHEN a Gift_Card is unused for 12 months, THE Shop_API SHALL set its status to `void`."
ISSUE: 4.1 says cards never expire. 4.2 voids unused cards after 12 months, and a void card cannot be redeemed (3.2). Both cannot hold.
OPTIONS:
  A) 4.1: THE Shop_API SHALL keep a Gift_Card balance unchanged until the Gift_Card is voided under 3.1 or 4.2.
  B) 4.2: THE Shop_API SHALL NOT change Gift_Card status because of unused time.

ID: F3
TYPE: AMBIGUITY
SEVERITY: medium
AFFECTS: Requirement 2.2
QUOTE: "THE Shop_API SHALL redeem gift cards promptly."
ISSUE: "Promptly" has no measurable target, so a test cannot fail on it.
OPTIONS:
  A) 2.2: THE Shop_API SHALL respond to a redemption request within 2 seconds for 95% of requests.
  B) 2.2: THE Shop_API SHALL respond to a redemption request within 500 milliseconds for 99% of requests.

ID: F4
TYPE: INCONSISTENCY
SEVERITY: medium
AFFECTS: Requirement 1.1, 2.3
QUOTE: "value of 10–500 dollars" / "accept Gift_Cards with a balance up to 1000 dollars"
ISSUE: Purchase caps a balance at 500 dollars, so the 1000 limit in 2.3 can never be reached. The two limits differ, and no behavior is given above 1000.
OPTIONS:
  A) 2.3: THE Shop_API SHALL accept Gift_Cards with a balance up to 500 dollars.
  B) 1.1: WHEN a shopper buys a Gift_Card with a value of 10–1000 dollars, THE Shop_API SHALL charge the Payment_Provider and create an `active` Gift_Card with that balance.

ID: F5
TYPE: EDGE
SEVERITY: high
AFFECTS: Requirement 2.1
QUOTE: "THE Shop_API SHALL subtract the Cart subtotal from the Gift_Card balance."
ISSUE: The case where the Cart subtotal is greater than the balance is not covered, so the balance could go negative. The spec also gives the balance in dollars and the subtotal in cents.
OPTIONS:
  A) 2.5: IF the Cart subtotal exceeds the Gift_Card balance, THEN THE Shop_API SHALL set the balance to 0 cents and return the remaining amount due in cents.
  B) 2.5: IF the Cart subtotal exceeds the Gift_Card balance, THEN THE Shop_API SHALL return HTTP 409 with error `insufficient_balance` and leave the balance unchanged.

ID: F6
TYPE: FAILURE
SEVERITY: medium
AFFECTS: Requirement 1.1
QUOTE: "THE Shop_API SHALL charge the Payment_Provider and create an `active` Gift_Card with that balance."
ISSUE: Only the success path is given. A declined charge or an unreachable Payment_Provider is not covered.
OPTIONS:
  A) 1.3: IF the Payment_Provider declines or fails the charge, THEN THE Shop_API SHALL return HTTP 402 with error `payment_failed` and create no Gift_Card.
  B) 1.3: IF the Payment_Provider does not answer within 10 seconds, THEN THE Shop_API SHALL return HTTP 504 with error `payment_timeout` and create no Gift_Card.

ID: F7
TYPE: EDGE
SEVERITY: medium
AFFECTS: Requirement 1.1
QUOTE: "a value of 10–500 dollars"
ISSUE: No behavior is given for a value outside 10–500 or a value that is not a whole number of dollars.
OPTIONS:
  A) 1.4: IF the purchase value is outside 10–500 dollars or not a whole number, THEN THE Shop_API SHALL return HTTP 400 with error `invalid_amount` and not charge the Payment_Provider.

ID: F8
TYPE: EDGE
SEVERITY: medium
AFFECTS: Requirement 2.1, 5.1
QUOTE: "THE Shop_API SHALL subtract the Cart subtotal from the Gift_Card balance."
ISSUE: Two redemptions of the same code at the same time are not covered. Both could read the same balance, so the balance could be wrong and the ledger old values could be wrong.
OPTIONS:
  A) 2.6: WHEN two redemptions of one code run at the same time, THE Shop_API SHALL apply them one after the other so the balance never falls below 0 cents.
  B) 2.6: WHEN a redemption of a code runs while another redemption of that code is in progress, THE Shop_API SHALL return HTTP 409 with error `card_busy`.

ID: F9
TYPE: EDGE
SEVERITY: low
AFFECTS: Requirement 5.1, 4.2
QUOTE: "append a ledger entry with the code, old value, new value, actor id, and UTC timestamp"
ISSUE: A change made by the 12-month void in 4.2 or by card creation has no staff or shopper actor and no old value. The ledger fields are not defined for these cases.
OPTIONS:
  A) 5.3: WHEN a change has no user actor, THE Shop_API SHALL write the actor id `system` in the ledger entry.
```

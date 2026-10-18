# Analyst round 1 (FULL) — raw output

Model: claude-sonnet-5-5. Tools: Read, Glob, Grep, SubagentHandback.

ID: F1
TYPE: INCONSISTENCY
SEVERITY: high
AFFECTS: Requirement 4.1, Requirement 4.2
QUOTE: "THE Shop_API SHALL keep Gift_Card balances forever; Gift_Cards never expire."
ISSUE: 4.1 says cards never expire. 4.2 voids a card after 12 months unused, which is expiry. Both cannot hold.
OPTIONS:
  A) 4.2: WHEN a Gift_Card is unused for 12 months, THE Shop_API SHALL leave its status `active` and its balance unchanged.
  B) 4.1: THE Shop_API SHALL keep a Gift_Card balance until the card has been unused for 12 months, then 4.2 applies.

ID: F2
TYPE: ASSUMPTION
SEVERITY: medium
AFFECTS: Requirement 3.1
QUOTE: "WHEN a staff member voids a Gift_Card through the Merchant_Portal, THE Shop_API SHALL set the Gift_Card status to `void`."
ISSUE: Merchant_Portal is not in the Glossary. shop/api.py has no void route, staff identity or auth. Design cannot tell how a void request reaches Shop_API.
OPTIONS:
  A) NEEDS_OWNER: What is the Merchant_Portal (separate system or a Shop_API route)? What is the void request interface (method, path) and how is staff identity checked?

ID: F3
TYPE: AMBIGUITY
SEVERITY: medium
AFFECTS: Requirement 2.2
QUOTE: "THE Shop_API SHALL redeem gift cards promptly."
ISSUE: "promptly" has no measurable target. A test cannot fail on it.
OPTIONS:
  A) 2.2: THE Shop_API SHALL return the redemption response within 2 seconds for 95% of requests.
  B) 2.2: Delete this criterion (no latency target is needed).

ID: F4
TYPE: INCONSISTENCY
SEVERITY: medium
AFFECTS: Requirement 1.1, Requirement 2.3
QUOTE: "THE Shop_API SHALL accept Gift_Cards with a balance up to 1000 dollars."
ISSUE: 1.1 caps a new card at 500 dollars, and no requirement adds balance. A balance of 501-1000 dollars cannot exist. Behavior above 1000 is also unstated.
OPTIONS:
  A) 2.3: Delete this criterion (the 1.1 cap of 500 dollars already bounds balances).
  B) 2.3: IF a Gift_Card balance is above 1000 dollars, THEN THE Shop_API SHALL reject redemption with HTTP 422 and error `balance_too_large`.

ID: F5
TYPE: EDGE
SEVERITY: medium
AFFECTS: Requirement 2.1
QUOTE: "THE Shop_API SHALL subtract the Cart subtotal from the Gift_Card balance."
ISSUE: The case where subtotal exceeds balance is unspecified; the balance would go negative. Units differ: Cart.subtotal_cents is in cents, but 1.1 and 2.3 use dollars.
OPTIONS:
  A) 2.5: IF the Cart subtotal exceeds the Gift_Card balance, THEN THE Shop_API SHALL reject redemption with HTTP 422 and error `insufficient_balance`, leaving the balance unchanged.
  B) 2.5: WHEN the Cart subtotal exceeds the Gift_Card balance, THE Shop_API SHALL set the balance to 0 cents and return the remaining amount in cents.

ID: F6
TYPE: FAILURE
SEVERITY: medium
AFFECTS: Requirement 1.1
QUOTE: "THE Shop_API SHALL charge the Payment_Provider and create an `active` Gift_Card with that balance."
ISSUE: No behavior for a failed or timed-out charge, or a value outside 10-500 dollars. Design must guess whether a card is created.
OPTIONS:
  A) 1.3: IF the Payment_Provider charge fails, THEN THE Shop_API SHALL return HTTP 402 with error `payment_failed` and create no Gift_Card.
  B) 1.3: IF the value is outside 10-500 dollars, THEN THE Shop_API SHALL return HTTP 400 with error `bad_value` and not charge the Payment_Provider.

ID: F7
TYPE: EDGE
SEVERITY: medium
AFFECTS: Requirement 2.1, Requirement 5.1
QUOTE: "THE Shop_API SHALL subtract the Cart subtotal from the Gift_Card balance."
ISSUE: Two concurrent redemptions of one card, or a repeat redemption of the same Cart, are unspecified. The balance could be spent twice.
OPTIONS:
  A) 2.6: WHEN two redemptions of one Gift_Card run at the same time, THE Shop_API SHALL apply them one after the other so the final balance is never below 0 cents.

ID: F8
TYPE: EDGE
SEVERITY: low
AFFECTS: Requirement 5.1, Requirement 4.2
QUOTE: "THE Shop_API SHALL append a ledger entry with the code, old value, new value, actor id, and UTC timestamp."
ISSUE: Actor id is undefined for system changes such as the 12-month void. The old value is undefined at card creation.
OPTIONS:
  A) 5.3: WHERE a change has no staff or shopper actor, THE Shop_API SHALL record the actor id `system` in the ledger entry.

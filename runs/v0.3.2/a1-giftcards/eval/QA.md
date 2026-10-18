# QA log

## spec-analyze — round 1 repair (no question)
- F6: A and B close different gaps (charge failure vs out-of-range value) → split into F6a (A) and F6b (B). Each has one option → A | Defer.
- F7: A and B close different gaps (unknown code vs already void) → split into F7a, F7b. Each → A | Defer.
- F8: option B is `NEEDS_OWNER` next to a concrete A. Analyst rule says NEEDS_OWNER is a sole option. Kept as A | B | Defer.
- F5: ISSUE also names concurrent redemption, with no option. Not split (no option to split); left for recheck.
- F9: low, but NEEDS_OWNER → asked (skill: owner question at any severity).

## Q1 (Requirement 4)
- F1 [high INCONSISTENCY] 4.1 vs 4.2: A) 4.2 keeps card `active`, balance unchanged after 12 months no redemption | B) 4.1 card `active` until staff void or 12 months | Defer
- Answer: A (Script: high/medium → option A)

## Q2 (Requirement 3)
- F2 [medium ASSUMPTION, NEEDS_OWNER] What is Merchant_Portal; which route and staff auth for void? Options: answer | Defer
- F7a [medium EDGE] A) 3.3 void unknown code → 404 `unknown_card` | Defer
- F7b [medium EDGE] A) 3.4 void already-void card → 200, no ledger entry | Defer
- Answers: F2 → NEEDS_OWNER most conservative concrete value: Merchant_Portal = staff client that sends `POST /gift-cards/{code}/void`; caller identity in `ctx["actor"]` = {"id", "role"}; non-`staff` role → HTTP 403 `forbidden`. F7a → A. F7b → A.

## Q3 (Requirement 2)
- F3 [medium AMBIGUITY] A) 2.2 within 2 seconds for 95% of redemption requests | B) delete 2.2 | Defer
- F4 [medium CONFLICT] A) 2.3 balance > 1000 dollars → 422 `balance_too_high` | B) delete 2.3 | Defer
- F5 [high EDGE] A) 2.5 subtotal > balance → 422 `insufficient_balance`, balance unchanged | B) 2.5 balance → 0, return remainder | Defer
- Answers: A, A, A

## Q4 (Requirement 1)
- F6a [medium FAILURE] A) 1.3 charge fails → 402 `payment_failed`, no Gift_Card | Defer
- F6b [medium FAILURE] A) value outside 10–500 dollars → 400 `bad_value`, no charge | Defer
- Answers: A, A

## Q5 (Requirement 5)
- F8 [medium EDGE] A) 5.3 creation old value `null`; system changes actor `system` | B) NEEDS_OWNER | Defer
- F9 [low ASSUMPTION, NEEDS_OWNER] What is the Ledger store and where does the actor id come from? Options: answer | Defer
- Answers: F8 → A. F9 → NEEDS_OWNER most conservative concrete value: Ledger = append-only list at `ctx["ledger"]`; actor id = `ctx["actor"]["id"]`.

## Q6 (Requirement 2)
- F10 [medium INCONSISTENCY, NEEDS_OWNER] Which flow raises a balance above 500 dollars? If none, remove 2.3? Options: answer | Defer
- Answer: NEEDS_OWNER most conservative concrete value: no such flow; keep 2.3 as a guard (owner chose it in F4; removal is the less conservative change). No text change.

## Q7 (Requirement 1, 5)
- F11 [medium CONFLICT, NEEDS_OWNER] Does Payment_Provider support refund? Name and signature? Else write the Ledger entry before the charge? Options: answer | Defer
- Answer: NEEDS_OWNER most conservative concrete value: Payment_Provider has `charge(amount_cents) -> charge_id` and `refund(charge_id)`; refund the charge when the Ledger write fails after it (shopper keeps no loss). New 1.7.

## Q8 (Requirement 3)
- F12 [medium CONFLICT] non-staff + unknown code on void: A) 3.6 → 403 `forbidden` | B) 3.6 → 404 `unknown_card` | Defer
- F13 [medium CONFLICT] void card + 2.3/2.5 condition: A) → 409 `card_void` | B) → 422 per 2.3/2.5 | Defer
- Answers: A, A

## Q9 (Requirement 2, 4, 1) — VERIFY resolve
- F14 [medium CONFLICT] 2.3 vs 2.5 precedence: A) 2.7 → `balance_too_high` | B) 2.7 → `insufficient_balance` | Defer
- F15 [medium INCONSISTENCY] single option (repair → A | Defer): A) 4.2 scoped to `active` cards | Defer
- F16 [medium FAILURE] A) 1.8 refund fails → 503 `refund_failed` | B) NEEDS_OWNER | Defer
- Answers: A, A, A
- F17 [low AMBIGUITY] → not asked (low in VERIFY → `## Open Questions`).

## Q10 (spec-new step 1) `docs/specs/gift-cards/` exists: Resume | New name
- Answer: Resume (Script)

## Q11 (gate: design) `design.md: 4 components, 12 properties`: Approve | Request changes
- Answer: Approve (Script)

## Q12 (gate: tasks) `tasks.md: 5 leaves, 4 waves`: Approve | Request changes
- Answer: Approve (Script)


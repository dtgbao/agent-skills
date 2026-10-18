# QA log

## spec-analyze round 1 (4 AskUserQuestion calls, grouped by requirement)

Call 1 — Requirement 1
- Q (F6, medium): Charge failure / bad value for 1.1? Options: A) 1.3 payment_failed 402 | B) 1.3 bad_value 400 | Defer → **A** (script: high/medium → A)

Call 2 — Requirement 2
- Q (F3, medium): "promptly" in 2.2? A) within 2 s for 95 % | B) delete | Defer → **A**
- Q (F4, medium): 2.3 1000-dollar cap vs 1.1 500 cap? A) delete 2.3 | B) reject >1000 with 422 | Defer → **A**
- Q (F5, medium): subtotal > balance? A) 422 insufficient_balance | B) set to 0, return remainder | Defer → **A**
- Q (F7, medium): concurrent redemption? A) serialize, balance never below 0 | Defer → **A**

Call 3 — Requirement 3
- Q (F2, medium, NEEDS_OWNER): What is Merchant_Portal, what is the void interface, how is staff checked? → **Conservative concrete value (logged):** no separate portal; void is a Shop_API route `POST /gift-cards/<code>/void`; caller identity = request field `actor` = `{"id", "role"}`; only role `staff` may void; any other caller → HTTP 403 `forbidden`, status unchanged.

Call 4 — Requirement 4
- Q (F1, high): 4.1 never expire vs 4.2 void after 12 months? A) 4.2 keeps card active | B) 4.1 balance kept until 12 months | Defer → **A**

Low, deferred without asking: F8.

## spec-analyze round 2 (2 AskUserQuestion calls)

Call 5 — Requirement 3
- Q (F9, medium): void card + low balance → 409 or 422? A) 3.4 card_void first | B) 3.4 insufficient_balance | Defer → **A**

Call 6 — Requirement 5
- Q (F10, high): ledger fails after charge? A) 5.3 refund, no card | B) 5.3 ledger before charge | Defer → **A**

## spec-new (resume)

- Q (step 1): `docs/specs/gift-cards/` exists. Resume | New name → **Resume** (script)

- Gate design — shown: `design.md: 4 components, 6 properties`. Approve | Request changes → **Approve** (script)
- Gate tasks — `check-tasks` RESULT: PASS; shown: `tasks.md: 5 leaves, 4 waves`. Approve | Request changes → **Approve** (script)

## spec-run

- Mode: `--mode waves` given → not asked.

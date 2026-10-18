# spec-analyze apply log

## Round 1 (N0 = 12)
- 1.3 ← F6a. Merge: narrowed "declines or fails" to "declines the charge or returns an error", because a timeout is now 1.5 (F6b); keeps the two cases exclusive.
- 1.4 ← F7 as given.
- 1.5 ← F6b. New-number clash (analyst gave 1.3, F7 holds 1.4) → renumbered to 1.5.
- 2.2 ← F3 A (supersedes "promptly"; replaced).
- 2.3 ← F4 A (supersedes 1000-dollar limit; replaced).
- 2.5 ← F5 A, 2.6 ← F8 A.
- 3.1 ← F1 NEEDS_OWNER answer (Merchant_Portal removed; route `POST /gift-cards/<code>/void`).
- 3.3 ← F1 NEEDS_OWNER answer, staff check (new behavior → new criterion).
- 4.1 ← F2 A (supersedes "never expire"; replaced).
- F9 low → `## Open Questions`.
- EARS check: every changed criterion one SHALL, ≤40 words, Event/Unwanted/Ubiquitous form. Pass.
- `SPEC edited docs/specs/gift-cards requirements` run (requirements was approved). Criteria 12 → 18.

## Round 2
- 2.1 ← F11 A (replaced; supersedes old 2.1).
- 4.1 ← F10 A. Dropped trailing clause "so a card unused for 12 months keeps its full balance until voided under 4.2": a second assertion (EARS one-assertion rule) and the main clause already covers it. Logged.
- EARS check pass. `SPEC edited` run. Criteria stay 18.

## Round 3
- Glossary Payment_Provider ← F12 owner answer (interface names `charge`, `refund`).
- 5.3 ← F12 owner answer. Dropped "and return 503 `ledger_unavailable`": 5.2 already covers it. Logged.
- EARS check pass. `SPEC edited` run. Criteria 18 → 19.

## VERIFY 1 resolve + apply
- Glossary Payment_Provider ← F16 owner answer: `charge_id` renamed `charge_ref` (Shop_API makes it first). 5.3 text updated to `charge_ref` (rename only).
- Glossary Actor ← F13 owner answer. 3.3 ← now names `ctx["actor"]["role"]`.
- Glossary Error_Log added: F14 option names "the error log", absent from Glossary (orchestrator fix, logged; concrete value = conservative default).
- 1.6 ← F16 owner answer (new criterion).
- 3.4 ← F15 A.
- 5.4 + 5.5 ← F14 A split: option had two assertions (503 and log write) → two criteria. 5.4 adds "instead of `ledger_unavailable`" to settle the overlap with 5.2. Logged.
- EARS check pass. `SPEC edited` run. Criteria 19 → 23.

## VERIFY 2
- F17 (medium) left after the last allowed VERIFY → `## Open Questions` (skill step 5). Not asked.
- `SPEC edited` run.

## Result
- Growth: N0 = 12 → N = 23 criteria (+92 %). Over 50 % → recommend splitting the spec (for example: purchase + payment recovery; redemption; void/expiry/audit).
- Open Questions: F9 (low), F17 (medium, left after VERIFY).
- F9 proposed number 5.3 now clashes with the new 5.3 → renumbered to 5.6 in Open Questions. Logged.

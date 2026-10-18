# spec-analyze apply log (plugin 0.3.4)

N0 = 12.

## Round 1
- 1.3 ← F6a A. 1.4 ← F7 A. 1.5 ← F6b (analyst gave 1.3; clash with F6a 1.3 and F7 1.4 → renumbered 1.5).
- 2.2 ← F2 A (supersedes "promptly"). 2.3 ← F4 A (supersedes "accept up to 1000"). 2.5 ← F3 A. 2.6 ← F9 A.
- F5 owner answer: interface parts → Glossary `Merchant_Portal` (route `POST /gift-cards/<code>/void`) and `Actor` (`ctx["actor"]`). Behavior part → new 3.3 (non-staff → 403 `forbidden`). 3.1 text unchanged (term now defined).
- 4.1 ← F1 A (supersedes). 4.2 removed (F1 A deletes it). Logged.
- 5.3 ← F8 A minus "and create no Gift_Card" (5.2 already rejects the change). Logged.
- Cross-check: 2 clashes → F10, F11 → resolved (A) → 2.1, 4.1 replaced. See `cross-check.md`.
- EARS: all changed criteria 1 SHALL, ≤40 words. Pass. `SPEC edited` run. Criteria 12 → 18 (+7 new, −1 removed).

## Round 2
- F12 owner answer is a behavior → new 5.4 (503 `refund_failed`).
- F13a owner answer is a behavior → new 5.5 (401 `actor_required`).
- F13b owner answer is a data value → Glossary `Ledger_Entry` (`old` = `null` on creation), not a criterion.
- Cross-check: 2 clashes → F14 (5.4 adds "instead of `ledger_unavailable`"), F15 (5.5 scoped to purchase/redemption). Both A.
- EARS pass. `SPEC edited` run. Criteria 18 → 20.

## Round 3
- 4.1 ← F16 A, minus "so no elapsed time changes the status or balance" (second assertion). Logged.
- Cross-check: no clash. EARS pass. `SPEC edited`. Criteria stay 20.

## VERIFY 1 resolve + apply
- 3.2 ← F18 A. 5.5 ← F17 A. Words: 5.5 = 33 words, ≤40. EARS pass. Cross-check: no clash. `SPEC edited`. Criteria stay 20.

## VERIFY 2
- F19, F20 (medium) left after last VERIFY → `## Open Questions`.

## Result
- Growth N0 = 12 → N = 20 (+67 %). Over 50 % → recommend splitting the spec (e.g. purchase + payment failure; redemption + void; audit).
- Open Questions: F19, F20.

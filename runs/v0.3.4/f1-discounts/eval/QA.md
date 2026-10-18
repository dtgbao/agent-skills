# QA log (plugin 0.3.4)

## Q1 — requirements gate (gate.md step 2)
Shown: `requirements.md: 5 requirements, 25 criteria`
Options: Approve | Request changes | Analyze first (recommended: money domain)
Answer: Analyze first (Script)

## Q2 — analyze round 1, Requirement 1 (spec-analyze step 3)
- F2 (high, NEEDS_OWNER): where does the Code_Book live, and the create function name? → Script rule (most conservative concrete value): `ctx["code_book"]` holds a `shop.discounts.CodeBook`; create = `CodeBook.create(code, kind, amount, min_subtotal, valid_until) -> DiscountCode`; refusal raises `ValueError`. Logged.
- F5 (medium): A | Defer (one non-owner option) → A (Script).

## Q3 — analyze round 1, Requirement 2 and 4
- F1 (high, NEEDS_OWNER): which key gives Current_Date, how does Cart get it? → Script rule: `ctx["today"]`, a `datetime.date`; each Cart method that needs it takes `today: date` as an argument. Logged.
- F4 (medium): A | B | Defer → A (Script).
- F3a (high, repaired from F3, 4.5): A | B | Defer → A (Script).
- F3b (high, repaired from F3, 4.6): A | B | Defer → A (Script).

## (no question) F6 low → deferred without asking (spec-analyze step 3).

## Q4 — analyze round 2, Requirement 2
- F7 (high, NEEDS_OWNER): Cart attach method signature; how is a refusal reason reported? → Script rule (conservative): `Cart.attach_code(code, code_book, today) -> None`; refusal raises `shop.discounts.AttachRefused`, whose `reason` attribute is the reason string; also `Cart.detach_code()`, `Cart.discount_cents(today)`, `Cart.amount_due_cents(today)`. Logged.

## Q5 — verify finding, Requirement 5 (spec-analyze step 5 → 3)
- F8 (medium, repaired: split A into 5.6 + 5.7): A | B | Defer → A (Script).
- F9 low → deferred without asking.

## Q6 — cross-check clash, Requirement 5 (spec-analyze step 4 → step 3)
- F10 (INCONSISTENCY, medium, orchestrator-raised): 5.3 (400) vs 5.6 (500) when both apply. Options: A) context check first (500 wins) | B) body check first (400 wins) | Defer → A (Script: medium → A).

## Q7 — requirements gate, second show
Shown: `requirements.md: 5 requirements, 29 criteria (growth 25 → 29, +16 %)`. Open verify findings: F11 (medium, in Open Questions). Also deferred: F6, F9 (low).
Options: Approve | Request changes | Analyze first
Answer: Approve (Script)

## Q8 — design gate
Shown: `design.md: 3 components, 7 properties`
Options: Approve | Request changes
Answer: Approve (Script)

## Q9 — tasks gate
`check-tasks`: RESULT: PASS (WARN: checkpoints 2 and 4 share waves with later-layer leaves).
Shown: `tasks.md: 6 leaves, 4 waves`
Options: Approve | Request changes
Answer: Approve (Script)

## Q10 — spec-sync step 2, design gate (stale design refined)
Proposed: design.md:73 `PERCENT_RANGE = (1, 90)` → `(1, 50)`; design.md:102 `outside 1–90` → `outside 1–50`.
Shown: `design.md: 3 components, 7 properties`
Options: Approve | Request changes
Answer: Approve (Script: design gate Approve)

## Q11 — spec-sync step 5
Shown: `eval/sync-proposal.md` (table + diff).
Options: Apply all | Pick | Cancel
Answer: Apply all (Script)


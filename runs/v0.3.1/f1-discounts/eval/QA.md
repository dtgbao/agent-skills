# QA log

## Q1 — spec-new step 3 / gate (requirements)
Count line: `requirements.md: 5 requirements, 19 criteria`. Recommend Analyze first (money domain).
Options: Approve | Request changes | Analyze first (Recommended)
Answer (Script): **Analyze first**

## Q2 — spec-analyze step 3, round 1, Requirement 1 (F6)
Options: A) 1.6 reject duplicate `code` with ValueError | B) replace record | Defer
Answer (Script "High/medium → option A"): **A**

## Q3 — spec-analyze step 3, round 1, Requirement 2 (F2, F3)
F2: A) order 2.2, 2.3, 2.4, 2.5 | B) order 2.5, 2.2, 2.3, 2.4 | Defer → **A**
F3: A) 400 `bad code` | B) 404 `unknown code` | Defer → **A**

## Q4 — spec-analyze step 3, round 1, Requirements 3/4 (F1 high, F4 NEEDS_OWNER)
F1: A) 4.3 zero-discount precedence | B) narrow 3.1 | Defer → **A**
F4 NEEDS_OWNER: "How does Cart receive Today? `today` argument on its discount method, or Cart holding a reference to `ctx`."
Answer (Script "NEEDS_OWNER → most conservative concrete value"): **`today: datetime.date` argument on `Cart.discount_cents(today)` / `Cart.total_cents(today)`** (pure, no shared ctx reference, testable).

## Q5 — spec-analyze step 3, round 1, Requirement 5 (F5)
Options: A) 200, cart unchanged | B) 404 `no code` | Defer
Answer: **A**

F7 (low) → deferred without asking (skill rule).

## Q6 — spec-analyze step 3, round 2, Requirement 2 (F8)
Options: A) full order 5.2, 2.7, 2.2–2.5 | B) unknown cart + bad code → 404 only | Defer
Answer: **A**. Applied by merging into 2.6 (option A fully covers and supersedes old 2.6; a separate 2.8 would duplicate it). Count stays 25.

## Q7 — gate (requirements), after analyze
Count line: `requirements.md: 5 requirements, 25 criteria · growth 19 → 25 (+32 %)`. Open verify findings: none. Open Questions: F7 (low).
Options: Approve | Request changes | Analyze first
Answer (Script): **Approve**

## Q8 — gate (design)
Count line: `design.md: 3 components, 6 properties`.
Options: Approve | Request changes
Answer (Script): **Approve**

## Q9 — gate (tasks)
`check-tasks` → RESULT: PASS. Count line: `tasks.md: 6 leaves, 4 waves` (3 checkpoints).
Options: Approve | Request changes
Answer (Script): **Approve**
Then told user: `/sdd:spec-run discount-codes`.

## Q10 — spec-sync step 2, gate (design, stale)
Refinement: design.md percent bound 90 → 50 in 4 places (interface sketch `PERCENT_MAX`, Data Models, Property 5, Testing Strategy row 1). Count line: `design.md: 3 components, 6 properties`.
Options: Approve | Request changes
Answer (Script "Design gate: Approve"): **Approve**

## Q11 — spec-sync step 5
Proposal: `eval/sync-proposal.md` (edit 1.1, 3.2; untick 1.1, 1.2, 3.2, groups 1, 3, checkpoints 2, 4, 6).
Options: Apply all | Pick | Cancel
Answer (Script): **Apply all**


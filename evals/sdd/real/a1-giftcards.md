## Script (a1-giftcards)

The spec `docs/specs/gift-cards/` exists. Requirements are approved. Design and tasks are pending.

Commands:
1. `/sdd:spec-analyze gift-cards`
2. `/sdd:spec-new gift-cards` (resume)
3. `/sdd:spec-run gift-cards --mode waves --optional`

Answers:
- spec-analyze: high/medium → option A. `NEEDS_OWNER` → the most conservative concrete value, log it. Close step: deferred high/medium → same rule. Split spec → Continue.
- spec-new: resume runs with no question (named dir). Every gate: Approve.
- spec-run: failed leaf → Retry once, then Skip. Red checkpoint → Stop. Counterexample → fix implementation.

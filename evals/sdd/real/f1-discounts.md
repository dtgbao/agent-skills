## Script (f1-discounts)

Commands:
1. `/sdd:spec-new Requirements-First: add discount codes to carts. A code gives a percent (1–90) or a fixed amount in cents off the subtotal, may need a minimum subtotal, has an expiry date, and a cart holds at most one code.`
2. `/sdd:spec-run <name> --mode waves --optional`
3. Hand edit, as a human: in `requirements.md` change the percent upper bound 90 → 50. Text only. Touch no other file.
4. `/sdd:spec-sync <name>`
5. `/sdd:spec-run <name> --mode waves --optional`

Answers:
- Requirements gate: first "Analyze first". High/medium → option A. `NEEDS_OWNER` → pick the most conservative concrete value, log it. Analyze Close step: deferred high/medium → same rule. Split spec → Continue. Then "Approve".
- Design gate, tasks gate: Approve.
- spec-run: failed leaf → Retry once, then Skip. Red checkpoint → Untick leaf, then Stop. Counterexample → fix implementation.
- spec-sync: Apply all.

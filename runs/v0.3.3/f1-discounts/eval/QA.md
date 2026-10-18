# QA log

## Q1 — requirements gate (gate.md step 2)
Shown: `requirements.md: 5 requirements, 24 criteria`
Options: Approve | Request changes | Analyze first (recommended: money domain)
Answer: Analyze first (Script: first "Analyze first")

## Q2 — analyze round 1, Requirement 1 (spec-analyze step 3)
- F3 (medium, NEEDS_OWNER): Code_Registry type, add/lookup names, ctx["codes"] type, module? → UNSCRIPTED value per Script rule "NEEDS_OWNER → most conservative concrete value": `shop.discounts.CodeRegistry` object; `add(code: DiscountCode) -> None`; `get(code_string: str) -> DiscountCode | None`; `ctx["codes"]` is a CodeRegistry. Logged.
- F4 (medium): A | B | Defer → A (Script: high/medium → A)

## Q3 — analyze round 1, Requirement 2 (spec-analyze step 3)
- F1 (high, NEEDS_OWNER): Cart method names, how Cart gets registry + Today, error signal, date type? → conservative value (Script rule): explicit args, no hidden state. `Cart.apply_code(code_string, registry, today)`, `Cart.remove_code()`, `Cart.discount_cents(today)`, `Cart.total_cents(today)`; rejection raises `shop.discounts.DiscountError` whose message is the error text; Today and Expiry_Date are `datetime.date`. Logged.
- F2 (medium): A | B | Defer → A
- F5 (medium): A | B | Defer → A

## Q4 — verify finding, Requirement 1 (spec-analyze step 5 → step 3)
- F6 (medium, NEEDS_OWNER): DiscountCode module, constructor, fields; does constructor accept invalid values? → conservative value (Script rule), the analyst's own example: frozen dataclass `shop.discounts.DiscountCode(code_string, kind, value, minimum_subtotal, expiry_date)`; constructor does not validate; only `CodeRegistry.add` raises. Logged.

## Q5 — requirements gate, second show (gate.md step 1–2)
Shown: `requirements.md: 5 requirements, 28 criteria (growth 24 → 28, +17 %)`. Open verify findings: none.
Options: Approve | Request changes | Analyze first
Answer: Approve (Script)

## Q6 — design gate
Shown: `design.md: 3 components, 8 properties`
Options: Approve | Request changes
Answer: Approve (Script)

## Q7 — tasks gate
`check-tasks`: RESULT: PASS (2 WARN: checkpoints 2 and 4 share waves with later-layer leaves).
Shown: `tasks.md: 6 leaves, 4 waves`
Options: Approve | Request changes
Answer: Approve (Script)

## Q8 — spec-sync step 2, design gate (stale design refined)
Proposed: design.md:79 `percent 1–90` → `percent 1–50`. No other design text holds the bound.
Shown: `design.md: 3 components, 8 properties`
Options: Approve | Request changes
Answer: Approve (Script: design gate Approve)

## Q9 — spec-sync step 5
Shown: `eval/sync-proposal.md` table + diff.
Options: Apply all | Pick | Cancel
Answer: Apply all (Script)


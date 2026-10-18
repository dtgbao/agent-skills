# Questions (scripted user) — plugin 0.3.4 rerun

## spec-new step 1 (name)
Not asked. Input not empty; `docs/specs/stock-overbooking/` absent.

## spec-new step 3 (workflow)
Not asked. Input names "Bugfix".

## Q1 — bugfix step 1 (facts)
Question: Repro, current and expected results come from your report. Which existing behavior must stay the same after the fix?
Options: free text (one question, ≤4 allowed).
Answer (Script "Must-hold facts"): "One reserve over stock still raises OutOfStock. qty < 1 raises ValueError. release never makes available exceed initial stock. Cart.remove releases its units."

## Q2 — gate: bugfix.md
Shown: `docs/specs/stock-overbooking/bugfix.md: 0 requirements, 13 criteria` (gate.md count rule; bugfix.md has no `### Requirement` headings. Split: 3 current, 3 expected, 7 unchanged.)
Question: Approve bugfix.md?
Options: Approve | Request changes | Analyze first. Recommendation: none. Rule says ">8 requirements"; this file has 0 requirement headings and 13 criteria, so the rule is unclear here. Not a money/health domain; no ambiguity seen.
Answer (Script "Every gate: Approve"): Approve

## Q3 — gate: design.md
Shown: `docs/specs/stock-overbooking/design.md: 0 components, 2 properties` (no Components and Interfaces section in the bugfix skeleton; Fix names 1 component, Inventory.reserve)
Question: Approve design.md?
Options: Approve | Request changes
Answer (Script): Approve

## Q4 — gate: tasks.md
check-tasks: RESULT: PASS (eval/check-tasks-gate.txt)
Shown: `docs/specs/stock-overbooking/tasks.md: 5 leaves, 3 waves` (4 required, 1 optional; 2 checkpoints)
Question: Approve tasks.md?
Options: Approve | Request changes
Answer (Script): Approve
Then told user: `/sdd:spec-run stock-overbooking`.

# spec-run (cmd 2: --mode single)
Step 1: NO DRIFT, all approved. Step 2: mode from args, not asked. Step 3 scope: 1.1, 1.2, 1.3, 2.1 (4.1* dropped). Step 4: check-tasks PASS.

## Q5 — leaf 1.1 (pin red, S)
Question: Run leaf 1.1? Options: Run | Skip | Stop
Answer (Script): Run

## Q6 — leaf 1.2 (pin green, M)
Question: Run leaf 1.2? Options: Run | Skip | Stop
Answer (Script): Run

## Q7 — leaf 1.3 (pin green, S)
Question: Run leaf 1.3? Options: Run | Skip | Stop
Answer (Script): Run

## Q8 — leaf 2.1 (fix, S)
Question: Run leaf 2.1? Options: Run | Skip | Stop
Answer (Script): Run

# spec-run (cmd 3: --mode single --optional)
Step 1 NO DRIFT; step 2 mode from args; step 3 scope: 4.1* only (pin 1.1 is `[x]`, so the "pin after fix" drop did not apply); step 4 PASS.

## Q9 — leaf 4.1* (stateful test, M)
Question: Run leaf 4.1? Options: Run | Skip | Stop
Answer (Script): Run

# Questions (scripted user)

## Q1 — spec-new step 3 (workflow)
Not asked. Input names "Bugfix". Step 3: "Input names one → use it."

## Q2 — bugfix workflow step 1 (facts)
Question: Which behavior must hold after the fix (must-hold facts)? Repro, current and expected are implied by the input.
Options: free text.
Answer (Script): "One reserve over stock still raises OutOfStock. qty < 1 raises ValueError. release never makes available exceed initial stock. Cart.remove releases its units."

## Q3 — gate: bugfix.md
Shown: `docs/specs/cart-oversell/bugfix.md: 0 requirements, 11 criteria (3 current, 3 expected, 5 unchanged)`
Question: Approve bugfix.md?
Options: Approve | Request changes | Analyze first (not recommended: 11 items but no money/health domain, no ambiguity seen)
Answer (Script "Every gate: Approve"): Approve

## Q4 — gate: design.md
Shown: `docs/specs/cart-oversell/design.md: 0 components, 2 properties` (Fix names 1 component: Inventory.reserve; bugfix-design skeleton has no Components and Interfaces section)
Question: Approve design.md?
Options: Approve | Request changes
Answer (Script): Approve

## Q5 — gate: tasks.md
check-tasks: RESULT: PASS (eval/check-tasks-1.txt)
Shown: `docs/specs/cart-oversell/tasks.md: 4 leaves, 3 waves` (3 required + 1 optional, 2 checkpoints)
Question: Approve tasks.md?
Options: Approve | Request changes
Answer (Script): Approve
Then told user: `/sdd:spec-run cart-oversell`.

# spec-run (cmd 2: --mode single)
Step 2 mode: not asked (`--mode single` given). Step 3 scope: 1.1, 1.2, 2.1 (4.1* dropped, no `--optional`).

## Q6 — leaf 1.1 (exploration pin, S)
Question: Run leaf 1.1? Options: Run | Skip | Stop
Answer (Script "each leaf → Run"): Run

## Q7 — leaf 1.2 (preservation pins, M)
Question: Run leaf 1.2? Options: Run | Skip | Stop
Answer (Script): Run

## Q8 — leaf 2.1 (fix, S)
Question: Run leaf 2.1? Options: Run | Skip | Stop
Answer (Script): Run

# spec-run (cmd 3: --mode single --optional)
Step 2: not asked (`--mode single`). Step 3 scope: 4.1* only (1.1 is `Expect: red` pin with `[x]` fix leaf 2.1 → already `[x]`, not in scope anyway; rule "pin after fix" did not trigger since 1.1 is `[x]`).

## Q9 — leaf 4.1* (optional API test, S)
Question: Run leaf 4.1? Options: Run | Skip | Stop
Answer (Script): Run

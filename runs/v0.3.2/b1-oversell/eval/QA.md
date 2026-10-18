# QA log

## Q1 — spec-new step 1 (name)
Check: `docs/specs/reserve-oversell/` exists? No → no question asked. Name = `reserve-oversell`.

## Q2 — bugfix workflow step 1 (Facts)
Question: Which behavior must stay unchanged after the fix?
Implied by input (no question): repro (stock 5, A adds 3, B adds 3), current (both succeed, available -1), expected (second add refused).
Options: (free text)
Answer (Script, Must-hold facts): "One reserve over stock still raises OutOfStock. qty < 1 raises ValueError. release never makes available exceed initial stock. Cart.remove releases its units."

## Q3 — gate: bugfix.md (requirements phase)
Shown: `docs/specs/reserve-oversell/bugfix.md: 0 requirements, 14 criteria` (4 Current, 4 Expected, 6 Unchanged; no `### Requirement` headings in bugfix form)
Question: Approve bugfix.md?
Options: Approve | Request changes | Analyze first (not recommended: 14 criteria, no money domain, no ambiguity seen)
Answer (Script, Every gate): Approve

## Q4 — gate: design.md
Shown: `docs/specs/reserve-oversell/design.md: 0 components, 2 properties` (Fix names 1 component: Inventory.reserve; no `###` under a "Components and Interfaces" section in bugfix-design skeleton)
Question: Approve design.md?
Options: Approve | Request changes
Answer (Script, Every gate): Approve

## Q5 — gate: tasks.md
`check-tasks` → RESULT: PASS (24 checks).
Shown: `docs/specs/reserve-oversell/tasks.md: 4 leaves, 3 waves`
Question: Approve tasks.md?
Options: Approve | Request changes
Answer (Script, Every gate): Approve
Then told user: `/sdd:spec-run reserve-oversell`.

## Q6 — spec-run (cmd 2): mode
`--mode single` given → no question.

## Q7 — spec-run (cmd 2): leaf 1.1 (wave 0)
Question: Run leaf 1.1 "Pin the two-cart oversell (exploration)"?
Options: Run | Skip | Stop
Answer (Script, each leaf): Run

## Q8 — spec-run (cmd 2): leaf 1.2 (wave 0)
Question: Run leaf 1.2 "Pin unchanged reserve and release behavior (preservation)"?
Options: Run | Skip | Stop
Answer (Script, each leaf): Run

## Q9 — spec-run (cmd 2): leaf 2.1 (wave 1)
Question: Run leaf 2.1 "Check reserve against available units"?
Options: Run | Skip | Stop
Answer (Script, each leaf): Run

## Q10 — spec-run (cmd 3): mode
`--mode single --optional` given → no question. Scope: 4.1 only (1.1 red pin has `[x]` fix 2.1 → already `[x]`, not in scope).

## Q11 — spec-run (cmd 3): leaf 4.1* (wave 2)
Question: Run leaf 4.1 "Test two carts over the API"?
Options: Run | Skip | Stop
Answer (Script, each leaf): Run

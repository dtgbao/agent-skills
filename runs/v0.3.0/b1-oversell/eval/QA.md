# Q&A log

## Q1 — spec-new / bugfix step 1 (Facts: behavior that must hold)
Question: Which behavior must stay unchanged after the fix?
Options: free text
Answer (Script): "One reserve over stock still raises OutOfStock. qty < 1 raises ValueError. release never makes available exceed initial stock. Cart.remove releases its units."
Note: expected result not stated in input. Taken as implied by "more units than are in stock": cart B's add raises OutOfStock, available stays 2. Not asked (input covers it).

## Q2 — gate: bugfix.md (`bugfix.md: 14 criteria — 4 current, 4 expected, 6 unchanged`)
Options: Approve | Request changes | Analyze first (not recommended: 14 items but one small defect, no ambiguity seen)
Answer (Script): Approve

## Q3 — gate: design.md (`design.md: 1 component, 2 properties`)
Options: Approve | Request changes
Answer (Script): Approve

## Q4 — gate: tasks.md (`tasks.md: 4 leaves, 3 waves`; check-tasks RESULT: PASS)
Options: Approve | Request changes
Answer (Script): Approve
Then told user: `/sdd:spec-run cart-oversell`

## spec-run #1 (`cart-oversell --mode single`)
Step 1 drift: RESULT: NO DRIFT. All phases approved. Step 2 mode: single (flag). Step 3 scope: 1.1, 1.2, 2.1 (2.2 `*` dropped). Step 4 check-tasks: PASS.

## Q5 — leaf 1.1 (wave 0)
Options: Run | Skip | Stop
Answer (Script): Run

## Q6 — leaf 1.2 (wave 0)
Options: Run | Skip | Stop
Answer (Script): Run

## Q7 — leaf 2.1 (wave 1)
Options: Run | Skip | Stop
Answer (Script): Run

Checkpoint 3 (run #1): `pytest -q` → 15 passed. Green → [x].

### Run #1 report
| Leaf | Size | Model | Attempts | Status | Tests | Counterexample |
|---|---|---|---|---|---|---|
| 1.1 | S | haiku | 1 | done | 4 fail (expected red) | none |
| 1.2 | M | sonnet | 1 | done | 8 pass (expected green) | none |
| 2.1 | S | haiku | 1 | done | 15 pass | none |
| 2.2* | M | — | 0 | not in scope (optional, no --optional) | — | — |
| 3 Checkpoint | — | — | — | green | 15 passed | — |

## spec-run #2 (`cart-oversell --mode single --optional`)
Step 1 drift: NO DRIFT, all approved. Step 2 mode: single. Step 3 scope: 2.2 only (all other leaves [x]; `*` kept by --optional; no red pin in scope). Step 4 check-tasks: PASS.

## Q8 — leaf 2.2 (wave 2)
Options: Run | Skip | Stop
Answer (Script): Run

Checkpoint 3 (run #2): leaf above ran → re-run. `pytest -q` → 16 passed. Green → stays [x].

### Run #2 report
| Leaf | Size | Model | Attempts | Status | Tests | Counterexample |
|---|---|---|---|---|---|---|
| 2.2* | M | sonnet | 1 | done | 1 pass (200 examples) | none |
| 3 Checkpoint | — | — | — | green | 16 passed | — |

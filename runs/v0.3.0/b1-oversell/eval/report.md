# b1-oversell eval

Orchestrator: claude-opus-5-5, effort low · Result: PASS

## Plugin load
- Slash command expanded? No. Command 1 came as text relayed from the parent session. No `<command-name>` block. All 3 skills were manual loads from the installed SKILL.md files.
- `${CLAUDE_PLUGIN_ROOT}` resolved by hand: `/Users/baodang/Documents/code/agent-skills/plugins/sdd/shared/scripts/spec.py` (ran OK).
- Agent types `sdd:spec-task-runner` and `sdd:spec-analyst` are in the agent list. Only the runner was used (Script: every gate Approve, so no Analyze).
- Frontmatter: runner frontmatter model is `sonnet`. The passed `model` won: S leaves said "claude-haiku-5-5", M leaves said "claude-sonnet-5-5". Tools: reports show only file edits + Bash test runs.

## Summary
- Spec `docs/specs/cart-oversell` (bugfix). bugfix.md 14 items, design.md 2 properties, tasks.md 4 leaves / 3 waves. check-tasks PASS.
- Root cause: `shop/inventory.py:16` compared qty to initial stock, not to available. Fix: `qty > self.available(sku)` (one line).
- Exploration pin red before fix (4 fail). Preservation pins green before fix (8 pass).
- Run #1 (single): 1.1, 1.2, 2.1 done, optional 2.2 dropped, checkpoint 15 passed.
- Run #2 (single --optional): only 2.2 in scope, done, checkpoint re-run 16 passed. Property 1 test fails on reverted code (checked).
- 4 questions + 4 leaf prompts from the Script. 0 UNSCRIPTED. 0 retries.

## Step trace
| Skill | Step | Action | Done-when held | Evidence |
|---|---|---|---|---|
| spec-new | 1 Name | `cart-oversell`; `docs/specs` absent | yes | `ls docs/specs` → none |
| spec-new | 2 Size | Workflow named → skip | yes | input "Bugfix:" |
| spec-new | 3 Workflow | Bugfix (named) | yes | — |
| spec-new | 4 State | `SPEC init` | yes | `INIT docs/specs/cart-oversell bugfix` |
| bugfix | 1 Facts | Repro/current/expected in input; asked must-hold | yes | QA Q1 |
| bugfix | 2 Investigate | Cause + neighbors (api 409, same-cart double add) | yes | design.md Root Cause |
| bugfix | 3 bugfix.md | 4 current, 4 expected, 6 unchanged | yes | each 1.n has 2.n |
| bugfix | 4 Gate | draft → Approve → approve | yes | QA Q2, `APPROVED requirements` |
| bugfix | 5 design.md | Root Cause, Fix, diff, P1, P2, pins | yes | design.md |
| bugfix | 6 Gate | Approve | yes | QA Q3 |
| bugfix | 7 tasks.md | Bugfix order, pins before fix | yes | check-tasks RESULT: PASS |
| bugfix | 8 Gate | Approve; told `/sdd:spec-run cart-oversell` | yes | QA Q4 |
| spec-run #1 | 1 Load | drift NO DRIFT, all approved | yes | QA |
| spec-run #1 | 2–4 | mode single, scope 1.1/1.2/2.1, check PASS | yes | QA |
| spec-run #1 | 5 Execute | 3 single dispatches, marks [-]→[x], groups [x], checkpoint green | yes | dispatch D1–D3 |
| spec-run #1 | 7 Report | table | yes | QA "Run #1 report" |
| spec-run #2 | 1–4 | NO DRIFT, scope 2.2, PASS | yes | QA |
| spec-run #2 | 5 Execute | 2.2 dispatched, checkpoint re-run green | yes | dispatch D4 |
| spec-run #2 | 7 Report | table | yes | QA "Run #2 report" |

## Dispatches
| # | Leaf/round | Size | Model passed | Attempt | Status | Notes |
|---|---|---|---|---|---|---|
| D1 | 1.1 | S | haiku | 1 | done | red as expected, 4 fail |
| D2 | 1.2 | M | sonnet | 1 | done | 8 pass, Hypothesis 100 examples |
| D3 | 2.1 | S | haiku | 1 | done | 15 pass; cited line 18 (real 16) |
| D4 | 2.2* | M | sonnet | 1 | done | 200 examples; catches revert |

## Artifact checks
| Artifact | Done-when item | Pass/Fail | Evidence |
|---|---|---|---|
| bugfix.md | repro exact | Pass | Introduction steps 1–4 |
| bugfix.md | every 1.n has 2.n, same condition | Pass | 1.1–1.4 ↔ 2.1–2.4 |
| bugfix.md | Unchanged covers named + exposed paths | Pass | 3.1–3.4 user facts, 3.5 fit-exact, 3.6 unknown sku |
| bugfix.md | one assertion per item | Pass | defect split into 3 items + API item |
| design.md | Root Cause cites file:line, explains every Current | Pass | inventory.py:16, :18, :11; cart.py:13-14; api.py:20,27 |
| design.md | Fix names component + constraints | Pass | Inventory.reserve only |
| design.md | Call-tree diff | Pass | `diff` block |
| design.md | P1 fix, P2 preservation, Validates | Pass | 2.1–2.3; 3.3, 3.5 |
| design.md | pin tests for every Unchanged | Pass | Regression Strategy |
| tasks.md | check-tasks PASS | Pass | 23 PASS lines |
| code | tests | Pass | `pytest -q` → 16 passed |

## Issues
| ID | Severity | Plugin file:line | Problem | Proposed fix |
|---|---|---|---|---|
| I1 | low | shared/artifacts/bugfix-design.md:3 | Bugfix design does not link `correctness.md`. Its step 2 (`## Criteria Classification` table) is unclear for bugfix. Orchestrator skipped it. | State "Criteria Classification: not used in bugfix" or add it to the skeleton. |
| I2 | low | skills/spec-run/SKILL.md:22 | Group goes `[x]` when in-scope leaves are done. Group 2 showed `[x]` while optional 2.2 was `[ ]` after run #1. | Mark group `[x]` only when all its leaves are `[x]`, or note "optional leaves skipped". |
| I3 | low | shared/workflows/bugfix.md:7 | No rule for a fact the input implies but does not state (expected result). Orchestrator inferred it, did not ask. | Add: "Fact implied by input → state it in bugfix.md Introduction, do not ask." |
| I4 | low | agents/spec-task-runner.md:33 | Haiku run dropped the `NOTES:` prefix on line 2 and cited a wrong line number. Format not enforced. | Add "each NOTES line starts with `NOTES:`; cite lines from `git diff`". |

## Metrics
- Questions: 4 (1 facts, 3 gates) + 4 leaf Run prompts. UNSCRIPTED: 0.
- Dispatches: haiku 2, sonnet 2, opus 0. Analyst rounds: 0.
- Retries/escalations: 0.
- Gates: 3, all Approve. Checkpoints: 2 runs, both green.
- Tests: before 3 pass; after 16 pass, 0 fail.

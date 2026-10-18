# b1-oversell-v032 eval

Orchestrator: Opus 5.5 (claude-opus-5-5), effort low · Result: PASS

## Plugin load
- Slash command expanded? No. The task came from a parent session as plain text, with no `<command-name>` block. All 3 commands ran as `manual load` (eval/commands.md).
- `${CLAUDE_PLUGIN_ROOT}` resolved: `/Users/baodang/Documents/code/agent-skills/plugins/sdd/shared/workflows/bugfix.md`.
- Agent types `sdd:spec-task-runner` and `sdd:spec-analyst` were both in the agent list. `spec-task-runner` was used 4 times. `spec-analyst` was not used (all gates: Approve, no Analyze first).
- Frontmatter model applied: the runners said they ran as `claude-sonnet-5-5` when `model: sonnet` was passed, and as `claude-haiku-5-5` when `model: haiku` was passed. Tools: the runners used only Read/Write/Bash-type actions in their own `Files`.

## Summary
- Spec `docs/specs/reserve-oversell/` (bugfix workflow): bugfix.md (14 items), design.md (2 properties), tasks.md (4 leaves, 3 waves). All 3 phases are `approved`. Drift: none.
- Root cause: `shop/inventory.py:18` compares qty to the initial stock, not to the available stock. Fix: one line, `qty > self.available(sku)`.
- Exploration pin 1.1 was red before the fix (3 fail) and green after. Preservation pin 1.2 was green before and after.
- 4 dispatches, all `done` on attempt 1. 0 retries. Each report came through a SubagentHandback message, and spec-run step 5 tells the orchestrator to expect this.
- Final suite: 14 passed. Nothing committed.

## Step trace
| Skill | Step | Action | Done-when held | Evidence |
|---|---|---|---|---|
| spec-new | 1 Name | `reserve-oversell`, dir absent | yes | eval/QA.md Q1 |
| spec-new | 2 Size | Bugfix named, so a spec is used | yes | input "Bugfix:" |
| spec-new | 3 Workflow | Bugfix (named in input) | yes | no question |
| spec-new | 4 State | `SPEC init ... bugfix` | yes | `INIT docs/specs/reserve-oversell bugfix` |
| bugfix | 1 Facts | repro/current/expected implied; must-hold asked | yes | QA Q2, bugfix.md Introduction |
| bugfix | 2 Investigate | traced reserve → Cart.add → api 409 branch | yes | design.md Root Cause, 4 file:line cites |
| bugfix | 3 Draft bugfix.md | 4 Current, 4 Expected, 6 Unchanged | yes | 1.n↔2.n same condition; 3.5/3.6 split for one assertion each |
| bugfix | 4 Gate | draft → Approve → approve | yes | QA Q3, `APPROVED requirements` |
| bugfix | 5 Draft design.md | Root Cause, Fix, diff call tree, P1/P2, Regression Strategy | yes | design.md |
| bugfix | 6 Gate | Approve | yes | QA Q4, `APPROVED design` |
| bugfix | 7 Draft tasks.md | pins → fix → checkpoint → optional test → checkpoint | yes | `check-tasks` RESULT: PASS |
| bugfix | 8 Gate | Approve; told user `/sdd:spec-run reserve-oversell` | yes | QA Q5, `APPROVED tasks` |
| spec-run (cmd 2) | 1 Load | drift: NO DRIFT; all approved | yes | eval/run-cmd2.md |
| spec-run (cmd 2) | 2 Mode | `--mode single` | yes | QA Q6 |
| spec-run (cmd 2) | 3 Scope | 1.1, 1.2, 2.1; 4.1* dropped | yes | run-cmd2.md |
| spec-run (cmd 2) | 4 Graph | check-tasks PASS | yes | |
| spec-run (cmd 2) | 5 Execute | 3 leaves Run → done; checkpoints 3 and 5 green | yes | dispatch D1–D3, 13 passed |
| spec-run (cmd 2) | 6 Property failure | 1.1 counterexample is the expected red; no ask | n/a | see I4 |
| spec-run (cmd 2) | 7 Report | table written | yes | run-cmd2.md |
| spec-run (cmd 3) | 1–4 | NO DRIFT; scope 4.1*; check-tasks PASS | yes | run-cmd3.md |
| spec-run (cmd 3) | 5 Execute | 4.1 done; checkpoint 5 re-run green | yes | D4, 14 passed |
| spec-run (cmd 3) | 7 Report | table written; no `[-]` left | yes | run-cmd3.md |

## Dispatches
| # | Leaf/round | Size | Model passed | Attempt | Status | Notes |
|---|---|---|---|---|---|---|
| D1 | 1.1 pin (red) | M | sonnet | 1 | done | 3 fail on unfixed code; shrunk stock=1, ops=[(0,1),(0,1)] |
| D2 | 1.2 pin (green) | M | sonnet | 1 | done | 7 pass |
| D3 | 2.1 fix | S | haiku | 1 | done | 1-line diff at shop/inventory.py:18; 13 pass |
| D4 | 4.1* test | S | haiku | 1 | done | 1 pass; cmd 3 |

## Artifact checks
| Artifact | Done-when item | Pass/Fail | Evidence |
|---|---|---|---|
| bugfix.md | repro exact (state, input, observed) | Pass | Introduction steps 1–3 |
| bugfix.md | every 1.n has 2.n, same condition | Pass | 1.1–1.4 ↔ 2.1–2.4 |
| bugfix.md | Unchanged covers neighbor paths | Pass | 3.1–3.4 user facts; 3.5–3.6 exact-fit boundary from investigation |
| bugfix.md | one observable assertion per item | Pass | 3.5 split into 3.5/3.6 |
| design.md | Root Cause cites file:line, explains every Current item | Pass | inventory.py:18,20,13; cart.py:13-14; api.py:18,23 |
| design.md | Fix names changed components and constraints | Pass | Inventory.reserve only; 4 constraints |
| design.md | Call-tree as diff | Pass | `diff` block |
| design.md | P1 fix check, P2 preservation, with Validates | Pass | 2.1–2.4 / 3.1–3.6 |
| design.md | Regression Strategy names pin tests | Pass | test_oversell_pin.py, test_reserve_preserve.py |
| tasks.md | check-tasks RESULT: PASS | Pass | 24 PASS lines |
| tasks.md | pins before fix; fix deps on every pin | Pass | waves 0→1; deps 2.1: [1.1, 1.2] |
| tests | property tag + ≥100 iterations | Pass | both property tests: tag comment, max_examples=200 |
| spec-run | no `[-]` left; every in-scope leaf `[x]` | Pass | tasks.md all `[x]` after cmd 3 |

## Issues
| ID | Severity | Plugin file:line | Problem | Proposed fix |
|---|---|---|---|---|
| I1 | low | shared/gate.md:5 | The count rule counts `### Requirement` headings. bugfix.md has no such headings, so the count line shows "0 requirements, 14 criteria". | For bugfix.md, count the Current / Expected / Unchanged items, e.g. `bugfix.md: 4 current, 4 expected, 6 unchanged`. |
| I2 | low | shared/gate.md:5 | The design count uses `###` under "Components and Interfaces". The bugfix-design skeleton (shared/artifacts/bugfix-design.md:14-45) has no such section, so the line shows "0 components". | For bugfix design, count the components named in `## Fix`. |
| I3 | medium | shared/scripts/spec.py:59 | `criteria()` also reads Current items (`1.n WHEN ... THEN`). Thus `check-tasks` "every criterion cited" makes leaves cite defect items 1.1–1.4. shared/artifacts/tasks.md does not say this. A first draft that cites only 2.x/3.x fails. | Leave `1.` items out of coverage in bugfix, or write in tasks.md that leaves cite Current items too. |
| I4 | medium | skills/spec-run/SKILL.md:24 | Step 6 says: "Report holds counterexample → follow correctness.md step 5" (ask fix implementation / test / requirement). An `Expect: red` pin that reports `done` with a counterexample is an expected red, but the text does not exempt it. | Add: "Skip for an `Expect: red` pin with STATUS `done`." |
| I5 | low | skills/spec-run/SKILL.md:23 | Cmd 2: checkpoint 5 is below optional leaf 4.1, which was skipped. The checkpoint rule says "once every in-scope leaf above it is `[x]`", so 5 was ticked `[x]` while group 4 stayed `[ ]`. This works, but the rule does not state it, and cmd 3 had to re-run 5. | Write in the rule that a checkpoint with only skipped `*` leaves above it runs and ticks. |

## Metrics
- Questions: 8 asked (1 facts, 3 gates, 4 leaf Run). 0 UNSCRIPTED. 3 no-question checks were logged (name, 2× mode).
- Dispatches: 4 runner (sonnet 2, haiku 2, opus 0). Analyst 0.
- Retries/escalations: 0.
- Gates: 3 (all Approve). Analyze first: not recommended, not chosen.
- Tests: pin 1.1 red before the fix (0/3), then green. Final suite: 14 passed, 0 failed.

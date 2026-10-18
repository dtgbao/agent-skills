# b1-oversell-v033 eval

Orchestrator: claude-opus-5-5, effort low · Result: PASS

## Plugin load
- Slash command expanded? No. The first message came from a parent session as plain text, so all 3 commands ran as `manual load` (eval/commands.md).
- `${CLAUDE_PLUGIN_ROOT}` resolved by hand: `python3 /Users/baodang/Documents/code/agent-skills/plugins/sdd/shared/scripts/spec.py init docs/specs/cart-oversell bugfix` → `INIT docs/specs/cart-oversell bugfix`.
- Agent types `sdd:spec-task-runner` and `sdd:spec-analyst` are both in the agent list. Only the runner was dispatched (no Analyze first).
- Frontmatter: runner default `model: sonnet`. The `model` param overrode it: haiku leaves said "Haiku 5.5 (claude-haiku-5-5)", sonnet leaf said "Sonnet 5.5 (claude-sonnet-5-5)". Runner wrote only its `Files`.

## Summary
- spec-new: name `cart-oversell`, workflow Bugfix (named in input), 3 gates, all Approve. 11 criteria (3 current, 3 expected, 5 unchanged), 2 properties, 4 leaves (1 optional), 3 waves.
- Root cause: `shop/inventory.py:18` (before fix) compared qty with initial stock, not available. Fix: `if qty > self.available(sku):`.
- spec-run cmd 2: 3 leaves (haiku, sonnet, haiku), all done on attempt 1. Exploration pin red before fix (3 fail), green after. Checkpoints 3 and 5: 11 passed.
- spec-run cmd 3 (`--optional`): leaf 4.1* (haiku) done; checkpoint 5 re-run: 13 passed.
- Earlier v032 issue I3 (Current 1.x counted as criteria) is fixed: `spec.py:262` exempts `1.` ids for bugfix. v032 I4 (red pin counterexample) is fixed in spec-run step 6.
- Nothing committed.

## Step trace
| Skill | Step | Action | Done-when held | Evidence |
|---|---|---|---|---|
| spec-new | 1 Name | `cart-oversell`, no existing dir | yes | `ls docs` → none |
| spec-new | 2 Size | Bugfix named → "Named workflow wins"; spec kept though fix is 1 line | yes | input "Bugfix:" |
| spec-new | 3 Workflow | Bugfix, not asked | yes | QA Q1 |
| spec-new | 4 State | `SPEC init` | yes | .spec.json all pending |
| bugfix | 1 Facts | repro/current/expected implied; asked must-hold | yes | QA Q2 |
| bugfix | 2 Investigate | traced api.py → cart.py → inventory.py; neighbor: same-cart path, API | yes | design.md Root Cause |
| bugfix | 3 Draft bugfix.md | 1.1–1.3, 2.1–2.3, 3.1–3.5 | yes | Artifact checks |
| bugfix | 4 Gate | draft → Approve → approved | yes | QA Q3 |
| bugfix | 5–6 design + Gate | design.md, Approve | yes | QA Q4 |
| bugfix | 7–8 tasks + Gate | check-tasks PASS, Approve, told `/sdd:spec-run cart-oversell` | yes | eval/check-tasks-1.txt, QA Q5 |
| spec-run (2) | 1 Load | drift: NO DRIFT, all approved | yes | |
| spec-run (2) | 2 Mode | `single` from args | yes | |
| spec-run (2) | 3 Scope | 1.1, 1.2, 2.1; 4.1* dropped | yes | |
| spec-run (2) | 4 Graph | check-tasks PASS | yes | |
| spec-run (2) | 5 Execute | Run each leaf, `[-]` → dispatch → `[x]`; checkpoints 3, 5 green | yes | QA Q6–Q8, dispatch 1–3 |
| spec-run (2) | 7 Report | table | yes | eval/spec-run-1-report.md |
| spec-run (3) | 1–4 | NO DRIFT, single, scope 4.1*, PASS | yes | QA Q9 |
| spec-run (3) | 5 Execute | 4.1 done; checkpoint 5 re-run (leaf above ran) | yes | eval/checkpoint-5-rerun.txt |
| spec-run (3) | 7 Report | table | yes | eval/spec-run-2-report.md |

## Dispatches
| # | Leaf/round | Size | Model passed | Attempt | Status | Notes |
|---|---|---|---|---|---|---|
| 1 | 1.1 exploration pin | S | haiku | 1 | done | red as expected, 0/3 pass; report via hand-back message |
| 2 | 1.2 preservation pins | M | sonnet | 1 | done | 5/5 green on unfixed code |
| 3 | 2.1 fix | S | haiku | 1 | done | 11/11; one-line diff |
| 4 | 4.1* API test | S | haiku | 1 | done | 2/2 (cmd 3) |

## Artifact checks
| Artifact | Done-when item | Pass/Fail | Evidence |
|---|---|---|---|
| bugfix.md | repro exact (state, input, observed) | Pass | Introduction steps 1–3 |
| bugfix.md | every 1.n has 2.n, same condition | Pass | 1.1/2.1, 1.2/2.2, 1.3/2.3 |
| bugfix.md | Unchanged covers neighbor paths + user facts | Pass | 3.1–3.4 = user facts, 3.5 = within-stock path |
| bugfix.md | one assertion per item | Pass | 2 outcomes of the defect split into 1.1/1.2 |
| design.md | Root Cause cites file:line, explains every Current item | Pass (lines off by 1) | cites `inventory.py:17`; actual check line was :18 (orchestrator error) |
| design.md | Fix names component + constraint | Pass | Inventory.reserve, 4 constraints |
| design.md | Call-tree as diff | Pass | |
| design.md | P1 fix check, P2 preservation, Validates | Pass | P1 → 2.1–2.3, P2 → 3.1–3.5 |
| design.md | Regression Strategy names pins per Unchanged item | Pass | 3.1–3.5 listed |
| tasks.md | check-tasks RESULT: PASS | Pass | eval/check-tasks-1.txt; re-run PASS after both runs |
| .spec.json | all phases approved, no drift at end | Pass | drift: NO DRIFT |
| code | bug fixed | Pass | 13 passed |

## Issues
| ID | Severity | Plugin file:line | Problem | Proposed fix |
|---|---|---|---|---|
| I1 | low | shared/gate.md:7 | Count line rule counts `### Requirement` headings and `###` under Components and Interfaces. bugfix.md and the bugfix design skeleton have neither, so the line reads "0 requirements" / "0 components". | Add bugfix forms: `bugfix.md: 3 current, 3 expected, 5 unchanged` · `design.md: 1 changed component, 2 properties`. |
| I2 | low | shared/artifacts/bugfix-design.md:6 | "Root Cause cites `file:line`" has no check that the line is right. Orchestrator cited `inventory.py:17`; the check was on :18. No step caught it. | Add to Done-when: "each cited `file:line` checked with `grep -n` before gate". |
| I3 | low | shared/artifacts/bugfix-design.md:3 | "Property 1 and 2 cover the criteria" pushes the API criterion 2.3 into Property 1. The pin covers 2.3 with an example test only; the property test checks Cart, not `handle`. | Allow "example-only" criteria in a bugfix design, or say a property may name an example test for an interface-level criterion. |

## Metrics
- Questions: 9 logged (2 not asked per skill rules: workflow, mode), 0 UNSCRIPTED.
- Dispatches: haiku 3, sonnet 1, opus 0. Analyst 0.
- Retries/escalations: 0.
- Gates: 3, all Approve. check-tasks: 3 runs, all PASS. Drift checks: 3, all NO DRIFT.
- Tests: before fix 3 pass + 3 fail (pin red, expected); final 13 pass, 0 fail.

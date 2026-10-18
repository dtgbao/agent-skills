# b1-oversell eval — plugin 0.3.4, reused session

Orchestrator: claude-opus-5-5, effort low · Result: PASS

## Plugin load
- Slash command expanded? No. The commands came as a cross-session message, so all 3 ran as `manual load` (eval/commands.md). I re-read every skill, agent and shared file from disk before use.
- Plugin 0.3.4: `plugin.json` version 0.3.4; the source tree is the same as `~/.claude/plugins/cache/bao-plugins/sdd/0.3.4` (`diff -r` empty, evals aside).
- `${CLAUDE_PLUGIN_ROOT}` resolved by hand: `python3 /Users/baodang/Documents/code/agent-skills/plugins/sdd/shared/scripts/spec.py init docs/specs/stock-overbooking bugfix` → `INIT docs/specs/stock-overbooking bugfix`.
- Agent types `sdd:spec-task-runner` and `sdd:spec-analyst` are in the agent list. Only the runner was dispatched (no Analyze first).
- Frontmatter: runner default `model: sonnet`; the `model` param overrode it. Haiku leaves said "claude-haiku-5-5 (Haiku 5.5)"; sonnet leaves said "Sonnet 5.5 (claude-sonnet-5-5)". Each runner wrote only its `Files` (`git status`: 1 modified source file, 4 new test files).

## Summary
- spec-new: new name `stock-overbooking`, Bugfix workflow (named in input). 3 gates, all Approve. 13 criteria (3 current, 3 expected, 7 unchanged), 2 properties, 5 leaves (1 optional), 3 waves.
- Root cause: `shop/inventory.py:18` tested `qty > self._initial[sku]`. Fix: `qty > self.available(sku)` (one line, confirmed by `git diff`).
- Investigation added 2 neighbor paths this time: one cart that adds twice (1.3/2.3), and the HTTP 409 route as an Unchanged item (3.7). It also added "refused add leaves cart lines unchanged" (3.6).
- spec-run cmd 2: 4 leaves (haiku 3, sonnet 1), all done on attempt 1. The red pin failed 3/3 before the fix. Its counterexample (`s=1, h=1, q=1`) was exempt under spec-run step 6. Checkpoints 3 and 5: 13 passed.
- spec-run cmd 3 (`--optional`): leaf 4.1* (sonnet, stateful test) done. Checkpoint 5 re-run: 14 passed.
- M1 holds: all 5 runner prompts held the cited criterion text, and all 5 NOTES lines named the cited ids. Nothing committed.

## 0.3.4 checks

M1: the runner prompt holds the text of every cited criterion, and the runner NOTES name the criterion ids it covered.

| Leaf | `_Requirements:_` | Criterion lines in prompt | NOTES ids | Held |
|---|---|---|---|---|
| 1.1 | 2.1, 2.2, 2.3 | 3 (eval/prompts/1.1.md) | "Covers 2.1 (…), 2.2 (…), 2.3 (…)" | yes |
| 1.2 | 3.1, 3.2, 3.3, 3.5 | 4 (eval/prompts/1.2.md) | "Covers 3.1, 3.2, 3.3, 3.5" | yes |
| 1.3 | 3.4, 3.6, 3.7 | 3 (eval/prompts/1.3.md) | "Covers 3.4 (…), 3.6 (…), 3.7 (…)" | yes |
| 2.1 | 2.1, 2.2, 2.3 | 3 (eval/prompts/2.1.md) | "Criteria 2.1, 2.2, 2.3 covered by the verify run" | yes |
| 4.1* | 2.1, 2.2, 3.4 | 3 (eval/prompts/4.1.md) | "Covers 2.1 (…), 2.2 (…), 3.4 (…)" | yes |

- Source: `skills/spec-run/SKILL.md:20` ("the text of every criterion in its `_Requirements:_`"). `agents/spec-task-runner.md:8,12-13,37` (caller gives cited criterion text; step 1 Done-when; NOTES "criterion ids covered").
- I built each prompt block with `grep -E '^(<ids>) ' bugfix.md`, so the text is exact. Check: count of criterion lines in each prompt equals count of ids in `_Requirements:_` (5/5).
- Runner step-1 Done-when ("every cited criterion id has a test case or check in your `Verify`"): every NOTES maps each id to a named test, except 2.1 (a code leaf). Its NOTES says the Verify run covers the ids.
- Other 0.3.4 changes (analyst `CHECK` line, spec-analyze steps 3–4) were not exercised: no Analyze first in this Script.

## Step trace
| Skill | Step | Action | Done-when held | Evidence |
|---|---|---|---|---|
| spec-new | 1 Name | `stock-overbooking`; dir absent | yes | QA |
| spec-new | 2 Size | 1-line fix, but Bugfix named → "Named workflow wins" | yes | input "Bugfix:" |
| spec-new | 3 Workflow | Bugfix, not asked | yes | QA |
| spec-new | 4 State | `SPEC init` | yes | INIT line |
| bugfix | 1 Facts | 3 facts implied; asked must-hold (1 question) | yes | QA Q1 |
| bugfix | 2 Investigate | traced api.py:18 → cart.py:13 → inventory.py:18; line refs checked with `grep -n` | yes | design.md Root Cause table |
| bugfix | 3 Draft bugfix.md | 1.1–1.3, 2.1–2.3, 3.1–3.7 | yes | Artifact checks |
| bugfix | 4 Gate | draft → Approve → approved | yes | QA Q2 |
| bugfix | 5–6 design + Gate | design.md, Approve | yes | QA Q3 |
| bugfix | 7–8 tasks + Gate | check-tasks PASS → Approve; told `/sdd:spec-run stock-overbooking` | yes | eval/check-tasks-gate.txt, QA Q4 |
| spec-run (2) | 1–4 | NO DRIFT, all approved; mode from args; scope 1.1–1.3, 2.1; PASS | yes | QA |
| spec-run (2) | 5 Execute | Run → `[-]` → dispatch → `[x]`; group marks; checkpoints 3, 5 | yes | QA Q5–Q8, dispatch 1–4 |
| spec-run (2) | 6 | 1.1 counterexample exempt (red pin, done) | yes | dispatch 1 |
| spec-run (2) | 7 Report | table | yes | eval/spec-run-1-report.md |
| spec-run (3) | 1–4 | NO DRIFT; scope 4.1*; PASS | yes | QA Q9 |
| spec-run (3) | 5 Execute | 4.1 done; checkpoint 5 re-run | yes | eval/checkpoint-5-rerun.txt |
| spec-run (3) | 7 Report | table | yes | eval/spec-run-2-report.md |

## Dispatches
| # | Leaf/round | Size | Model passed | Attempt | Status | Notes |
|---|---|---|---|---|---|---|
| 1 | 1.1 repro pin (red) | S | haiku | 1 | done | 0/3 pass before fix; hand-back message |
| 2 | 1.2 inventory pins (green) | M | sonnet | 1 | done | 4/4 |
| 3 | 1.3 cart + HTTP pins (green) | S | haiku | 1 | done | 3/3 |
| 4 | 2.1 guard fix | S | haiku | 1 | done | 13/13 |
| 5 | 4.1* stateful test | M | sonnet | 1 | done | 1/1 (cmd 3), ~105 s |

## Artifact checks
| Artifact | Done-when item | Pass/Fail | Evidence |
|---|---|---|---|
| bugfix.md | repro exact | Pass | Start / Do / See lines |
| bugfix.md | every 1.n has 2.n, same condition | Pass | 1.1↔2.1, 1.2↔2.2, 1.3↔2.3 |
| bugfix.md | Unchanged covers neighbor paths | Pass | user facts 3.1–3.4; investigation 3.5–3.7 |
| bugfix.md | one assertion per item | Pass | two defect outcomes split 1.1/1.2 |
| design.md | Root Cause file:line explains every Current item | Pass | table rows 1.1–1.3; `inventory.py:18` confirmed by runner and diff |
| design.md | Fix names component + constraints | Pass | Inventory.reserve, 4 constraints |
| design.md | Call-tree as diff | Pass | |
| design.md | P1 fix check / P2 preservation with Validates | Pass | P1 → 2.1–2.3; P2 → 3.1–3.7 |
| design.md | pin per Unchanged item | Pass | Regression Strategy table |
| tasks.md | check-tasks PASS | Pass | at gate and at each spec-run load |
| .spec.json | all approved, no drift at end | Pass | `RESULT: NO DRIFT` |
| code | bug fixed, no regressions | Pass | 14 passed |

## Issues
| ID | Severity | Plugin file:line | Problem | Proposed fix |
|---|---|---|---|---|
| I1 | low | shared/gate.md:7 | The count line counts `### Requirement` headings and `###` under Components and Interfaces. Bugfix artifacts have neither, so the gate shows "0 requirements" and "0 components". (Carried over from 0.3.3.) | Add bugfix forms: `bugfix.md: N current, N expected, N unchanged` · `design.md: N changed components, 2 properties`. |
| I2 | low | shared/gate.md:8 | The Analyze-first recommendation uses ">8 requirements". A bugfix.md has 0 requirement headings (13 criteria here), so the rule does not say whether to recommend it. | Say "requirements (bugfix: criteria)", or give a bugfix limit. |
| I3 | low | agents/spec-task-runner.md:37 | NOTES must "cite file:line from `git diff`". A new file has no diff lines, so 2 of 5 runners wrote "new file, so no git diff". | Allow file:line in new files: "from `git diff`, or from the new file". |
| I4 | low | shared/artifacts/bugfix-design.md:6 | No step checks that the Root Cause `file:line` is correct. This run had correct refs only because I checked with `grep -n`. (Carried over.) | Add to Done-when: "each `file:line` checked with `grep -n`". |

## Metrics
- Questions: 9 logged (name, workflow and mode not asked, per the skill rules). 0 UNSCRIPTED.
- Dispatches: haiku 3, sonnet 2, opus 0. Analyst 0.
- Retries/escalations: 0.
- Gates: 3, all Approve. check-tasks: 4 runs, all PASS. Drift: 3 runs, all NO DRIFT.
- Tests: baseline 3 pass. Before fix: repro 0/3 (red, expected), preservation 7/7. Final: 14 pass, 0 fail.

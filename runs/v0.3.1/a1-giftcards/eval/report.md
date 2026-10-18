# a1-giftcards-v031 eval

Orchestrator: Opus 5.5 (claude-opus-5-5), effort low · Result: PASS

## Plugin load
- Slash command expanded? No. The turn text was `/sdd:spec-analyze gift-cards`, but no skill body arrived. All 3 commands ran as `manual load` (`eval/commands.md`).
- `${CLAUDE_PLUGIN_ROOT}` resolved by hand: `/Users/baodang/Documents/code/agent-skills/plugins/sdd/shared/ears.md`.
- Agent types `sdd:spec-task-runner`, `sdd:spec-analyst`: both available.
- Frontmatter applied: analyst (no model passed) said "Sonnet 5.5 (claude-sonnet-5-5)", which matches frontmatter `sonnet`. Runners said Haiku 5.5 / Sonnet 5.5 / Opus 5.5, which matches the `model` passed. Analyst tools: "Read, Glob, Grep, SubagentHandback" (matches frontmatter).

## Summary
- spec-analyze: 3 FULL/FOCUSED rounds + 1 VERIFY, 13 findings (F1–F13). Criteria grew 12 → 17 (+41.7 %), so no split advice.
- 8 findings applied (option A), 1 NEEDS_OWNER (F2) answered with a conservative value. F8, F13 (low) and F11, F12 (verify, medium) went to Open Questions.
- spec-new resume: design (4 components, 6 properties) and tasks (5 leaves, 4 waves, 2 checkpoints) drafted. Both gates approved. `check-tasks` PASS.
- spec-run waves --optional: 5 dispatches, all `done` on attempt 1. No retries, no counterexamples. Both checkpoints green. 11 tests pass.
- Main gaps: the analyst breaks its own option rules, verify-medium findings get no resolve step, and the skill names no model for the analyst.

## Step trace
| Skill | Step | Action | Done-when held | Evidence |
|---|---|---|---|---|
| spec-analyze | 1 Load | `SPEC drift` → NO DRIFT; N0 = 12 | yes | eval/trace.md |
| spec-analyze | 2 Analyze | D1 FULL → 8 findings | yes | eval/analyst-round-1.md |
| spec-analyze | 3 Resolve | 4 grouped asks; high/medium → A; F2 NEEDS_OWNER → conservative; F8 low deferred | yes | eval/QA.md |
| spec-analyze | 4 Apply | 2.3 removed, 2.2/3.1/4.2 changed, new 1.3/2.4/2.5/3.3; Actor added to Glossary; `SPEC edited` | yes | requirements.md |
| spec-analyze | 5 Recheck | D2 FOCUSED → F9, F10 applied; D3 FOCUSED → NO FINDINGS; D4 VERIFY → F11–F13 to Open Questions; growth reported | yes | analyst-round-2/3/verify.md |
| spec-new | 1 Name | dir exists → Resume; drift NO DRIFT; jump to design | yes | QA.md |
| spec-new | 5 → RF 1 | stack + test cmd from README | yes | README.md |
| spec-new | RF 4 Design | design.md drafted; 17/17 criteria classified; Open Questions decided | yes | design.md |
| spec-new | RF 5 Gate | draft → count line → Approve → `SPEC approve design` | yes | .spec.json |
| spec-new | RF 6 Tasks | tasks.md drafted | yes | `check-tasks` RESULT: PASS |
| spec-new | RF 7 Gate | draft → Approve → `SPEC approve tasks` (baseline 17 criteria) | yes | .spec.json |
| spec-run | 1–4 | drift clean, mode waves (arg), scope 5 leaves incl. `*`, check-tasks PASS | yes | trace.md |
| spec-run | 5 Execute | waves 0–3, wave 2 dispatched in one message; checkpoints 2 and 4 green | yes | dispatch.md D5–D9 |
| spec-run | 6 Property | no counterexample reported | n/a | — |
| spec-run | 7 Report | table below; no `[-]` left | yes | tasks.md |

## Dispatches
| # | Leaf/round | Size | Model passed | Attempt | Status | Notes |
|---|---|---|---|---|---|---|
| D1 | analyze round 1 FULL | — | none (frontmatter sonnet) | 1 | 8 findings | F6/F7 break option rules |
| D2 | analyze round 2 FOCUSED | — | none | 1 | 2 findings | F10 B has 2 SHALL |
| D3 | analyze round 3 FOCUSED | — | none | 1 | NO FINDINGS | rounds stop |
| D4 | analyze VERIFY | — | none | 1 | 3 findings | to Open Questions |
| D5 | 1.1 | S | haiku | 1 | done | |
| D6 | 1.2 | L | opus | 1 | done | |
| D7 | 1.3* | M | sonnet | 1 | done | self-fixed its own red P6 test |
| D8 | 3.1 | M | sonnet | 1 | done | parallel with D7 |
| D9 | 3.2* | M | sonnet | 1 | done | |

## Artifact checks
| Artifact | Done-when item | Pass/Fail | Evidence |
|---|---|---|---|
| requirements.md | every changed criterion: one SHALL, ≤40 words | Pass | 3.4 = 34 words; 2.4 one SHALL |
| requirements.md | deferred → Open Questions with id, type, severity | Pass | F8, F11, F12, F13 |
| design.md | every criterion → component or property | Pass | Criteria Classification 17 rows |
| design.md | interface sketch per new component | Pass | 4 Python sketches |
| design.md | Error Handling per external dependency | Pass | Payment_Provider charge + refund, Ledger |
| design.md | ≥1 Mermaid, `diff` file tree, call trees | Pass | sequenceDiagram; 2 call-tree diffs |
| design.md | Testing Strategy lists every property | Pass | P1–P6, ≥100 |
| design.md | non-functional owner | Pass | 2.2 → GiftCardStore, 3.3 → route |
| design.md | Open Questions decided | Pass | Key design decisions F8, F11, F12, F13 |
| tasks.md | `check-tasks` RESULT: PASS | Pass | 22/22 |
| code | property tag + ≥100 iterations | Pass | 6 tags, `max_examples=100` ×6 |
| run | every in-scope leaf `[x]`, no `[-]` | Pass | tasks.md |

## Issues
| ID | Severity | Plugin file:line | Problem | Proposed fix |
|---|---|---|---|---|
| I1 | medium | agents/spec-analyst.md:34-35 | Analyst breaks its own option rules. F6 A/B close two different gaps. F10 B has two `SHALL`. F7 has a single non-NEEDS_OWNER option. The unchosen F6 B gap (value outside 10–500) left no trace, so design had to invent `bad_value`. | Add an output self-check: "per finding, A and B close the same gap; per option, SHALL count = 1". In spec-analyze step 3, split a multi-gap finding before asking. |
| I2 | medium | skills/spec-analyze/SKILL.md:22 | VERIFY findings of medium severity (F11 refund failure, F12 void unknown code) go to Open Questions with no resolve step. The spec ends with design-blocking gaps, and design decides them silently. | Medium/high VERIFY findings → one more Resolve ask (step 3) before parking. Or the requirements gate shows them as a decision. |
| I3 | medium | skills/spec-analyze/SKILL.md:15 | Step 2 names no `model` for the analyst. The eval rule "pass the model the skill names" has nothing to pass. Frontmatter `sonnet` applied. | State "omit `model` (frontmatter sonnet)" or name `sonnet`, as spec-run does. |
| I4 | low | shared/correctness.md:11, agents/spec-task-runner.md:14 | Runner step 3 points at correctness step 5, which says "in spec-run only" and "test stays unchanged until user picks". The 1.3 runner hit a red P6 run, changed its own test, and reported `COUNTEREXAMPLE: none`. This hides a red run from the orchestrator. | Runner: any red property run → put the counterexample in the report. Allow a self-fix only for a new test file, and only with a NOTES line. |
| I5 | low | skills/spec-run/SKILL.md:23, shared/artifacts/tasks.md | Checkpoint 2 (after group 1) must wait for 1.3, which shares wave 2 with 3.1 (group 3). So the checkpoint ran after layer-3 code had landed and did not isolate layer 1. `check-tasks` does not flag this. | `check-tasks`: warn when a leaf below a checkpoint is in a wave ≤ the last wave above it. Or the tasks rules: a checkpoint sits after the wave that completes its group. |
| I6 | low | shared/artifacts/tasks.md:5 | The running mark for an optional leaf is not defined (`[-]*` vs `[-]`). I used `[-]*`. `check-tasks` accepted it. | Document `[-]*` / `[x]*`. |
| I7 | low | (harness) | The slash command did not expand. All skills ran as manual load. | Check the plugin registration at project scope (the `disable-model-invocation` skills are user-only). |

## Metrics
- Questions: 9 ask calls logged (spec-analyze 6 calls / 9 questions incl. 1 NEEDS_OWNER; spec-new 1 resume + 2 gates). 0 UNSCRIPTED.
- Dispatches: 9 total. sonnet 7 (4 analyst via frontmatter + 3 runners), haiku 1, opus 1.
- Retries/escalations: 0.
- Gates: 2 (design, tasks), both Approve. Checkpoints: 2, both green first run.
- Tests: 11 pass, 0 fail (3 existing + 3 store properties + 5 API).
- Criteria: 12 → 17. Findings: 13 (1 high round 1, 1 high round 2).
- Nothing committed.

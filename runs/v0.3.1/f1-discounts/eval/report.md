# f1-discounts-v031 eval

Orchestrator: claude-opus-5-5, effort low · Result: PASS

## Plugin load
- Slash command expanded? No. Command 1 arrived as task text from the parent session. All 5 Script commands ran as manual load (`eval/commands.md`).
- `${CLAUDE_PLUGIN_ROOT}` resolved by hand to `/Users/baodang/Documents/code/agent-skills/plugins/sdd`, e.g. `/Users/baodang/Documents/code/agent-skills/plugins/sdd/shared/correctness.md` (passed to every runner).
- Agent types `sdd:spec-task-runner` and `sdd:spec-analyst`: both available.
- Frontmatter applied: analyst said "claude-sonnet-5-5. Tools: Read, Glob, Grep, SubagentHandback" (matches `tools: Read, Glob, Grep`, `model: sonnet`). Runners said Sonnet 5.5 (`model: sonnet` passed for Size M).

## Summary
- Spec `docs/specs/discount-codes` built Requirements-First: 5 requirements, 19 → 25 criteria (+32 %), 3 components, 6 properties, 6 leaves, 4 waves, 3 checkpoints.
- Analyze: 4 analyst dispatches (FULL, FOCUSED ×2, VERIFY). 8 findings; 7 applied (option A), F7 low deferred. F4 NEEDS_OWNER → `today` argument.
- Run 1: 6 leaves, all done first try. 17 tests pass.
- Hand edit 90 → 50 → drift found `CHANGED 1.2`, `AFFECTS 1.1 1.2`, `SUSPECT 3.2 tests/test_cart_discount.py:19`. Sync unticked 3 leaves + 2 groups + 3 checkpoints, edited 1.1 and 3.2.
- Run 2: 3 leaves done. Checkpoint 2 went red on 3.2's stale test and was deferred per the rule; green after 3.2. 17 pass, no `90` left in code or tests, `51` rejected.
- All subagent reports came as SubagentHandback messages, not in the Agent tool result (I1).

## Step trace
| Skill | Step | Action | Done-when held | Evidence |
|---|---|---|---|---|
| spec-new | 1 Name | `discount-codes`, dir absent | yes | `ls docs/specs` empty |
| spec-new | 2 Size | named workflow wins | yes | — |
| spec-new | 3 Workflow | Requirements-First from input | yes | — |
| spec-new | 4 State | `SPEC init` | yes | `INIT docs/specs/discount-codes requirements-first` |
| req-first | 1 Context | read README, pyproject, shop/*, tests | yes | stack Python, pytest+Hypothesis |
| req-first | 2 Draft req | 5 req, 19 criteria, Glossary | yes | `requirements.md` |
| gate | 1–3 | draft, ask → Analyze first | yes | QA Q1 |
| spec-analyze | 2 | FULL dispatch | yes | `analyst-round-1.md` (7 findings) |
| spec-analyze | 3 | ask A/B/Defer; F7 low deferred | yes | QA Q2–Q5 |
| spec-analyze | 4 | apply 1.6, 2.6, 2.7, 4.3, 4.4, 5.3 | yes | 25 criteria |
| spec-analyze | 5 | FOCUSED r2 (F8 → merged into 2.6), r3 NO FINDINGS, VERIFY NO FINDINGS, growth 19→25 | yes | `analyst-round-{2,3,verify}.md`, QA Q6 |
| gate | 5 | Approve requirements | yes | `APPROVED requirements`, QA Q7 |
| req-first | 4–5 | design.md (mermaid, diff tree, call trees, classification, 6 properties), gate Approve | yes | QA Q8 |
| req-first | 6–7 | tasks.md, `check-tasks` PASS, gate Approve | yes | `RESULT: PASS`, QA Q9 |
| spec-run #1 | 1–4 | drift none, mode waves, scope 6 leaves incl `*`, check PASS | yes | — |
| spec-run #1 | 5 | waves 0–3; wave 1 and 2 dispatched in one message; checkpoints 2/4/6 green | yes | `run-1.md` |
| hand edit | — | 1.2 `1–90` → `1–50`, requirements.md only | yes | `grep 1–50` |
| spec-sync | 1 | drift | yes | `sync-drift.txt` |
| spec-sync | 2 | design stale → 4 lines 90→50, gate Approve | yes | QA Q10 |
| spec-sync | 3–5 | matrix, evidence, proposal, Apply all | yes | `sync-proposal.md`, QA Q11 |
| spec-sync | 6 | apply, `check-tasks` PASS, approve tasks | yes | phases all `approved`, baseline 1.2 = 1–50 |
| spec-run #2 | 3 | scope 1.1, 1.2, 3.2 | yes | — |
| spec-run #2 | 5 | 1.1 → 1.2 → checkpoint 2 red (3.2 file) deferred → 3.2 → checkpoints 2/4/6 green | yes | `run-2-checkpoint2.txt` |
| spec-run #2 | 7 | report; no `[-]` left | yes | table below |

## Dispatches
| # | Leaf/round | Size | Model passed | Attempt | Status | Notes |
|---|---|---|---|---|---|---|
| D1 | analyst FULL | — | none (default sonnet) | 1 | 7 findings | handback msg |
| D2 | analyst FOCUSED r2 | — | none | 1 | 1 finding | |
| D3 | analyst FOCUSED r3 | — | none | 1 | NO FINDINGS | cites future "hand edit to 50" (leak) |
| D4 | analyst VERIFY | — | none | 1 | NO FINDINGS | |
| D5 | run1 1.1 | M | sonnet | 1 | done | |
| D6 | run1 1.2 | M | sonnet | 1 | done | parallel with D7; mentions future bound edit (leak) |
| D7 | run1 3.1 | M | sonnet | 1 | done | |
| D8 | run1 3.2 | M | sonnet | 1 | done | parallel with D9 |
| D9 | run1 5.1 | M | sonnet | 1 | done | |
| D10 | run1 5.2 | M | sonnet | 1 | done | |
| D11 | run2 1.1 | M | sonnet | 1 | done | PERCENT_MAX 90→50 |
| D12 | run2 1.2 | M | sonnet | 1 | done | test bound 90→50 |
| D13 | run2 3.2 | M | sonnet | 1 | done | generator uses PERCENT_MIN..MAX |

## Artifact checks
| Artifact | Done-when item | Pass/Fail | Evidence |
|---|---|---|---|
| requirements.md | 2–7 criteria per requirement | Pass | 6, 7, 5, 4, 3 |
| requirements.md | one SHALL, ≤40 words | Pass | applied options re-worded to one SHALL (F1 option had two) |
| requirements.md | every term in Glossary | Pass | 10 terms |
| requirements.md | every input bounded | Pass (F7 deferred) | `expires_on` type in Open Questions |
| requirements.md | failure/edge criterion per input req | Pass | 1.2–1.6, 2.2–2.7, 4.1–4.2, 5.2–5.3 |
| design.md | every criterion → component/property | Pass | `_Requirements:_` on 3 components |
| design.md | ≥1 mermaid, diff tree, call trees | Pass | sequence diagram, 3 diff call trees |
| design.md | Criteria Classification complete | Pass | 25 rows |
| design.md | Testing Strategy per property | Pass | 6 rows, 200 iterations |
| design.md | Open Questions decided | Pass | F7 marked out of scope |
| tasks.md | `check-tasks` PASS | Pass | before both gates and after sync |
| tests | ≥100 iterations, tag per property | Pass | 6 `Feature: discount-codes, Property N` tags, max_examples 200 |
| .spec.json | no `stale` after sync | Pass | all `approved` |
| code | bound = 50 | Pass | `shop/discounts.py:7`, 51 → ValueError |

## Issues
| ID | Severity | Plugin file:line | Problem | Proposed fix |
|---|---|---|---|---|
| I1 | medium | skills/spec-run/SKILL.md:20-21 | Runner (and analyst) reports arrive as a SubagentHandback message; the Agent tool result holds only "delivered as a message". A literal reading of "no `STATUS:` line → `[ ]`" marks every leaf failed. | Add: "Report may arrive as a hand-back message; read it there before checking `STATUS:`." Same note in spec-analyze step 2. |
| I2 | medium | (eval harness) project `CLAUDE.md` | The Script (future 90 → 50 edit) is in subagent context. Analyst r3 and runner 1.2 cite it. Weakens the drift/sync test. | Move the Script out of `CLAUDE.md` (e.g. orchestrator-only prompt). |
| I3 | low | agents/spec-analyst.md:34 | F1 option A had two `SHALL` ("…SHALL compute… and this SHALL take precedence"), against its own "Count `SHALL`" rule. | Add to Done-when: "every option has exactly one SHALL". |
| I4 | low | skills/spec-analyze/SKILL.md:19 | F8 option A (new 2.8) fully supersedes 2.6. Rule "new criterion number, never a longer criterion" gives no path for a replacing option; I merged into 2.6. | Add: "Option that supersedes an existing criterion → replace that criterion, log it." |
| I5 | low | skills/spec-sync/SKILL.md:22 | Step 6 says `SPEC approve <every stale phase>`, but step 2's gate already approved design. Unclear whether to re-approve. | "`SPEC approve <dir> tasks` (upstream phases approved at step 2 gate)." |
| I6 | low | shared/state.md:3 | `SPEC` = `python3 ${CLAUDE_PLUGIN_ROOT}/…/spec.py` as a shell variable fails in zsh (no word split): "no such file or directory". Needed a wrapper script. | Show the full command line, or say "run as `python3 <path> <cmd>`". |
| I7 | low | agents/spec-analyst.md (behavior) | Analyst r3 claimed the Introduction states 90; it does not. Harmless hallucination. | Require QUOTE-style citation for any claim in NO FINDINGS notes. |

## Metrics
- Questions: 11 logged in `QA.md` (0 UNSCRIPTED). Gates: 5 (req ×2, design ×2, tasks ×1) + sync Apply all.
- Dispatches: 13 — analyst 4 (no model passed → sonnet), runner 9 (sonnet 9, haiku 0, opus 0).
- Retries/escalations: 0. Checkpoint deferrals: 1 (run 2, checkpoint 2). Red checkpoints shown to user: 0. Counterexamples: 0.
- Tests: 17 pass / 0 fail (final). Nothing committed.

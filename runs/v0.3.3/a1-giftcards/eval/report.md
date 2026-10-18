# a1-giftcards-v033 eval

Orchestrator: Opus 5.5 (claude-opus-5-5), effort low · Result: PASS

## Plugin load
- Slash command expanded? No. The task came from the parent session as plain text. All three commands ran as `manual load` from `plugins/sdd/skills/<skill>/SKILL.md` (see `eval/commands.md`).
- `${CLAUDE_PLUGIN_ROOT}` resolved by hand. Example: `/Users/baodang/Documents/code/agent-skills/plugins/sdd/shared/ears.md`.
- Agent types `sdd:spec-analyst` and `sdd:spec-task-runner` were available. All 10 dispatches used them.
- Frontmatter applied. Analyst (no `model` passed) said "claude-sonnet-5-5 … Read, Glob, Grep, SubagentHandback": frontmatter `sonnet` + read-only tools. Runners said haiku / opus / sonnet as passed, with Read, Write, Edit, Bash (Glob, Grep not named; probably unused).
- Every subagent report came as a SubagentHandback message, not in the Agent result. Both skills tell the orchestrator to expect this.

## Summary
- spec-analyze: 3 analysis rounds (FULL, FOCUSED, FOCUSED) + 2 VERIFY passes. 17 findings. 14 applied, 2 deferred to `## Open Questions` (F9 low, F17 medium left after last VERIFY), F6 split in two.
- Criteria 12 → 23 (+92 %). The skill recommends a spec split; the recommendation is in `eval/apply-log.md`.
- spec-new resumed at `design`. design.md (4 components, 9 properties) and tasks.md (5 leaves, 4 waves, `check-tasks` PASS + 1 WARN) both approved.
- spec-run `--mode waves --optional`: 5 leaves, 5 done on attempt 1, 3 checkpoints green. 13 tests pass.
- Main plugin defects: analyst options break the analyst's own checklist (I1). An applied option made a new inconsistency, which round 2 had to fix (I2).

## Step trace
| Skill | Step | Action | Done-when held | Evidence |
|---|---|---|---|---|
| spec-analyze | 1 Load | `SPEC drift` → NO DRIFT; read requirements + state; N0 = 12 | yes | transcript |
| spec-analyze | 2 Analyze | D1 FULL, no `model` | yes (9 findings) | `analyst-round-1.md` |
| spec-analyze | 3 Resolve | F6 split (A/B different gaps); F7 A\|Defer; F9 low deferred; 3 question calls ≤4 each, grouped by requirement | yes | `QA.md` |
| spec-analyze | 4 Apply | 10 criteria changed/added; clash 1.3→1.5 renumbered; EARS check; `SPEC edited` | yes | `apply-log.md` |
| spec-analyze | 5 Recheck r2 | D2 FOCUSED → F10 high, F11 medium; resolve + apply; clause dropped from F10 | yes | `analyst-round-2.md` |
| spec-analyze | 5 Recheck r3 | D3 FOCUSED → F12 high NEEDS_OWNER; conservative answer; 5.3 added | yes | `analyst-round-3.md` |
| spec-analyze | 5 VERIFY 1 | D4 on 12 ids → 4 medium; one resolve + apply; F14 split into 5.4/5.5 | yes | `analyst-round-4-verify.md` |
| spec-analyze | 5 VERIFY 2 | D5 on 6 changed ids → F17 medium → Open Questions; growth reported | yes | `analyst-round-5-verify.md` |
| spec-new | 1 Name | dir exists → Resume (Script); drift NO DRIFT; jump to design | yes | `QA.md` |
| spec-new | 5 → RF step 4–5 | design.md drafted; `SPEC draft` + Approve → `approve` | yes | `.spec.json` design approved |
| spec-new | 5 → RF step 6–7 | tasks.md; `check-tasks` PASS; draft + Approve | yes | `.spec.json` tasks approved |
| spec-run | 1–4 | drift NO DRIFT, all approved, mode waves, scope 5 leaves (with `*`), `check-tasks` PASS | yes | transcript |
| spec-run | 5 wave 0–1 | 1.1 haiku, 1.2 opus; checkpoint 2 green (3 tests) | yes | `dispatch.md` D6–D7 |
| spec-run | 5 wave 2 | 3.1 + 5.1 sonnet in one message; checkpoint 4 green (8 tests) | yes | D8–D9 |
| spec-run | 5 wave 3 | 5.2 sonnet; group 5 + checkpoint 6 green (13 tests) | yes | D10 |
| spec-run | 7 Report | no `[ ]`/`[-]` left in tasks.md | yes | below |

## Dispatches
| # | Leaf/round | Size | Model passed | Attempt | Status | Notes |
|---|---|---|---|---|---|---|
| D1 | analyst FULL | — | (omitted) | 1 | 9 findings | ran as sonnet |
| D2 | analyst FOCUSED r2 | — | (omitted) | 1 | 2 findings | F10 caused by F2 A |
| D3 | analyst FOCUSED r3 | — | (omitted) | 1 | 1 finding | NEEDS_OWNER with extra draft text |
| D4 | analyst VERIFY 1 | — | (omitted) | 1 | 4 findings | 2 NEEDS_OWNER |
| D5 | analyst VERIFY 2 | — | (omitted) | 1 | 1 finding | → Open Questions |
| D6 | 1.1 | S | haiku | 1 | done | |
| D7 | 1.2 | L | opus | 1 | done | concurrency checked with 20 threads |
| D8 | 3.1 | M | sonnet | 1 | done | flagged actor_id vs `ctx.get("actor")` gap in leaf text |
| D9 | 5.1 | M | sonnet | 1 | done | P4,5,7,8,9 |
| D10 | 5.2 | M | sonnet | 1 | done | P1,2,3,6 + 2.2 example |

## Artifact checks
| Artifact | Done-when item | Pass/Fail | Evidence |
|---|---|---|---|
| requirements.md | every chosen option applied | Pass | `apply-log.md` |
| requirements.md | every changed criterion passes EARS (1 SHALL, ≤40 words) | Pass | F10 trailing clause dropped, F14 split |
| requirements.md | no open high/medium outside Open Questions | Pass | F17 (medium) is in Open Questions |
| requirements.md | growth reported | Pass | 12 → 23 |
| design.md | every criterion mapped | Pass | Criteria Classification lists 23 |
| design.md | interface sketches, Mermaid, `diff` tree, call tree | Pass | design.md |
| design.md | Open Questions decided | Pass | F9, F17 under Key design decisions |
| design.md | non-functional owner | Pass | 2.2 → Shop_API routes |
| tasks.md | `check-tasks` RESULT: PASS | Pass | 1 WARN (checkpoint 4 shares wave with 5.1) |
| code | property tag + ≥100 iterations | Pass | 9 tags; `max_examples` 100–200 |
| tests | suite green | Pass | 13 passed |
| .spec.json | all phases approved, criteria baseline stored | Pass | 23 criteria in baseline |

## Issues
| ID | Severity | Plugin file:line | Problem | Proposed fix |
|---|---|---|---|---|
| I1 | medium | agents/spec-analyst.md:32-34 | Analyst broke its own checklist in 4 findings: F6 A/B closed different gaps; F14, F17 options held two assertions; F12 `NEEDS_OWNER` option carried a draft criterion after the question. The orchestrator repaired each. Same as v032 I1. | Make the checklist a required last output line per finding, e.g. `CHECK: gaps=1 shall=1 asserts=1`, so a breach is visible and the orchestrator can reject it. |
| I2 | medium | skills/spec-analyze/SKILL.md:19 | Step 4 checks merged text only against EARS form. F2 A ("balance unchanged until void") contradicted 2.1 redemption; only round 2 caught it (F10 high). | In step 4, add: "Check each changed criterion against every criterion it names or shares a term with; a clash → back to step 3 before the next round." |
| I3 | low | skills/spec-analyze/SKILL.md:22 | Owner answers add interfaces (charge_ref, Actor, Error_Log), and each VERIFY finds new failure paths on them. VERIFY 1: 4 findings, VERIFY 2: 1 more. The cap stops the loop, but growth hit 92 %. | When a NEEDS_OWNER answer adds an interface, tell the analyst to list its failure paths in the same round, or count owner-answer criteria apart in the growth line. |
| I4 | low | skills/spec-analyze/SKILL.md:19 | The renumber rule covers only clashes among applied options. Deferred F9 kept a proposed id 5.3; a later apply used 5.3 for a different criterion. The orchestrator renumbered by hand. | "Deferred items keep no criterion number" or "renumber Open Questions proposals after each apply". |
| I5 | low | shared/state.md:3 | The warning about a zsh shell variable is correct, but easy to miss. The orchestrator set `S="python3 …/spec.py"` and both draft and approve failed silently (the variable was not split). The next call recovered. | Show one copy-paste form, e.g. `python3 "$CLAUDE_PLUGIN_ROOT/shared/scripts/spec.py" approve <dir> design`, and say "never put `python3` in a variable". |

## Metrics
- Questions: 7 question calls (spec-analyze 7 calls, 16 items: 12 option A, 4 NEEDS_OWNER (F1, F12, F13, F16) answered with conservative values, 0 UNSCRIPTED); spec-new 1 resume + 2 gates. Deferred without asking: F9 (low). Left after VERIFY: F17.
- Dispatches: 10. Analyst 5 (sonnet via frontmatter). Runner 5: haiku 1, sonnet 3, opus 1.
- Retries/escalations: 0. Counterexamples: 0.
- Gates: design Approve, tasks Approve. Checkpoints: 3 green, 0 red.
- Tests: 13 pass, 0 fail.
- Criteria: 12 → 23 (+92 %).

# a1-giftcards-v032 eval

Orchestrator: Opus 5.5 (claude-opus-5-5), effort low · Result: PASS

## Plugin load
- Slash command expanded? No. The task text held only `/sdd:spec-analyze gift-cards`, with no skill body. All three skills were read from `/Users/baodang/Documents/code/agent-skills/plugins/sdd/skills/<skill>/SKILL.md` (see `eval/commands.md`).
- `${CLAUDE_PLUGIN_ROOT}` resolved by hand: `/Users/baodang/Documents/code/agent-skills/plugins/sdd/shared/ears.md`. `plugin.json` version 0.3.2.
- Agent types `sdd:spec-analyst` and `sdd:spec-task-runner` were both available.
- Frontmatter applied: the analyst ran with `model` omitted and said "Sonnet 5.5 (claude-sonnet-5-5)" (frontmatter `sonnet`). Runners said Haiku 5.5 / Opus 5.5 / Sonnet 5.5, the same as the `model` passed. Each report came as a hand-back message, not in the Agent result. The skills expect this.

## Summary
- All 3 Script commands ran to the end. Phases are all `approved`. All 5 leaves and 3 checkpoints are `[x]`. 23 tests pass.
- spec-analyze: 3 rounds + VERIFY, 17 findings. 16 resolved, 1 deferred (F17 low → `## Open Questions`, decided in design). Criteria went from 12 to 27 (+125 %). The skill recommends a split.
- 4 NEEDS_OWNER answers used the most conservative concrete value (F2, F9, F10, F11). Two of them added interfaces the code does not have (`ctx["actor"]`, `ctx["payments"].refund`).
- The analyst broke its own option rules 6 times. The orchestrator repaired them per spec-analyze step 3 (I1).
- spec-run: 6 dispatches, 0 retries, 0 escalations, 0 counterexamples, 0 red checkpoints.

## Step trace
| Skill | Step | Action | Done-when held | Evidence |
|---|---|---|---|---|
| spec-analyze | 1 Load | `spec.py drift` → NO DRIFT; N0 = 12 | yes | `eval/trace.md` |
| spec-analyze | 2 Analyze | FULL dispatch, F1–F9 | yes | `eval/analyst-round-1.md` |
| spec-analyze | 3 Resolve | split F6, F7; asked 5 groups (≤4 per call) | yes | `eval/QA.md` Q1–Q5 |
| spec-analyze | 4 Apply | merged text, 10 new criteria, 3 replaced, Glossary +3; `spec.py edited` | yes | `requirements.md`, trace |
| spec-analyze | 5 Recheck | R2 FOCUSED (F10–F11), R3 FOCUSED (F12–F13), VERIFY (F14–F17); growth reported | yes | `analyst-round-2/3/4-verify.md` |
| spec-new | 1 Name | dir exists → Resume → drift → jump to design | yes | QA Q10 |
| spec-new | 5 / RF 4–5 | design.md drafted; gate draft → Approve → approve | yes | QA Q11, `.spec.json` |
| spec-new | 5 / RF 6–7 | tasks.md; `check-tasks` PASS (1 WARN); gate → Approve | yes | QA Q12, criteria baseline = 27 |
| spec-run | 1–4 | drift NO DRIFT; mode waves; scope 5 leaves (with `*`); check-tasks PASS | yes | trace |
| spec-run | 5 Execute | waves 0–3, parallel dispatch in one message for waves 0 and 2; checkpoints 2, 4, 6 green | yes | `eval/dispatch.md` |
| spec-run | 6–7 | no counterexample; report table below | yes | Dispatches |

## Dispatches
| # | Leaf/round | Size | Model passed | Attempt | Status | Notes |
|---|---|---|---|---|---|---|
| D1 | analyze R1 FULL | — | omitted (sonnet) | 1 | 9 findings | F8/F9 rule breaks |
| D2 | analyze R2 FOCUSED | — | omitted | 1 | 2 findings | both NEEDS_OWNER; F10 re-raises F4 |
| D3 | analyze R3 FOCUSED | — | omitted | 1 | 2 findings | both propose id 3.6 |
| D4 | analyze VERIFY | — | omitted | 1 | 4 findings | 3 medium applied, never re-verified |
| D5 | 1.1 payments | S | haiku | 1 | done | wave 0 |
| D6 | 1.2 ledger | S | haiku | 1 | done | wave 0 |
| D7 | 1.3 service | L | opus | 1 | done | wave 1 |
| D8 | 3.1 api | M | sonnet | 1 | done | wave 2 |
| D9 | 5.1* props | M | sonnet | 1 | done | 12 properties, 100 examples each |
| D10 | 5.2 api tests | M | sonnet | 1 | done | redeem test uses subtotal 0 |

## Artifact checks
| Artifact | Done-when item | Pass/Fail | Evidence |
|---|---|---|---|
| requirements.md | every chosen option applied | Pass | QA answers ↔ criteria 1.3–1.8, 2.2–2.7, 3.3–3.7, 4.2, 5.3 |
| requirements.md | changed criteria pass EARS (1 SHALL, ≤40 words) | Pass | manual check, trace |
| requirements.md | no open high/medium outside Open Questions | Pass | only F17 (low) is in Open Questions |
| design.md | every criterion → component/property | Pass | `_Requirements:_` lines + classification table (27 rows) |
| design.md | interface sketches, Mermaid, `diff` tree, call trees | Pass | design.md |
| design.md | Open Question F17 decided | Pass | Key design decisions |
| design.md | Testing Strategy lists all 12 properties | Pass | table |
| tasks.md | `check-tasks` RESULT: PASS | Pass | WARN checkpoint 4 (5.1 in shared wave 2) |
| .spec.json | phases approved, criteria baseline stored | Pass | 27 criteria |
| tests | property tag + ≥100 iterations | Pass | 12 tags, `max_examples=100` |
| run | no `[-]` left, every leaf `[x]` | Pass | tasks.md |

## Issues
| ID | Severity | Plugin file:line | Problem | Proposed fix |
|---|---|---|---|---|
| I1 | medium | agents/spec-analyst.md:28-33 | The analyst broke its own option rules: F8 and F16 put a concrete A with a NEEDS_OWNER B; F6 and F7 have an A and a B for different gaps; F5 A, F6 A/B and F7 B have 2 assertions each; F9 is NEEDS_OWNER at `low` (rule: at least medium). | Add a pre-output checklist to spec-analyst.md: per option count SHALL and assertions, NEEDS_OWNER sole, A/B same gap, NEEDS_OWNER ≥ medium. |
| I2 | medium | agents/spec-analyst.md:30 | In one round, F12 and F13 both proposed new criterion 3.6. "Next free criterion number" does not say that it increments across findings. The orchestrator had to renumber. | Say "number new criteria in order across all findings of the round". Also add to spec-analyze step 4: clash → renumber, log it. |
| I3 | medium | skills/spec-analyze/SKILL.md:24 | VERIFY high/medium → one Resolve + Apply, then no recheck. New criteria 1.8 and 2.7 and the changed 4.2 are never verified. | Allow one more VERIFY for only the ids that VERIFY changed. If findings remain, park them as `## Open Questions`. |
| I4 | medium | skills/spec-analyze/SKILL.md:19-23 | FOCUSED round 2 raised F10 again. F10 questions 2.3, which the owner picked in round 1 (F4 A). The analyst gets no list of decided findings, so this can loop. | Give the analyst the decided finding ids with their chosen options. Tell it to skip them unless a new criterion breaks them. |
| I5 | low | skills/spec-analyze/SKILL.md:21 | For NEEDS_OWNER the skill says only "ask the owner question". It does not give the options (free answer, Defer). In eval mode, the answers added interfaces (`refund`, `ctx["actor"]`) that design then had to accept. | Give the options: `Answer (free text) | Defer`. Prefer Defer when the answer adds an interface the code does not have. |
| I6 | low | skills/spec-analyze/SKILL.md:24 | Growth was 12 → 27 (+125 %). About half of it came from splits to keep one assertion per criterion (4 pairs). A >50 % growth limit then fires for nearly every money spec. | Count growth before splits for one assertion, or count by behavior. Or raise the limit. |
| I7 | low | agents/spec-task-runner.md:15 | The 5.2 runner tested redeem through `handle` with subtotal 0, so 2.1 subtraction is not exercised at the API level (Property 5 covers it at the service level). No step checks that `Verify` exercises each cited criterion. A redeem with subtotal 0 also writes a Ledger entry with old == new. The analyst did not see this gap in 5.1. | Runner: for each cited criterion, give a case that can fail on it. Analyst EDGE: check zero and no-op changes against audit criteria. |

Orchestrator slip (not a plugin defect): the first gate `SPEC` call used a shell variable, and zsh did not word-split it. state.md warns about this. The call was run again as full command lines.

## Metrics
- Questions: 12 groups logged (Q1–Q12). Analyze: 9 groups, 16 asked findings, 4 NEEDS_OWNER answers, 0 UNSCRIPTED. spec-new: 1 resume + 2 gates (both Approve). spec-run: 0 questions (no fail, no red).
- Dispatches: spec-analyst 4 (sonnet via frontmatter). spec-task-runner 6: haiku 2, sonnet 3, opus 1.
- Retries/escalations: 0 / 0.
- Gates: design Approve, tasks Approve (requirements were approved before; `edited` 4 times).
- Tests: 23 pass, 0 fail (3 old + 12 property + 8 API). `check-tasks`: PASS with 1 WARN.
- Criteria: 12 → 27. Not committed.

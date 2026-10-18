# a1-giftcards eval

Orchestrator: Opus 5.5 (claude-opus-5-5), effort low · Result: PASS

## Plugin load
- Slash command expanded? No. All 3 commands came as plain text from the parent session. Each skill was loaded by hand (`manual load`, see `eval/commands.md`).
- `${CLAUDE_PLUGIN_ROOT}` resolved by hand to `/Users/baodang/Documents/code/agent-skills/plugins/sdd`. Example: `python3 /Users/baodang/Documents/code/agent-skills/plugins/sdd/shared/scripts/spec.py check-tasks docs/specs/gift-cards`.
- Agent types `sdd:spec-analyst` and `sdd:spec-task-runner` were available and used. `general-purpose` was not used.
- Frontmatter applied. Analyst said "Sonnet 5.5, tools Read, Glob, Grep (+SubagentHandback)". Runners reported the model that was passed: haiku → Haiku 5.5, sonnet → Sonnet 5.5, opus → Opus 5.5.

## Summary
- spec-analyze: 3 FULL rounds + 1 VERIFY. 26 findings. 19 high/medium findings resolved with option A. 4 low findings and 3 verify findings went to Open Questions. Criteria went from 13 to 28.
- spec-new (resume): design.md (8 components, 10 properties) and tasks.md (11 leaves, 5 waves, 4 checkpoints) written. Both gates approved. check-tasks PASS.
- spec-run waves --optional: 15 runner dispatches. 14 were `done` on attempt 1. Leaf 1.1 returned `placeholder` with no report. It was retried one tier up (opus) → `done`.
- All checkpoints green. Final: 21 tests pass, 0 fail. No counterexamples. Final drift: NO DRIFT.
- 11 plugin issues logged. None blocked the run.

## Step trace
| Skill | Step | Action | Done-when held | Evidence |
|---|---|---|---|---|
| spec-analyze | 1 Load | `SPEC drift` → NO DRIFT; read requirements + state | yes | requirements approved |
| spec-analyze | 2 Analyze | D1 FULL | yes | F1–F13 |
| spec-analyze | 3 Resolve | 10 → A in 3 grouped calls; 3 low deferred | yes | QA.md calls 1–3 |
| spec-analyze | 4 Apply | edits, EARS splits, `SPEC edited` | yes | 4.2 deleted; 1.1 split |
| spec-analyze | 5 Recheck | D2, D3 FULL → 9 resolved, 1 deferred; D4 VERIFY → 3 to Open Questions | yes | analyst-round-{2,3,verify}.md |
| spec-new | 1 Name | dir exists → Resume; drift NO DRIFT; first non-approved = design | yes | QA.md Q1 |
| spec-new | 5 → req-first 4 | design.md drafted | yes | all 9 Done-when items (see Artifact checks) |
| spec-new | gate design | `SPEC draft` → Approve → `SPEC approve design` | yes | phase approved |
| spec-new | req-first 6 | tasks.md drafted | yes | check-tasks PASS (21 checks) |
| spec-new | gate tasks | `check-tasks` PASS → draft → Approve → approve | yes | phase approved, criteria baseline stored |
| spec-run | 1 Load | drift NO DRIFT; all phases approved | yes | .spec.json |
| spec-run | 2 Mode | `--mode waves` | yes | no question |
| spec-run | 3 Scope | 11 leaves (5 optional, `--optional`) | yes | tasks.md |
| spec-run | 4 Graph | check-tasks PASS | yes | |
| spec-run | 5 Execute | waves 0–4; one message per wave; retry 1.1 | yes | dispatch.md D5–D19 |
| spec-run | 5 Checkpoints | 2, 4, 6, 8 green | yes | 3 / 3 / 18 / 21 passed |
| spec-run | 6 Property failure | none | n/a | COUNTEREXAMPLE: none ×15 |
| spec-run | 7 Report | every leaf `[x]`, no `[-]` | yes | grep shows no open marks |

## Dispatches
| # | Leaf/round | Size | Model passed | Attempt | Status | Notes |
|---|---|---|---|---|---|---|
| D1 | analyze r1 FULL | – | sonnet | 1 | 13 findings | |
| D2 | analyze r2 FULL | – | sonnet | 1 | 6 findings | |
| D3 | analyze r3 FULL | – | sonnet | 1 | 4 findings | |
| D4 | analyze VERIFY | – | sonnet | 1 | 3 findings | to Open Questions |
| D5 | 1.1 | M | sonnet | 1 | no report | `placeholder`; file written, Verify passed; treated failed |
| D6 | 1.2 | S | haiku | 1 | done | |
| D7 | 1.3 | S | haiku | 1 | done | |
| D8 | 1.4 | S | haiku | 1 | done | |
| D9 | 1.1 | M | opus | 2 | done | retry, tier up; no change to file |
| D10 | 1.5 | S | haiku | 1 | done | |
| D11 | 3.1 | L | opus | 1 | done | |
| D12 | 3.2 | L | opus | 1 | done | |
| D13 | 3.3 | M | sonnet | 1 | done | |
| D14 | 5.1 | M | sonnet | 1 | done | |
| D15 | 5.2* | M | sonnet | 1 | done | 6 tests |
| D16 | 5.3* | L | opus | 1 | done | 5 tests, threads + barrier |
| D17 | 5.4* | M | sonnet | 1 | done | no tag comment |
| D18 | 5.5* | M | sonnet | 1 | done | |
| D19 | 7.1* | M | sonnet | 1 | done | |

## Artifact checks
| Artifact | Done-when item | Pass/Fail | Evidence |
|---|---|---|---|
| requirements.md | changed criteria pass EARS (one SHALL, ≤40 words) | Pass | max 31 words; F5/F7/F8/F9/F17/F19/F21 split |
| requirements.md | no open high/medium outside Open Questions | Pass | F24–F26 listed there |
| design.md | every criterion → component or property | Pass | Criteria Classification lists 28/28 |
| design.md | interface sketch per new/changed component | Pass | 8 Python sketches |
| design.md | Error Handling per external dependency | Pass | Payment_Provider, Ledger rows |
| design.md | ≥1 Mermaid | Pass | sequence diagram |
| design.md | File/Folder Structure as `diff` | Pass | |
| design.md | call tree `diff` where control flow changes | Pass | purchase, redeem, void, api, Cart |
| design.md | Criteria Classification lists every criterion | Pass | 28 rows |
| design.md | Testing Strategy lists every property | Pass | 10 rows, ≥100 |
| design.md | non-functional constraint has owner | Pass | 2.2 latency → `redeem.apply` |
| tasks.md | `check-tasks` RESULT: PASS | Pass | 21/21 checks |
| tests | tag comment per property (correctness.md step 4) | Fail | `tests/test_void.py` has a docstring, not `# Feature: gift-cards, Property 8` |
| tests | iterations ≥100 | Pass | max_examples 100–200; test_void uses default 100 |
| .spec.json | all phases approved, hashes, criteria baseline | Pass | NO DRIFT at end |

## Issues
| ID | Severity | Plugin file:line | Problem | Proposed fix |
|---|---|---|---|---|
| I1 | medium | skills/spec-run/SKILL.md:21 | No rule for a runner reply with no parseable report (D5 = `placeholder`). The orchestrator had to guess. | Add: "No `STATUS:` line → treat as `failed`, show raw reply." |
| I2 | medium | agents/spec-analyst.md:28 | Options often hold two assertions or two SHALLs (F5, F7, F9, F17, F19, F21, F24). The orchestrator had to split 7 times. | Add "one observable assertion" and reference the `shared/ears.md` rules. |
| I3 | medium | agents/spec-analyst.md:27 | Options A/B are sometimes complementary, not alternatives (F7, F9, F10). One pick drops a real fix. | Require A and B to exclude each other. Put a separate gap in a separate finding. |
| I4 | medium | skills/spec-analyze/SKILL.md:22 | Every FULL round found new medium items. After the 3-round cap, 3 medium items stay open. Criteria doubled (13 → 28). | Accept by design, or give VERIFY findings one resolve pass for high only. |
| I5 | low | agents/spec-analyst.md:29 | NEEDS_OWNER shows as option B with a stray `A)` label (F3, F6, F8, F11–F13). | Say "NEEDS_OWNER only as the sole option". |
| I6 | low | skills/spec-analyze/SKILL.md:19 | No rule for an option part that another criterion already covers (F18 "return 503" vs 5.2). | Add: "Drop parts that duplicate a criterion; log it." |
| I7 | low | agents/spec-task-runner.md:14 | The runner body cites `${CLAUDE_PLUGIN_ROOT}/shared/correctness.md`. A subagent may not resolve it. One runner (D17) left out the property tag comment. | Have spec-run pass the resolved path in the prompt, or inline the tag rule in the agent. |
| I8 | low | shared/scripts/spec.py:269 | check-tasks only compares `Files`. A same-wave leaf whose `Verify` imports another leaf's file passes. I found this by hand (`tests/fakes.py`). | Also scan backticked paths in `Do`/`Verify` against same-wave `Files`. |
| I9 | low | shared/artifacts/design.md:5 | Done-when has no item for requirements Open Questions. Design had to pick defaults without a rule (F22, F26). | Add: "every Open Question is decided in Key decisions or marked out of scope." |
| I10 | low | skills/spec-run/SKILL.md:20 | L → "your own model family". This is unclear for a retry of an M leaf (sonnet → ?). I used opus. | State the tier list once: haiku → sonnet → opus. |
| I11 | low | shared/gate.md:1 | The count-line examples do not say how to count components or leaves. | Name the heading pattern that is counted. |

## Metrics
- Questions: 23 logged (spec-analyze 19 → A; spec-new 3: Resume, design Approve, tasks Approve; spec-run 1: Retry). Low deferred without asking: 4. NEEDS_OWNER chosen: 0. UNSCRIPTED: 0.
- Dispatches: 19. sonnet 11 (4 analyst + 7 runner), haiku 4, opus 4.
- Retries/escalations: 1 (leaf 1.1, sonnet → opus). Skips: 0. Stops: 0.
- Gates: 2 approved (design, tasks). Checkpoints: 4 green, 0 red.
- Tests: 21 pass, 0 fail. Counterexamples: 0.
- Nothing committed.

# 02-reqfirst-haiku

Model: Haiku 5.5 · Skills run: spec-new (Requirements-First), spec-analyze (via gate), spec-analyst ×3 · Result: PARTIAL

## Summary
- The spec flow ran to the end. All three phases reached `approved`. Spec-new stopped before spec-run, as scripted.
- spec-new has no subagent tool in `allowed-tools`. The analyze step still ran through the Agent tool. Log as issue 02-1.
- The analyze loop hit the 3-round cap. Round 3 applied high and medium options (F1–F3). Those edits were not checked again.
- Artifact checks failed on three items: criterion 1.7 is not mapped in design, no criteria classification exists, and 1.6 and 1.8 bundle several behaviors.
- Requirement 1.8 asks that a timed-out write is discarded. A remote Lua script cannot guarantee that. The design records this as a known gap. The design gate did not block it.

## Step trace
| Skill | Step | Action taken | Done-when held | Evidence |
|---|---|---|---|---|
| spec-new | 1 Name | `shortlinks-rate-limit` from feature words | Pass | `docs/specs/` did not exist |
| spec-new | 2 Size | Not a one-line change | Pass | — |
| spec-new | 3 Workflow | Input named Requirements-First | Pass | — |
| spec-new | 4 State | Created `.spec.json`, phases pending | Pass | `workspace/docs/specs/shortlinks-rate-limit/.spec.json` |
| spec-new | 5 Run workflow | Read `requirements-first.md` only | Pass | — |
| requirements-first | 2 Draft requirements | 1 requirement, 8 criteria; phase `draft` | Pass (see Artifact checks) | `requirements.md` |
| requirements-first | 3 Gate 1 | Asked; answer "Analyze first" | Pass | Scripted |
| spec-analyze flow | 2 Analyze (round 1) | Agent dispatch, 5 findings (F1–F5, all high or medium) | Pass | Subagent hand-back |
| spec-analyze flow | 3–4 Resolve/Apply (round 1) | Option A for all 5; edits applied | Pass | `requirements.md` v2 |
| spec-analyze flow | 5 Recheck (round 2) | Agent dispatch, 5 findings (F1–F4 medium/high, F5 low) | Pass | Subagent hand-back |
| spec-analyze flow | 3–4 Resolve/Apply (round 2) | Option A for F1–F4; F5 deferred to Open Questions | Pass | `requirements.md` v3 |
| spec-analyze flow | 5 Recheck (round 3) | Agent dispatch, 8 findings (F5 duplicates deferred item) | Not met: cap reached | Subagent hand-back |
| spec-analyze flow | 3–4 Resolve/Apply (round 3) | F1–F3 option A; F4, F6–F8 deferred; F5 not re-asked | Partial: edits not rechecked | `requirements.md` v4 |
| requirements-first | 3 Gate 1 (again) | Approve | Pass | `.spec.json` requirements = approved |
| requirements-first | 4 Draft design | 3 components, 5 properties; phase `draft` | Fail (see Artifact checks) | `design.md` v1 |
| requirements-first | 5 Gate 2 | Request changes (scripted), then Approve after edit | Pass | Clock injected; fixed Window named in `design.md` |
| requirements-first | 6 Draft tasks | 10 leaves, 7 waves, 5 checkpoints/groups | Pass | `tasks.md`; validator PASS |
| requirements-first | 7 Gate 3 | Approve | Pass | `.spec.json` tasks = approved |
| spec-new | end | Tell user `/spec-run` (not run) | Pass | — |

## Scripted Q&A
| # | Question (as the skill would ask) | Options | Answer | Scripted? |
|---|---|---|---|---|
| 1 | Gate 1: requirements drafted. Approve or change? | Approve · Request changes · Analyze first | Analyze first | Yes |
| 2 | F1 Counted Request undefined (high) | A · B · Defer | A | Yes (rule: high/med → A) |
| 3 | F2 "current Window" undefined (high) | A · B · Defer | A | Yes |
| 4 | F3 Retry-After calc undefined (med) | A · B · Defer | A | Yes |
| 5 | F4 "concurrently" unmeasured (med) | A · B · Defer | A | Yes |
| 6 | F5 storage location and failure (high) | A · B · Defer | A | Yes |
| 7 | R2 F1 429 counted vs Limit (high) | A · B · Defer | A | Yes |
| 8 | R2 F2 "oldest" vs fixed Window (med) | A · B · Defer | A | Yes |
| 9 | R2 F3 503 counted? precedence (med) | A · B · Defer | A | Yes |
| 10 | R2 F4 storage terms missing (med) | A · B · Defer | A | Yes |
| 11 | R2 F5 clock source, edge at 60 s (low) | A · B · Defer | Defer | Yes (rule: low → Defer) |
| 12 | R3 F1 placeholder `<N> ms` (high) | A · B · Defer | A | Yes |
| 13 | R3 F2 429 vs 503 precedence (med) | A · B · Defer | A | Yes |
| 14 | R3 F3 timed-out write commits (med) | A · B · Defer | A | Yes |
| 15 | R3 F4 Counted Request circular (low) | A · B · Defer | Defer | Yes |
| 16 | R3 F6 undefined terms (low) | A · B · Defer | Defer | Yes |
| 17 | R3 F7 response body undefined (low) | A · B · Defer | Defer | Yes |
| 18 | R3 F8 storage data loss (low) | A · B · Defer | Defer | Yes |
| 19 | Gate 1 again: Approve or change? | Approve · Request changes · Analyze first | Approve | Yes |
| 20 | Gate 2: design drafted. Approve or change? | Approve · Request changes | Request changes: inject clock; name window algorithm and why | Yes |
| 21 | Gate 2 after edit: Approve or change? | Approve · Request changes | Approve | Yes |
| 22 | Gate 3: tasks drafted. Approve or change? | Approve · Request changes | Approve | Yes |

R3 F5 repeated the deferred clock item. It was not asked again. UNSCRIPTED: 0.

## Artifact checks

### requirements.md
| Artifact | Done-when item | Pass/Fail | Evidence |
|---|---|---|---|
| requirements.md | Every requirement has ≥1 criterion, numbered N.M | Pass | Req 1, criteria 1.1–1.8 |
| requirements.md | Every criterion matches one EARS pattern, one behavior, one observable assertion | Fail | 1.6 and 1.8 each bundle 3+ behaviors (`ears.md:23`) |
| requirements.md | Every system/actor term appears in Glossary | Fail | "server instance" (1.7) absent; deferred as R3-F6 |
| requirements.md | Every input has bound or format | Pass | `api_key` typed as string in Glossary |
| requirements.md | Every happy-path criterion has failure or edge | Pass | 1.1 → 1.2, 1.6, 1.8 |
| requirements.md | Zero unmeasured adjectives | Pass | "normal" removed in v2 |

### design.md
| Artifact | Done-when item | Pass/Fail | Evidence |
|---|---|---|---|
| design.md | Every criterion maps to ≥1 component or property | Fail | 1.7 cited by no component and no property |
| design.md | Every external dependency has Error Handling entry | Pass | Redis entry in Error Handling |
| design.md | Every component has interface sketch | Pass | RateLimiter, Clock, handle |
| design.md | ≥1 Mermaid diagram | Pass | Architecture |
| design.md | File tree as `diff` | Pass | File/Folder Structure |
| design.md | Changed components have tree/call-tree `diff` | Pass | RateLimiter, handle; Clock is new, no tree |
| design.md | Testing Strategy lists every property | Pass | Lists Properties 1–5 by number |
| design.md | Non-functional constraint has owner | Pass | 100 ms timeout → `RateLimiter(timeout_s)` |
| design.md | correctness: every criterion classified | Fail | No slot in skeleton. 1.7 "example-only" not recorded |
| design.md | correctness: every property validates ≥1 criterion | Pass | Properties 1–5 cite 1.1–1.6, 1.8 |
| design.md | correctness: every property has task | Pass | Tasks 2.3, 2.4, 2.5, 4.2, 4.3 |

### tasks.md
| Artifact | Done-when item | Pass/Fail | Evidence |
|---|---|---|---|
| tasks.md | Every criterion cited by ≥1 leaf | Pass | Validator: "cited 8" |
| tasks.md | Every leaf in exactly one wave | Pass | Validator |
| tasks.md | Every leaf names its files | Pass | Validator: files_of non-empty for all 10 |
| tasks.md | Graph JSON parses | Pass | Validator |

## Validator output
Script: `validate_tasks.py` (in this scenario dir). Run: `python3 -I validate_tasks.py <spec dir>`.

```
JSON parses: OK
Leaves: 10 · Waves: 7
Each leaf in exactly one wave: OK
Same-wave leaves disjoint: OK
Test leaves after code leaves: OK
Criteria 8 · cited 8 · uncited none

RESULT: PASS
exit=0
```

Note: the script checks the wave rules only. It does not check that a leaf sits after the waves holding its dependencies. Dependencies are not in the JSON.

## Word counts
| Artifact | Words |
|---|---|
| requirements.md (final) | 777 |
| design.md (after gate 2 edit) | 852 |
| tasks.md | 458 |

Skeleton fit:
- Requirements: "## Open Questions" is added by spec-analyze. It is not in the skeleton.
- Design: the "Component tree" view does not apply. The feature has no UI. The call tree view was used.
- Design: no place for the criteria classification that correctness.md step 2 requires.
- Tasks: fits. The one-file-per-test rule forced five property leaves into separate waves.

## Issues
| ID | Severity | Plugin file:line | Problem | Proposed fix |
|---|---|---|---|---|
| 02-1 | high | `plugins/sdd/skills/spec-new/SKILL.md:6` | `allowed-tools` has no subagent tool. Gate 1 "Analyze first" needs dispatch (`shared/gate.md:6`, `shared/workflows/requirements-first.md:11`). | Add the subagent tool to spec-new `allowed-tools`, or move analyze to its own command. |
| 02-2 | med | `plugins/sdd/skills/spec-analyze/SKILL.md:6, :15` | Lists `Task`. Step text says "subagent" and names no tool. The Agent tool is not listed. | Name the exact tool and list it. |
| 02-3 | med | `plugins/sdd/skills/spec-analyze/SKILL.md:21` | "Max 3 rounds" has no rule for open non-deferred findings after round 3. Round 3 edits were never rechecked. | State what happens at the cap: defer the rest, or stop and report unverified edits. |
| 02-4 | med | `plugins/sdd/skills/spec-analyze/SKILL.md:17` | "group related, ≤4 per call" gives no grouping key. | Define the grouping key, or drop the grouping. |
| 02-5 | med | `plugins/sdd/shared/workflows/requirements-first.md:12, :15` | Only the requirements step sets `draft` (`:9`). Design and tasks steps do not. | Add "Set phase `draft`" to steps 4 and 6. |
| 02-6 | med | `plugins/sdd/shared/artifacts/design.md:10` | "Testing Strategy lists every property from `correctness.md`". `correctness.md` defines no property list. | Say "every Property N in this document". |
| 02-7 | med | `plugins/sdd/shared/correctness.md:8, :13`; `plugins/sdd/shared/artifacts/design.md:15-62` | Done-when requires criteria classification. The design skeleton has no slot for it. | Add a "Criteria classification" table to the design skeleton. |
| 02-8 | med | `plugins/sdd/shared/artifacts/tasks.md:18`; `plugins/sdd/shared/correctness.md:10` | Property leaves in one test file must each occupy a separate wave. Five properties took five waves. | Allow serial order inside one file, or name a test file per property. |
| 02-9 | med | `plugins/sdd/agents/spec-analyst.md:29` | Option text contained a placeholder `<N> ms`. It was applied to the spec (R3 F1). | Require concrete values in options. Otherwise the finding must be Deferred. |
| 02-10 | med | `plugins/sdd/agents/spec-analyst.md:29`; `plugins/sdd/shared/ears.md:23` | Round 2 F4 option A put three behaviors in 1.6. The EARS "one behavior" rule was broken. No check catches it. | Analyst options must follow EARS rules. Recheck must test the rule. |
| 02-11 | med | `plugins/sdd/agents/spec-analyst.md:18`; `plugins/sdd/skills/spec-analyze/SKILL.md:21` | Round 3 re-reported a deferred item as new (R3 F5). The analyst has no list of deferred IDs. | Pass deferred IDs to the analyst. Tell it not to report them again. |
| 02-12 | low | `plugins/sdd/skills/spec-new/SKILL.md:13` | "Kebab-case from input" does not say which words to keep when input names a workflow and a feature. | Say: use the feature words. Drop the workflow name. |
| 02-13 | low | `plugins/sdd/shared/artifacts/requirements.md` (skeleton) | "## Open Questions" is appended by spec-analyze (`spec-analyze/SKILL.md:19`) but missing from the skeleton. | Add the section to the skeleton. |
| 02-14 | med | `plugins/sdd/shared/artifacts/design.md:3-11` | Design Done-when does not require that requirements are met. The Redis script cannot discard a timed-out write (1.8). The gap was recorded. The design gate did not block it. | Add a "Known gaps vs requirements" block that the gate must show. |
| 02-15 | low | `plugins/sdd/shared/gate.md:6` | "Analyze first (runs `/spec-analyze` flow)". The return path to the gate is not stated. I reran the gate by hand. | Add: after analyze, return to step 1 of the gate. |

## Ambiguity log
- "Kebab-case from input" (`spec-new/SKILL.md:13`) → name from feature words → input named both. Chose `shortlinks-rate-limit`.
- "Repeat steps 3–4 until … Max 3 rounds" (`spec-analyze/SKILL.md:21`) → round = one analyst dispatch, first dispatch = round 1 → cap reached after round 3, round-3 edits not rechecked.
- "group related, ≤4 per call" (`spec-analyze/SKILL.md:17`) → asked one question per finding → no grouping key given.
- "Set phase `draft`" only in requirements step (`requirements-first.md:9`) → I set `draft` for design and tasks when drafted. State file allows it (`state.md:16`).
- "after code it tests" (`correctness.md:10`) → test leaf wave must be later than every non-optional leaf in its group.
- "Testing Strategy lists every property" (`design.md:10`) → listed Properties 1–5 by number.
- Gate 2 request "name the window algorithm" → chose fixed Window. It matches the Glossary (requirements.md). Sliding was rejected for memory cost.
- Requirement 1.8 discard rule → could not be met by a remote script. Recorded as known gap; not hidden.

## Hard-to-follow instructions (small model)
- `spec-analyze/SKILL.md:21`: "Repeat steps 3–4 until `NO FINDINGS` or only deferred remain. Max 3 rounds." Round counting and cap behavior unclear.
- `spec-analyze/SKILL.md:17`: "group related, ≤4 per call". Grouping key undefined.
- `shared/correctness.md:7`: "None fits → ask user; skip steps 2–4 on decline." Two branches, one skip rule.
- `shared/correctness.md:10`: "optional `*`, after code it tests." "After" is undefined. Needed wave logic.
- `shared/artifacts/design.md:10`: "Testing Strategy lists every property from `…/correctness.md`". Source list does not exist.
- `shared/workflows/requirements-first.md:11`: "Offer `/spec-analyze` first when: … or ambiguity seen." "Ambiguity seen" is subjective.
- `shared/gate.md:6`: "Requirements phase adds: Analyze first (runs `/spec-analyze` flow)." The flow needs a tool the skill does not list. Return path not stated.
- `shared/state.md:16`: "Phase values: `pending` → `draft` → `approved`." Trigger for `draft` on design and tasks not stated.

## Metrics
- Questions asked: 22 (scripted 22, unscripted 0) · Subagent dispatches: 3 (spec-analyst) · Gates: 3 (5 gate answers) · Tests run: 0 pytest (no code phase); validator 1 run, PASS (1 pass / 0 fail)

## State check at each gate
| Gate | Expected (state.md / gate.md) | `.spec.json` after | Match |
|---|---|---|---|
| Gate 1 first draft | requirements `draft` (requirements-first.md:9) | requirements `draft` | Yes |
| Analyze rounds 1–3 (phase draft) | no change (not approved) | requirements `draft` | Yes |
| Gate 1 approve | requirements `approved` (gate.md:8) | requirements `approved` | Yes |
| Design draft | design `draft` (not stated in plugin; state.md:16) | design `draft` | Inferred (02-5) |
| Gate 2 request changes | no change (gate.md:3) | design `draft` | Yes |
| Gate 2 approve | design `approved` | design `approved` | Yes |
| Tasks draft | tasks `draft` (inferred) | tasks `draft` | Inferred (02-5) |
| Gate 3 approve | tasks `approved` | tasks `approved` | Yes |
| Stale marking | none expected: no upstream edit after approval | no `stale` | Yes |

REPORT: /Users/baodang/Documents/code/agent-skills/docs/sdd-eval/02-reqfirst-haiku/report.md RESULT: PARTIAL ISSUES: 15

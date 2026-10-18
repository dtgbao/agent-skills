# a1-giftcards eval — plugin 0.3.4, reused session

Orchestrator: Opus 5.5 (claude-opus-5-5), effort low · Result: PASS

The 0.3.3 run happened earlier in this session. For this run I read every SKILL.md, agent file and shared file again from disk. I did not reuse findings, answers or text from the 0.3.3 run.

## Plugin load
- Slash command expanded? No. The commands came as a cross-session message, so all 3 ran as `manual load` (`eval/commands.md`).
- `${CLAUDE_PLUGIN_ROOT}` resolved by hand, e.g. `/Users/baodang/Documents/code/agent-skills/plugins/sdd/shared/correctness.md`. `plugin.json` version = `0.3.4`.
- `sdd:spec-analyst` and `sdd:spec-task-runner` were both available, and all 10 dispatches used them.
- Frontmatter applied. The analyst (no `model` passed) reported "Sonnet 5.5 (claude-sonnet-5-5) … Read, Glob, Grep". The runners reported opus or sonnet as passed. The haiku runner (1.1) omitted the model line the prompt asked for. Each report arrived as a SubagentHandback message.

## Summary
- spec-analyze ran 3 rounds (FULL, FOCUSED, FOCUSED) and 2 VERIFY passes. The analyst gave 16 findings and the orchestrator cross-check added 4. 18 were applied. F19 and F20 (medium) were left after the last VERIFY and went to `## Open Questions`.
- Criteria went from 12 to 20 (+67 %, one removed). Growth is over 50 %, so the skill recommends a spec split.
- spec-new resumed at `design`: design.md (4 components, 12 properties) and tasks.md (5 leaves, 4 waves, `check-tasks` PASS + 1 WARN). Both gates were approved.
- spec-run (`--mode waves --optional`): 5/5 leaves done on attempt 1, 3 checkpoints green, **16 tests pass**.
- All 4 0.3.4 checks held (M1–M4, below). The weak point: the CHECK line is a self-report and was wrong on 5 of 16 findings.

## 0.3.4 checks

### M2 — where each NEEDS_OWNER answer went
Rule (`skills/spec-analyze/SKILL.md:19`): an answer that names an interface or type goes to the Glossary or the design Data Models; an answer that names a behavior becomes a criterion.

| Finding | Owner answer (conservative, logged in `QA.md`) | Went to | Evidence |
|---|---|---|---|
| F5 Merchant_Portal | staff UI outside repo; calls `POST /gift-cards/<code>/void`; staff = `ctx["actor"]["role"] == "staff"` | Interface → Glossary **Merchant_Portal**, **Actor**. Behavior (non-staff rejected) → new criterion **3.3**. 3.1 text unchanged. | `apply-log.md` Round 1 |
| F12 refund fails | HTTP 503 `refund_failed` | Behavior → criterion **5.4** | `apply-log.md` Round 2 |
| F13a missing actor | reject 401 `actor_required` | Behavior → criterion **5.5** | `apply-log.md` Round 2 |
| F13b creation old value | `null` | Data value → Glossary **Ledger_Entry**, no criterion | `apply-log.md` Round 2 |

Result: every owner answer went where the rule says. No interface name became a criterion.

### M3 — CHECK lines
Full table: `eval/check-audit.md`.
- The CHECK line was present on **16/16** analyst findings. F10, F11, F14 and F15 came from the orchestrator cross-check, so they have no CHECK line.
- **7** fail the literal step-3 test (`gaps=1 shall=1 asserts=1`): F1, F5, F6, F8, F12, F13, F16.
  - F5 and F12 fail only because a NEEDS_OWNER option has `shall=0 asserts=0`. That is correct for an owner question, so there was nothing to repair.
  - **5 real fails**, all repaired before asking:
    - F1: option B had 2 assertions → narrowed.
    - F6: A and B closed 2 gaps → split.
    - F8: A had 2 assertions → part dropped at apply.
    - F13: one owner question held 2 gaps → split.
    - F16: 2 assertions → trailing clause dropped.
  - In all 5 real fails, the self-reported CHECK said `gaps=1 … asserts=1`. Only the orchestrator's own count caught them.

### M4 — cross-check of changed criteria
Full table: `eval/cross-check.md`. It ran after each apply: round 1, round 2, round 3 and VERIFY 1.

| Apply | Clashes found | New finding → fix |
|---|---|---|
| Round 1 | 2.5 vs 2.1 (subtract vs reject for subtotal > balance) | F10 → 2.1 scoped to subtotal ≤ balance |
| Round 1 | 4.1 "until … balance reaches 0" vs Glossary status set | F11 → 4.1 "until a staff member voids it" |
| Round 2 | 5.4 vs 5.2 (two error codes, same input) | F14 → 5.4 "instead of `ledger_unavailable`" |
| Round 2 | 5.5 vs 3.3 (no actor on void: 401 vs 403) | F15 → 5.5 scoped to purchase/redemption |
| Round 3, VERIFY 1 | none | — |

What the cross-check missed:
- In round 1 it passed 4.1 "with its balance" vs 2.1. The analyst caught this in round 3 (F16).
- It noted 5.5 vs 1.4/2.4 check order as "design choice", and it did not compare 2.5 with 3.2. VERIFY 1 raised both (F17, F18).

### M1 — runner prompts held the cited criterion text
Each prompt was built from `tasks.md` + `requirements.md` and saved before dispatch in `eval/prompts/<leaf>.md`. Each prompt has a "Cited criterion text" block with one line per id in `_Requirements:_`:

| Leaf | Ids cited | Lines in prompt | Runner NOTES list criterion ids |
|---|---|---|---|
| 1.1 | 2 | 2 | yes (5.1, 5.2) |
| 1.2 | 19 | 19 | yes, with file:line |
| 3.1 | 6 | 6 | yes (2.2 noted "not asserted here") |
| 5.1 | 9 | 9 | yes |
| 5.2 | 11 | 11 | yes |

## Step trace
| Skill | Step | Action | Done-when held | Evidence |
|---|---|---|---|---|
| spec-analyze | 1 | drift NO DRIFT, N0 = 12 | yes | transcript |
| spec-analyze | 2 | D1 FULL, `model` omitted | yes (9 findings) | `analyst-round-1.md` |
| spec-analyze | 3 | CHECK audit; F1 narrowed, F6 split; 3 calls ≤4, grouped by requirement | yes | `QA.md`, `check-audit.md` |
| spec-analyze | 4 | apply; owner split Glossary/criterion; renumber 1.3→1.5; 4.2 removed; cross-check → F10, F11 → resolve + apply; `SPEC edited` | yes | `apply-log.md`, `cross-check.md` |
| spec-analyze | 5 r2 | D2 FOCUSED → F12, F13 (both NEEDS_OWNER); F13 split; cross-check → F14, F15 | yes | `analyst-round-2.md` |
| spec-analyze | 5 r3 | D3 FOCUSED → F16; clause dropped | yes | `analyst-round-3.md` |
| spec-analyze | 5 VERIFY 1 | D4 on 13 ids + Glossary → F17, F18 → resolve + apply | yes | `analyst-round-4-verify.md` |
| spec-analyze | 5 VERIFY 2 | D5 on 3.2, 5.5 → F19, F20 → Open Questions; growth 12 → 20 reported | yes | `analyst-round-5-verify.md` |
| spec-new | 1 | Resume (Script); drift clean; jump to design | yes | `QA.md` |
| spec-new | RF 4–5 | design.md; F19, F20 decided under Key design decisions; draft + approve | yes | `.spec.json` |
| spec-new | RF 6–7 | tasks.md; `check-tasks` PASS; draft + approve | yes | `.spec.json` |
| spec-run | 1–4 | drift clean, all approved, waves, 5 leaves in scope, `check-tasks` PASS | yes | transcript |
| spec-run | 5 | 4 waves; 3.1 + 5.1 dispatched in one message; checkpoints 2, 4, 6 green (3 → 9 → 16 tests) | yes | `dispatch.md` |
| spec-run | 7 | no `[ ]` / `[-]` left | yes | `tasks.md` |

## Dispatches
| # | Leaf/round | Size | Model passed | Attempt | Status | Notes |
|---|---|---|---|---|---|---|
| D1 | analyst FULL | — | (omitted) | 1 | 9 findings | CHECK 9/9 |
| D2 | analyst FOCUSED r2 | — | (omitted) | 1 | 2 findings | both medium non-INCONSISTENCY: FOCUSED mode breach |
| D3 | analyst FOCUSED r3 | — | (omitted) | 1 | 1 finding | caught clash the cross-check missed |
| D4 | analyst VERIFY 1 | — | (omitted) | 1 | 2 findings | check-order clashes |
| D5 | analyst VERIFY 2 | — | (omitted) | 1 | 2 findings | → Open Questions |
| D6 | 1.1 | S | haiku | 1 | done | no model line |
| D7 | 1.2 | L | opus | 1 | done | 17 quick checks |
| D8 | 3.1 | M | sonnet | 1 | done | parallel with D9 |
| D9 | 5.1 | M | sonnet | 1 | done | 6 properties |
| D10 | 5.2 | M | sonnet | 1 | done | edited generator after a red run (see I4) |

## Artifact checks
| Artifact | Done-when item | Pass/Fail | Evidence |
|---|---|---|---|
| requirements.md | chosen options applied; EARS (1 SHALL, ≤40 words) | Pass | `apply-log.md` |
| requirements.md | no open high/medium outside Open Questions | Pass | F19, F20 in Open Questions |
| requirements.md | growth reported | Pass | 12 → 20 |
| design.md | every criterion mapped, classified; 12 properties in Testing Strategy | Pass | Criteria Classification 20 rows |
| design.md | Open Questions decided | Pass | Key design decisions F19, F20 |
| design.md | Mermaid, `diff` tree, call tree, non-functional owner | Pass | design.md |
| tasks.md | `check-tasks` RESULT: PASS | Pass | 1 WARN (checkpoint 4 shares a wave with 5.1) |
| tests | property tags, ≥100 examples | Pass | 12 tags; `max_examples=100` |
| tests | suite green | Pass | 16 passed |
| .spec.json | all phases approved | Pass | NO DRIFT after run |

## Issues
| ID | Severity | Plugin file:line | Problem | Proposed fix |
|---|---|---|---|---|
| I1 | medium | agents/spec-analyst.md:56-59 · skills/spec-analyze/SKILL.md:17 | CHECK is a self-report. 5 of 16 findings reported `gaps=1 … asserts=1` but failed when counted (F1, F6, F8, F13, F16). Step 3 repairs only when the line is missing or not the right value, so a skill-following orchestrator that trusts the line misses all 5. | Step 3: "Recount gaps, SHALL and assertions per option; ignore the CHECK value when your count differs." Analyst: list the assertions (e.g. `asserts=1 [returns 409]`) so a miscount is visible. |
| I2 | low | skills/spec-analyze/SKILL.md:17 | The test `gaps=1 shall=1 asserts=1` fails every correct NEEDS_OWNER finding (`shall=0 asserts=0 owner=sole`). Read literally, F5 and F12 "need repair" when nothing is wrong. | Accept `gaps=1 owner=sole` for an owner finding. |
| I3 | medium | skills/spec-analyze/SKILL.md:19 | "Shares a term" did not make the cross-check compare two rejection rules that match the same input. Check-order clashes (F17, F18, F19, F20) reached VERIFY. F19 and F20 were still open at the end. 4.1 vs 2.1 was missed too (F16). | Add: "For each changed rejection criterion, list other rejection criteria that can match the same input; their order must be stated." |
| I4 | low | agents/spec-task-runner.md:15 | Runner 5.2 had a red property run (P11). It fixed its own generator and re-ran, and did not stop with STATUS `failed` + COUNTEREXAMPLE. The fix was right (a generated `/` changed the route), but the rule says stop and let the user pick. | Allow a test-only fix when the counterexample is not valid input for the property, and require it to be reported under COUNTEREXAMPLE as `fixed test: <input>`. Or make the stop rule more visible. |
| I5 | low | agents/spec-analyst.md:15 | FOCUSED round 2 returned 2 medium FAILURE/EDGE findings. FOCUSED allows those types only when high. The analyst named the breach itself. | Say what to do with real medium gaps in FOCUSED: report them as low, or as "Notes" after the findings. |

## Metrics
- Questions: spec-analyze had 8 question calls (calls 1–3, cross-check r1, call 4, cross-check r2, round 3, VERIFY 1), 20 items. 4 owner answers (F5, F12, F13a, F13b), all conservative and logged. 0 `UNSCRIPTED`. spec-new had 1 resume question and 2 gates.
- Dispatches: 10. Analyst 5 (sonnet via frontmatter). Runner 5: haiku 1, sonnet 3, opus 1.
- Retries/escalations: 0. Counterexamples reported: 0 (one self-fixed red run, I4).
- Gates: design Approve, tasks Approve. Checkpoints: 3 green, 0 red.
- Tests: 16 pass, 0 fail.
- Criteria: 12 → 20 (+67 %). Open Questions: F19, F20, both decided in design.
- Compared with the 0.3.3 run (same session): 0.3.3 grew criteria 12 → 23 (+92 %); 0.3.4 grew them 12 → 20 (+67 %). Owner-answer interfaces now go to the Glossary, so fewer criteria were added.

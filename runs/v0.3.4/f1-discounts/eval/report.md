# f1-discounts-v033 eval: plugin 0.3.4, reused session

Orchestrator: Opus 5.5 (claude-opus-5-5), effort low · Result: PASS

## Plugin load
- Slash command expanded? No. The first command came as a cross-session message in plain text. All four skill runs are `manual load` (`eval/commands.md`). I read every SKILL.md, agent and shared file again from disk (`plugin.json` version `0.3.4`).
- `${CLAUDE_PLUGIN_ROOT}`: I set it by hand to `/Users/baodang/Documents/code/agent-skills/plugins/sdd`. Resolved path: `/Users/baodang/Documents/code/agent-skills/plugins/sdd/shared/scripts/spec.py` (prints `INIT docs/specs/discount-codes requirements-first`).
- Agent types `sdd:spec-task-runner` and `sdd:spec-analyst` are available, with their frontmatter tool lists.
- Model: the analyst got no `model`, so it used the frontmatter `sonnet`. All runners got `sonnet` (every leaf is Size M). No agent said which model it ran as. Every report came back as a hand-back message.

## Summary
- All 5 Script commands ran to the end. The spec `docs/specs/discount-codes` has a new name and new text, not taken from the 0.3.3 run. It has 5 requirements (25 → 29 criteria), 3 components, 7 properties, and 6 leaves in 4 waves.
- Analyze had 5 rounds: FULL (6 findings), FOCUSED (1), FOCUSED (NO FINDINGS), VERIFY (2), VERIFY (1). The analyst raised 11 findings, and the cross-check raised 1 more (F10). 3 NEEDS_OWNER answers went to the Glossary.
- Run 1: 6 leaves, each done in the first attempt. 16 tests pass.
- Hand edit 90 → 50. Drift gave `CHANGED 1.2`, `AFFECTS 1.2 -> 1.1 1.2`, and `SUSPECT 1.2 -> 3.2 tests/test_cart_codes.py:20 (90)`. Sync unticked 1.1, 1.2 and 3.2. Run 2 fixed all three. 16 tests pass. No percent bound of 90 is left in `shop/` or `tests/`.
- On run 2, checkpoint 2 went red on 3.2's stale test. The run deferred it correctly and it was green after 3.2.

## 0.3.4 checks

### M1: the runner prompt held the cited criterion text, and runner NOTES named the ids
| Dispatch | Leaf | Cited ids in prompt | Criterion text in prompt | NOTES name ids |
|---|---|---|---|---|
| D6 | 1.1 | 12 | yes (`eval/prompt-1.1-run1.txt`) | "Covers 1.1-1.7, 4.1-4.3, 4.5, 4.6" |
| D7 | 1.2* | 12 | yes | "Covers 1.1-1.7 … 4.1-4.3, 4.5, 4.6" |
| D8 | 3.1 | 13 | yes | "2.1-2.7, 3.1, 3.2, 4.3-4.6" |
| D9 | 3.2* | 10 | yes | "4.4 (P4) … 2.1-2.7 (P5) … 3.1/3.2 (P6)" |
| D10 | 5.1 | 7 | yes | "Covers 5.1-5.7" |
| D11 | 5.2* | 7 | yes | one test name per id 5.1–5.7 |
| D12 | 1.1 (run 2) | 12 | yes; 1.2 says `1–50` | "fixed PERCENT_RANGE … to meet 1.2" |
| D13 | 1.2* (run 2) | 12 | yes; leaf text did not change, only the cited 1.2 text carries `1–50` | "changed the percent range from 1–90 to 1–50" |
| D14 | 3.2* (run 2) | 10 | yes (1.2 is not cited; the sync Do note carried `1–50`) | "4.4, 2.1-2.7, 3.1-3.2"; names 1.2 as the cause |

Result: 9 of 9 held. D13 shows that the cited text alone was enough to carry the new bound to the runner. The prompt builder is `scratchpad/prompt.py`, and each prompt is saved as `eval/prompt-<leaf>-run<n>.txt`.
Gap: D8 and D10 report done, but their runner Done-when ("every cited criterion id has a test case or check in your `Verify`") did not hold. Both say "no per-criterion tests" (I3).

### M2: where each NEEDS_OWNER answer went
| Finding | Question | Answer (Script rule: conservative value) | Went to |
|---|---|---|---|
| F1 | source of Current_Date | `ctx["today"]`, a `datetime.date`; Cart methods take `today` | Glossary `Current_Date` (not a criterion; analyst id 5.6 unused) |
| F2 | Code_Book owner and create API | `shop.discounts.CodeBook` in `ctx["code_book"]`; `CodeBook.create(...)` raises `ValueError` | Glossary `Code_Book` (analyst id 5.7 unused) |
| F7 | attach signature and refusal signal | `attach_code(code, code_book, today)`; raises `AttachRefused` with `.reason`; detach/discount/amount-due methods | Glossary `Cart code methods` (analyst id 2.8 unused) |
All three are interfaces or types, so per spec-analyze step 4 none became a criterion. Design Data Models repeats them.

### M3: every analyst finding had a CHECK line, and how many failed and were repaired
| Round | Finding | CHECK as written | Literal test | Real defect | Repair |
|---|---|---|---|---|---|
| FULL | F1 | `gaps=1 shall=0 asserts=0 owner=sole` | fail | none (NEEDS_OWNER has no SHALL) | none; logged I1 |
| FULL | F2 | `gaps=1 shall=0 asserts=0 owner=sole` | fail | none | none; I1 |
| FULL | F3 | `gaps=1 shall=1 asserts=1 owner=none` | pass | A changed 4.5 and 4.6 (2 criteria) | split into F3a/F3b |
| FULL | F4, F5, F6 | pass | pass | none | none |
| FOCUSED 2 | F7 | `gaps=1 shall=1 asserts=1 owner=sole` | pass | CHECK is false: an owner option has no SHALL | none to the finding; I1 |
| VERIFY 1 | F8 | pass | pass | A had 2 assertions (500 + carts unchanged) | split into 5.6 and 5.7 |
| VERIFY 1 | F9 | pass | pass | none | none (low, deferred) |
| VERIFY 2 | F11 | pass | pass | none | none (left after the last verify → Open Questions) |
Totals: 9 findings with a CHECK line (F1–F9, F11), and 2 rounds returned NO FINDINGS. 2 findings failed the literal test, and neither was a real defect. 2 findings passed but held real defects that I repaired (F3, F8). 1 CHECK value was false (F7). So the CHECK line was right on 6 of 10 findings.

### M4: the cross-check of changed criteria ran, and any clash it found
| Apply | Changed ids | Cross-checked against | Clash |
|---|---|---|---|
| Round 1 | 1.7, 2.7, 4.5, 4.6 | 1.1–1.3; 2.2–2.6, 5.2; 4.1–4.4, 2.4; 2.3 | none |
| Round 2 | none (Glossary only) | — | — |
| Verify 1 | 5.6, 5.7 | 5.1–5.5; 2.6, 3.1 | **5.3 vs 5.6**: a PUT with no `code` and a bad context gives 400 by 5.3 and 500 by 5.6 |
| F10 (from clash) | 5.6 replaced: "before any body check" | 5.3, 5.1, 5.4, 5.5 | none |
The cross-check ran 3 times and found 1 clash. It became F10 (INCONSISTENCY, medium) and went back to step 3 before the next round. The answer was A (Q6). VERIFY 2 then found a sibling gap, F11 (bad context vs 404). Evidence: `eval/apply-log.md`.

## Step trace
| Skill | Step | Action | Done-when held | Evidence |
|---|---|---|---|---|
| spec-new | 1–4 | name `discount-codes`, Requirements-First named, `SPEC init` | yes | `.spec.json` |
| req-first | 1–2 | read README, manifest, shop/*; draft 5 req / 25 criteria | yes | grep `SHALL.*SHALL` = 0 |
| gate (req) | 1–3 | draft, count line, Analyze first | yes | QA Q1 |
| spec-analyze | 2–4 FULL | D1; F1/F2 owner, F3 split, F4/F5 → A, F6 deferred; cross-check | yes | QA Q2–Q3, apply-log |
| spec-analyze | 5 FOCUSED ×2 | D2 (F7 owner), D3 NO FINDINGS → stop | yes | QA Q4 |
| spec-analyze | 5 VERIFY | D4 → F8 split → apply → cross-check clash → F10 → apply → D5 → F11 → Open Questions | yes | QA Q5–Q6 |
| gate (req) | 1, 2, 5 | `5 requirements, 29 criteria (25 → 29)`, open F11 shown, Approve | yes | QA Q7 |
| req-first | 4–5 | design: 3 components, 7 properties, 29 classified, F6/F9/F11 decided; Approve | yes | QA Q8 |
| req-first | 6–7 | tasks 6 leaves 4 waves, check-tasks PASS (2 WARN), Approve | yes | QA Q9 |
| spec-run #1 | 1–7 | waves 0–3, waves 1 and 2 each sent in one message, checkpoints green | yes | D6–D11, `eval/run-1.md` |
| hand edit | — | requirements.md:5, 18, 37 | — | text only |
| spec-sync | 1–2 | DRIFT/STALE/CHANGED/AFFECTS/SUSPECT; design.md:73, 102 refined, Approve | yes | `eval/sync-drift.txt`, QA Q10 |
| spec-sync | 3–6 | matrix, evidence, proposal, Apply all, approve tasks | yes | `eval/sync-proposal.md`, QA Q11 |
| spec-run #2 | 1–7 | 1.1 → 1.2 → checkpoint 2 red, deferred → 3.2 → all green | yes | D12–D14, `eval/run-2.md` |

## Dispatches
| # | Leaf/round | Size | Model passed | Attempt | Status | Notes |
|---|---|---|---|---|---|---|
| D1 | analyst FULL | — | omitted (sonnet) | 1 | 6 findings | F3 needed a split |
| D2 | analyst FOCUSED | — | omitted | 1 | 1 (F7) | false CHECK |
| D3 | analyst FOCUSED | — | omitted | 1 | NO FINDINGS | stopped early |
| D4 | analyst VERIFY | — | omitted | 1 | 2 (F8, F9) | F8 needed a split |
| D5 | analyst VERIFY | — | omitted | 1 | 1 (F11) | → Open Questions |
| D6 | 1.1 | M | sonnet | 1 | done | — |
| D7 | 1.2* | M | sonnet | 1 | done | same message as D8 |
| D8 | 3.1 | M | sonnet | 1 | done | Done-when gap |
| D9 | 3.2* | M | sonnet | 1 | done | same message as D10 |
| D10 | 5.1 | M | sonnet | 1 | done | Done-when gap |
| D11 | 5.2* | M | sonnet | 1 | done | — |
| D12 | 1.1 (run 2) | M | sonnet | 1 | done | 90 → 50 |
| D13 | 1.2* (run 2) | M | sonnet | 1 | done | new bound came from the cited text only |
| D14 | 3.2* (run 2) | M | sonnet | 1 | done | 90 → 50 split |

## Artifact checks
| Artifact | Done-when item | Pass/Fail | Evidence |
|---|---|---|---|
| requirements.md | 2–7 criteria per requirement | Pass | 7, 7, 2, 6, 7 |
| requirements.md | one SHALL, ≤40 words | Pass | grep `SHALL.*SHALL` = 0; longest (5.6) is 37 words |
| requirements.md | terms in Glossary, inputs bounded | Pass | VERIFY passes found no ASSUMPTION |
| requirements.md | failure/edge criterion per input requirement | Pass | 1.2–1.7, 2.2–2.7, 3.2, 5.2/5.3/5.6 |
| design.md | every criterion mapped; Classification lists 29 | Pass | table rows 1.1–5.7 |
| design.md | Mermaid, `diff` tree, call trees | Pass | sequenceDiagram, 4 `diff` blocks |
| design.md | Open Questions decided | Pass | F6, F9, F11 under Key design decisions |
| tasks.md | `check-tasks` PASS | Pass | before and after sync |
| .spec.json | all phases approved, no stale | Pass | end state |
| code | bound follows the edit | Pass | `shop/discounts.py:6` `(1, 50)` |
| tests | full suite | Pass | 16 passed |

## Issues
| ID | Severity | Plugin file:line | Problem | Proposed fix |
|---|---|---|---|---|
| I1 | medium | skills/spec-analyze/SKILL.md:17; agents/spec-analyst.md:56 | The CHECK target `gaps=1 shall=1 asserts=1` does not fit NEEDS_OWNER findings, which have no SHALL. The analyst wrote `shall=0` one time (a literal fail) and `shall=1` one time (false). | Give owner findings their own target: `gaps=1 shall=0 asserts=0 owner=sole`. Repair only on a mismatch with the target for that finding type. |
| I2 | medium | agents/spec-analyst.md:59 | The analyst writes CHECK about itself, so it can say pass when the option fails. F3 A changed 2 criteria, and F8 A had 2 assertions. Both said `asserts=1`. | Add `ids=1` (option touches one criterion) to CHECK. In spec-analyze step 3, the orchestrator counts SHALLs and assertions itself and does not trust CHECK. |
| I3 | low | agents/spec-task-runner.md:13 | The step 1 Done-when ("every cited id has a check in your Verify") cannot hold for code leaves whose tests sit in a later test leaf. D8 and D10 reported done anyway. | Add "…or is cited by a `Kind: test` leaf that deps on this leaf". |
| I4 | low | skills/spec-run/SKILL.md:20 | The prompt carries only criteria in `_Requirements:_`. A confirmed SUSPECT leaf (3.2) needed the changed 1.2 text. Sync had to add a Do note by hand. | spec-sync step 5: for a confirmed SUSPECT, add the changed id to that leaf's context (or spec-run adds SUSPECT ids to the prompt). |
| I5 | low | agents/spec-task-runner.md:37 | NOTES must "cite file:line from `git diff`", but new untracked files have no diff. 6 of 9 reports say "untracked, no git diff" and give no line. | Allow `git diff --no-index /dev/null <file>` or `grep -n` for new files. |
| I6 | low | skills/spec-analyze/SKILL.md:22 | After the last VERIFY, a medium finding (F11) goes to Open Questions with no question asked. Design then decides it alone. The rule holds, but the owner never sees the option text. | At the gate, list each high/medium Open Question with its A/B options, so the user can answer or approve it as deferred. |

## Metrics
- Questions: 11 logged (Q1–Q11). 0 UNSCRIPTED. 3 NEEDS_OWNER answers set by the Script rule. 3 low findings deferred without a question (F6, F9; F11 is medium and was left after the last verify).
- Dispatches: 14. spec-analyst 5 (sonnet by frontmatter). spec-task-runner 9 (sonnet 9, haiku 0, opus 0).
- Retries/escalations: 0. Failed leaves: 0. Counterexamples: 0.
- Gates: requirements shown 2 times (Analyze first, then Approve), design 2 times (spec-new, spec-sync), tasks 1 time, sync Apply all 1 time.
- Checkpoints: run 1 3/3 green. Run 2: 1 red, deferred by rule, then 3/3 green.
- Tests: 16 passed, 0 failed (`uv run --no-project --with pytest --with hypothesis python -m pytest -q`). Nothing committed.

REPORT: /Users/baodang/Documents/code/sdd-mock/f1-discounts-v033/eval/report.md RESULT: PASS ISSUES: 6

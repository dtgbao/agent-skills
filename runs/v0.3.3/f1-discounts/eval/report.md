# f1-discounts-v033 eval

Orchestrator: Opus 5.5 (claude-opus-5-5), effort low · Result: PASS

## Plugin load
- Slash command expanded? No. The first message came from another session as plain text, with no skill body. All 4 skill runs are `manual load` (`eval/commands.md`).
- `${CLAUDE_PLUGIN_ROOT}` resolved: I set it by hand to `/Users/baodang/Documents/code/agent-skills/plugins/sdd`. Example resolved path: `/Users/baodang/Documents/code/agent-skills/plugins/sdd/shared/scripts/spec.py` (runs, prints `INIT ...`).
- Agent types `sdd:spec-task-runner` and `sdd:spec-analyst` are available. Both are listed with their frontmatter tools (`Read, Write, Edit, Glob, Grep, Bash` / `Read, Glob, Grep`).
- Frontmatter applied: the analyst was dispatched with no `model`, so it used the frontmatter default `sonnet`. Runners got `sonnet` (M) or `haiku` (S). No agent said which model it ran as. Every report came back as a hand-back message, not in the Agent result. The skills expect this.

## Summary
- All 5 Script commands ran to the end. Spec `docs/specs/cart-discount-codes`: 5 requirements, 24 → 28 criteria, 3 components, 8 properties, 6 leaves in 4 waves.
- Analyze: FULL (5 findings) → FOCUSED (NO FINDINGS, stopped early) → VERIFY (1 medium) → VERIFY (NO FINDINGS). 3 NEEDS_OWNER answers came from the Script rule (conservative value), logged in `eval/QA.md`.
- Run 1: 6 leaves done in the first attempt. Suite 22 passed.
- Hand edit 90 → 50: drift gave `CHANGED 1.2`, `AFFECTS 1.2 -> 1.1 1.2`, `SUSPECT 1.2 -> 3.2 tests/test_cart_discount.py:30 (90)`. Sync unticked 1.1, 1.2, 3.2 and checkpoints 2, 4, 6. Run 2 fixed all three leaves. 22 passed. No `90` remains in `shop/` or `tests/`.
- The checkpoint deferral rule worked: checkpoint 2 went red on a later leaf's stale test, and the run deferred it. This fixes the v0.3.1 issue I2.
- I tripped the zsh `$S` word-split trap one time. state.md warns about it. I reran with full command lines.

## Step trace
| Skill | Step | Action | Done-when held | Evidence |
|---|---|---|---|---|
| spec-new | 1 Name | `cart-discount-codes`, dir did not exist | yes | `docs/specs/cart-discount-codes/` |
| spec-new | 2 Size | workflow named → spec needed | yes | input names Requirements-First |
| spec-new | 3 Workflow | Requirements-First from input | yes | `.spec.json` workflow |
| spec-new | 4 State | `SPEC init` | yes | `INIT ... requirements-first` |
| req-first | 1 Context | read README, pyproject, shop/*, tests | yes | stack Python + Hypothesis |
| req-first | 2 Draft req | 5 req, 24 criteria; split a 2-SHALL criterion (4.4) | yes | grep `SHALL.*SHALL` = 0 |
| gate (req) | 1–3 | draft, count line, Analyze first | yes | QA Q1 |
| spec-analyze | 2 FULL | D1 analyst | yes | `eval/analyst-round-1.md` |
| spec-analyze | 3 Resolve | F1,F3 owner; F2,F4,F5 → A | yes | QA Q2–Q3 |
| spec-analyze | 4 Apply | 1.6, 1.7, 2.6, 2.7, 2.2 replaced, Glossary | yes | `eval/apply-log.md` |
| spec-analyze | 5 Recheck | FOCUSED clean → stop; VERIFY → F6 → apply → VERIFY clean | yes | D2–D4, QA Q4 |
| gate (req) | 1, 2, 5 | `5 requirements, 28 criteria (24 → 28)`, Approve | yes | QA Q5, `APPROVED requirements` |
| req-first | 4 Draft design | 3 components, 8 properties, all 28 classified | yes | design.md |
| gate (design) | 1, 2, 5 | Approve | yes | QA Q6 |
| req-first | 6 Draft tasks | 6 leaves, 3 checkpoints | yes | `check-tasks` RESULT: PASS (2 WARN) |
| gate (tasks) | 1, 2, 5 | Approve | yes | QA Q7 |
| spec-run #1 | 1–4 | NO DRIFT, mode waves, scope 6 incl. `*`, PASS | yes | — |
| spec-run #1 | 5 | waves 0–3; wave 1 and wave 2 each sent in one message | yes | D5–D10 |
| spec-run #1 | 5 checkpoints | 2 → 10 passed, 4 → 13 passed, 6 → 22 passed | yes | `eval/checkpoints.md` |
| spec-run #1 | 7 Report | table | yes | `eval/run-1.md` |
| hand edit | — | requirements.md lines 5, 14, 35 | — | text only |
| spec-sync | 1 Load | DRIFT req, STALE design+tasks, CHANGED 1.2 | yes | `eval/sync-drift.txt` |
| spec-sync | 2 Upstream | design.md:79 1–90 → 1–50, gate Approve | yes | QA Q8 |
| spec-sync | 3–4 | coverage matrix; AFFECTS + SUSPECT confirmed | yes | `eval/sync-proposal.md` |
| spec-sync | 5–6 | Apply all; approve tasks; check-tasks PASS | yes | QA Q9; phases all `approved` |
| spec-run #2 | 1–4 | NO DRIFT, scope 1.1, 1.2*, 3.2* | yes | — |
| spec-run #2 | 5 | 1.1 → 1.2 → checkpoint 2 red, deferred → 3.2 → checkpoints green | yes | D11–D13, `eval/checkpoints.md` |
| spec-run #2 | 7 Report | table; no `[-]` left | yes | `eval/run-2.md` |

## Dispatches
| # | Leaf/round | Size | Model passed | Attempt | Status | Notes |
|---|---|---|---|---|---|---|
| D1 | analyst FULL | — | omitted (sonnet) | 1 | 5 findings | F4 B had 2 SHALLs (checklist breach) |
| D2 | analyst FOCUSED | — | omitted | 1 | NO FINDINGS | stopped early |
| D3 | analyst VERIFY | — | omitted | 1 | 1 medium (F6) | — |
| D4 | analyst VERIFY | — | omitted | 1 | NO FINDINGS | — |
| D5 | 1.1 | M | sonnet | 1 | done | said it did not read requirements/design |
| D6 | 1.2* | M | sonnet | 1 | done | 7 passed |
| D7 | 3.1 | M | sonnet | 1 | done | same message as D6 |
| D8 | 3.2* | M | sonnet | 1 | done | — |
| D9 | 5.1 | M | sonnet | 1 | done | same message as D8 |
| D10 | 5.2* | S | haiku | 1 | done | NOTES file:line cites wrong |
| D11 | 1.1 (run 2) | M | sonnet | 1 | done | 90 → 50 |
| D12 | 1.2* (run 2) | M | sonnet | 1 | done | added 45–55 boundary values |
| D13 | 3.2* (run 2) | M | sonnet | 1 | done | 90 → 50 |

## Artifact checks
| Artifact | Done-when item | Pass/Fail | Evidence |
|---|---|---|---|
| requirements.md | 2–7 criteria per requirement | Pass | 7, 7, 2, 6, 6 |
| requirements.md | one SHALL, ≤40 words | Pass | grep `SHALL.*SHALL` = 0 |
| requirements.md | terms in Glossary | Pass | VERIFY found no ASSUMPTION after F6 |
| requirements.md | inputs bounded | Pass | Value, Minimum, Code_String, dates |
| requirements.md | failure/edge per input requirement | Pass | 1.2–1.7, 2.2–2.5, 3.2, 5.2/5.3/5.6 |
| design.md | every criterion mapped | Pass | Criteria Classification lists 28 |
| design.md | Mermaid, `diff` tree, call trees | Pass | sequenceDiagram, 4 `diff` blocks |
| design.md | Testing Strategy lists every property | Pass | 8 rows |
| design.md | Open Questions handled | Pass | none in requirements |
| tasks.md | `check-tasks` PASS | Pass | RESULT: PASS (before and after sync) |
| .spec.json | phases approved, no stale | Pass | all `approved` at end |
| code | percent bound follows edit | Pass | `shop/discounts.py:35` `<= 50`; grep 90 = none |
| tests | full suite | Pass | 22 passed |

## Issues
| ID | Severity | Plugin file:line | Problem | Proposed fix |
|---|---|---|---|---|
| I1 | medium | agents/spec-task-runner.md:12 | Runner D5 skipped step 1. It said it did not read requirements.md or design.md. A leaf whose Do text is incomplete would then drift from the criteria. | Add to Done-when: "NOTES cites ≥1 criterion id it read". Or have spec-run put the cited criterion text in the prompt. |
| I2 | medium | skills/spec-analyze/SKILL.md:19 | Step 4 does not say where a NEEDS_OWNER answer goes. F1, F3 and F6 answers are interface facts (names, types), not behavior. The analyst gave them criterion ids (2.6, 1.6, 1.8). I put them in the Glossary. | Add: "Owner answer that names an interface or type → Glossary or Data Models; a behavior → criterion." |
| I3 | low | skills/spec-analyze/SKILL.md:19 | Apply can push a requirement over the 2–7 cap (shared/artifacts/requirements.md:6). Req 2 would have had 9 criteria. I kept it at 7 by superseding 2.2 and moving owner facts to the Glossary. | Add an Apply rule: count >7 → split the requirement or merge per the supersede rule, and log it. |
| I4 | low | agents/spec-analyst.md:40 | Option numbers are reserved across both A and B (2.7/2.8, 2.9/2.10). After A is chosen, the numbers have gaps, so Apply must renumber. | Number only option A. B reuses A's target id. |
| I5 | low | agents/spec-analyst.md:34 | D1 F4 option B had 2 SHALLs. The checklist forbids this. | Add a final check line: "count SHALL per option = 1". spec-analyze step 3 repair already catches it. |
| I6 | low | agents/spec-task-runner.md:36 | D10 (haiku) NOTES cite `shop/api.py:23-26`. The real mapping is at :33-36. | Ask the runner to take cites from `git diff -U0` or `grep -n`, not from memory. |

## Metrics
- Questions: 9 logged (Q1–Q9). 0 UNSCRIPTED options. 3 NEEDS_OWNER answers set by the Script rule (conservative value).
- Dispatches: 13. spec-analyst 4 (sonnet by frontmatter). spec-task-runner 9: sonnet 8, haiku 1, opus 0.
- Retries/escalations: 0. Failed leaves: 0. Counterexamples: 0.
- Gates: requirements ×2 shows (Analyze first, Approve), design ×2 (spec-new, spec-sync), tasks ×1 + sync Apply all.
- Checkpoints: run 1 3/3 green. Run 2: 1 red deferred (correct per rule), then 3/3 green.
- Tests: 22 passed, 0 failed (`uv run --no-project --with pytest --with hypothesis python -m pytest -q`). Nothing committed.

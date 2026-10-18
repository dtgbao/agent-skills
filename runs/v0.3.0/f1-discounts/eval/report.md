# f1-discounts eval

Orchestrator: Opus 5.5 (claude-opus-5-5), effort low · Result: PASS

## Plugin load
- Slash command expanded? No. The parent session sent command 1 as plain text, so every command ran by manual load (`eval/commands.md`).
- `${CLAUDE_PLUGIN_ROOT}` resolved: yes, by hand. Example: `/Users/baodang/Documents/code/agent-skills/plugins/sdd/shared/workflows/requirements-first.md`. `SPEC` = `python3 /Users/baodang/Documents/code/agent-skills/plugins/sdd/shared/scripts/spec.py`.
- Agent types `sdd:spec-task-runner` and `sdd:spec-analyst` were available and used for all 12 dispatches. No `general-purpose` agent was used.
- Frontmatter: spec-analyst got no `model` and said "Sonnet 5.5 (claude-sonnet-5-5)", which matches frontmatter `sonnet`. The runner said Sonnet 5.5 when sent `sonnet` and Haiku 5.5 when sent `haiku`. Tools held: the analyst only read files; the runners wrote only their own `Files`.

## Summary
- spec-new (Requirements-First) made 3 artifacts in `docs/specs/cart-discount-codes/`, each passing an approval gate. Three FULL analyst rounds and one VERIFY round moved requirements from 22 to 26 criteria. F4, F9 and F11 were deferred.
- spec-run 1 (waves, optional): 5 of 5 leaves done on the first try. Both checkpoints were green, with 15 tests passing.
- Hand edit 90 → 50: `SPEC drift` found DRIFT, CHANGED 1.2, AFFECTS 1.1 and 1.3, plus 2 SUSPECT lines in 3.2. Every suspect was real.
- spec-sync re-gated design with no change and edited the leaf 1.1 text. It unticked 1.1, 1.3 and 3.2 plus their groups and checkpoints, then approved tasks. The next drift check was clean.
- spec-run 2: 3 of 3 leaves done. Checkpoint 2 went red once because leaf 3.2's tests were still stale (Untick leaf). After 3.2 ran, all 15 tests passed. Spot check: percent 50 is accepted and 51 is rejected.
- Main defect: the analyst sees only `requirements.md`. Its F3 option A invented the line-body fields `unit_price_cents` and `quantity`, which clash with the real `sku`/`qty` API.

## Step trace
| Skill | Step | Action | Done-when held | Evidence |
|---|---|---|---|---|
| spec-new | 1 Name | `cart-discount-codes`; dir absent | yes | `ls docs` → none |
| spec-new | 2 Size | workflow named → skip | yes | — |
| spec-new | 3 Workflow | Requirements-First from input | yes | — |
| spec-new | 4 State | `SPEC init` | yes | `INIT docs/specs/cart-discount-codes requirements-first` |
| req-first | 1 Context | read README, pyproject, shop/*, tests | yes | stack = Python, pytest+Hypothesis, typecheck none |
| req-first | 2 Draft req | 4 req / 22 criteria | yes | 2–7 criteria each; one SHALL each (3.4 fixed before gate) |
| gate | 1–3 | draft, Analyze first → spec-analyze 2–5 | yes | Q1, `analyst-round-1..3.md`, `analyst-round-4-verify.md` |
| spec-analyze | 3 Resolve | 8 medium → A; 3 low → deferred | yes | Q2–Q6 |
| spec-analyze | 4 Apply | merged; F7 option A split (2 SHALL) | yes | requirements.md 2.10 |
| spec-analyze | 5 Recheck | rounds 2, 3 FULL; VERIFY → NO FINDINGS | yes | D2–D4 |
| gate | 5 Approve req | `SPEC approve requirements` | yes | Q7 |
| req-first | 4 Draft design | 3 components, 7 properties, 26-row classification | yes | design.md |
| gate | Approve design | | yes | Q8 |
| req-first | 6 Draft tasks | 5 leaves, 4 waves, 2 checkpoints | yes | `check-tasks` RESULT: PASS (21 checks) |
| gate | Approve tasks | | yes | Q9 |
| spec-run 1 | 1–4 | drift none, all approved, scope 5 (optional on), graph PASS | yes | — |
| spec-run 1 | 5 Execute | waves 0..3; wave 2 = 1.3 ∥ 3.1 in one message | yes | D5–D9 |
| spec-run 1 | 5 Checkpoints | 2: 7 passed; 4: 15 passed | yes | `spec-run-1.md` |
| hand edit | — | 2 lines in requirements.md | yes | `grep 1–50` |
| spec-sync | 1 Load | DRIFT / CHANGED 1.2 / AFFECTS / SUSPECT ×2 | yes | `spec-sync.md` |
| spec-sync | 2 Upstream | design re-gated, no change | yes | Q10 |
| spec-sync | 3–4 | matrix + evidence per leaf | yes | `spec-sync.md` |
| spec-sync | 5–6 | Apply all; approve tasks; drift clean | yes | Q11; `RESULT: NO DRIFT`; no `stale` |
| spec-run 2 | 3 Scope | 1.1, 1.3*, 3.2* | yes | — |
| spec-run 2 | 5 Execute | 1.1 → 1.3 → checkpoint 2 red → 3.2 | yes | D10–D12, Q12 |
| spec-run 2 | 5 Checkpoints | 2 and 4 re-run: 15 passed | yes | final tasks.md all `[x]` |

## Dispatches
| # | Leaf/round | Size | Model passed | Attempt | Status | Notes |
|---|---|---|---|---|---|---|
| D1 | analyst round 1 FULL | — | none | 1 | 4 findings | 3 medium, 1 low |
| D2 | analyst round 2 FULL | — | none | 1 | 5 findings | 4 medium, 1 low (NEEDS_OWNER) |
| D3 | analyst round 3 FULL | — | none | 1 | 2 findings | 1 medium, 1 low |
| D4 | analyst VERIFY | — | none | 1 | NO FINDINGS | |
| D5 | run1 1.1 | M | sonnet | 1 | done | |
| D6 | run1 1.2 | S | haiku | 1 | done | |
| D7 | run1 1.3* | M | sonnet | 1 | done | parallel with D8 |
| D8 | run1 3.1 | M | sonnet | 1 | done | parallel with D7 |
| D9 | run1 3.2* | M | sonnet | 1 | done | |
| D10 | run2 1.1 | M | sonnet | 1 | done | reported 2 failing stale tests, still `done` |
| D11 | run2 1.3* | M | sonnet | 1 | done | |
| D12 | run2 3.2* | M | sonnet | 1 | done | |

## Artifact checks
| Artifact | Done-when item | Pass/Fail | Evidence |
|---|---|---|---|
| requirements.md | 2–7 criteria per requirement | Pass | 5 / 10 / 6 / 5 |
| requirements.md | one EARS pattern, one SHALL, ≤40 words | Pass | awk scan: no line has >1 SHALL or >40 words |
| requirements.md | every term in Glossary | Pass | VERIFY: no ASSUMPTION |
| requirements.md | every input bounded | Pass | Code_String, Value, Minimum, Expiry, line body |
| requirements.md | failure/edge per input requirement | Pass | 1.2–1.5, 2.2–2.9, 4.4, 4.5 |
| requirements.md | no unmeasured adjectives | Pass | "usable" removed (F6) |
| design.md | every criterion → component/property | Pass | 26-row table + `_Requirements:_` |
| design.md | interface sketches, Mermaid, `diff` tree, call tree | Pass | sections present |
| design.md | Error Handling per dependency | Pass | ctx today/codes, registry, cart |
| design.md | Testing Strategy lists every property | Pass | 7 rows, ≥100 |
| tasks.md | `check-tasks` RESULT: PASS | Pass | after spec-new and after spec-sync |
| .spec.json | all approved, no stale, drift clean | Pass | end state |
| code | tests | Pass | 15 passed |
| code | 1.2 new bound | Pass | 50 accepted, 51 ValueError |

## Issues
| ID | Severity | Plugin file:line | Problem | Proposed fix |
|---|---|---|---|---|
| I1 | medium | `skills/spec-analyze/SKILL.md:15`, `agents/spec-analyst.md:10` | The analyst gets only the requirements file. F3 option A named new line-body fields (`unit_price_cents`, `quantity`) that clash with the real `sku`/`qty` + `CATALOG` API. With answer "A", the spec forced a breaking API change and a field that is checked but never used. | Pass the stack and the files the requirements name. Tell the analyst to Grep existing interfaces and keep options consistent with them, or use `NEEDS_OWNER` when it cannot. |
| I2 | medium | `skills/spec-run/SKILL.md:23` | On a re-run, a checkpoint runs when its groups above are `[x]`. But the full test command also runs test files owned by later-wave in-scope leaves that are still stale (3.2), so checkpoint 2 goes red and forces an Untick/Continue/Stop question. The answer "Stop" would end the run before 3.2 can fix its tests. | Before the red prompt, check whether the failing test file belongs to an in-scope leaf that has not run yet. If so, defer the checkpoint until that leaf runs, or say so in the prompt. |
| I3 | low | `agents/spec-task-runner.md:18` | D10 returned `STATUS: done` with "2 fail (expected: green)". Its Verify was "existing tests pass". This breaks the runner's own Done-when, but the failures were in files it may not touch. | Add a rule: failures only in files owned by other leaves → `done` plus a `FOREIGN-FAIL: <files>` line. Any other failure → `failed`. |
| I4 | low | `agents/spec-analyst.md:28` | F7 option A had two `SHALL` ("SHALL treat … and SHALL otherwise return"), which breaks the analyst's own rule. The orchestrator split it. | Add a self-check: count `SHALL` per option before output. |
| I5 | low | `skills/spec-analyze/SKILL.md:17` | When a finding is low and also `NEEDS_OWNER` (F9), it is unclear which rule wins: "Low → defer" or "ask the owner question". It was deferred. F9 also left the `ctx` key for the registry open, so design had to choose it (`ctx["codes"]`). | State the precedence. Better: treat `NEEDS_OWNER` on a name that design needs as medium. |

## Metrics
- Questions (QA.md): 12. Gates: 3 in spec-new (requirements, design, tasks) and 1 in spec-sync (design). Analyze rounds: 3 FULL + 1 VERIFY. Findings: 11 (8 medium → A, 3 low → deferred). NEEDS_OWNER asked: 0. UNSCRIPTED answers: 0. One answer was read as a sequence ("Untick leaf, then Stop"; Q12).
- Dispatches: 12 in total. spec-analyst: 4 (model not passed, ran as sonnet). spec-task-runner: sonnet 7, haiku 1.
- Retries/escalations: 0. Failed/blocked leaves: 0. Counterexamples: 1, from a stale test, not the code (D10). The test was fixed by its own leaf 3.2, per the scope.
- Checkpoints: run 1 green ×2. Run 2: red ×1 (checkpoint 2, before 3.2 ran), then green ×2.
- Tests: 15 passed, 0 failed (final). Nothing committed.

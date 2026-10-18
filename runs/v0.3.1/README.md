# sdd v0.3.1: rerun of f1 and a1

Date: 2026-10-18 · Plugin: `sdd@bao-plugins` v0.3.1 (project scope) · Orchestrator: Opus 5.5, effort medium · Fresh copies of the [v0.3.0](../v0.3.0/README.md) mock projects, same scripts

## Verdict

**2 of 2 PASS.** The 0.3.1 fixes work. The analyze loop converges: in a1, round 3 returned `NO FINDINGS`, and criteria growth fell from +115 % to +42 %. Recall stayed at 7 of 7. The spec is smaller in every phase, so the run needs fewer dispatches. The analyst still breaks some of its own option rules. One new defect is real and simple to fix: subagent reports can arrive as a hand-back message, and the skills do not say so.

## 0.3.0 → 0.3.1

| Measure | f1 0.3.0 | f1 0.3.1 | a1 0.3.0 | a1 0.3.1 |
|---|---|---|---|---|
| Result | PASS | PASS | PASS | PASS |
| Criteria before → after analyze | 22 → 26 (+18 %) | 19 → 25 (+32 %) | 13 → 28 (+115 %) | 12 → 17 (+42 %) |
| Findings per round (r1 / r2 / r3 / verify) | 4 / 5 / 2 / 0 | 7 / 1 / 0 / 0 | 13 / 6 / 4 / 3 | 8 / 2 / 0 / 3 |
| Open after verify | 0 | 0 | 3 medium | 2 medium, 1 low |
| Words: requirements / design / tasks | 1145 / 1660 / 712 | 900 / 1530 / 795 | 1047 / 2071 / 1421 | 720 / 1649 / 636 |
| Leaves | 5 | 6 | 14 | 5 |
| Runner dispatches (haiku / sonnet / opus) | 8 (1 / 7 / 0) | 9 (0 / 9 / 0) | 15 (4 / 7 / 4) | 5 (1 / 3 / 1) |
| Retries | 0 | 0 | 1 (no report) | 0 |
| Tests at end | 15 pass | 17 pass | 21 pass | 11 pass |

Each run was checked again after it ended: the suite passes, `check-tasks` prints `RESULT: PASS`, and all phases are `approved`. Note: the count of seed criteria differs (13 vs 12) because the two orchestrators counted differently.

## a1 analyst recall (same answer key)

| Key | Planted defect | 0.3.0 round 1 | 0.3.1 round 1 |
|---|---|---|---|
| K1 | value 10–500 vs balance up to 1000 | F4 ✓ | F4 ✓ |
| K2 | "promptly" | F3 ✓ | F3 ✓ |
| K3 | never expire vs void after 12 months | F1 ✓ | F1 ✓ |
| K4 | `Merchant_Portal`, staff not in Glossary | F2 ✓ | F2 ✓, cites "shop/api.py has no void route" (code grep, R1) |
| K5 | balance < subtotal | F5 ✓ | F5 ✓, notes cents vs dollars from `Cart.subtotal_cents` |
| K6 | Payment_Provider failure | F7 ✓ | F6 ✓ |
| K7 | concurrent redemption | F6 ✓ | F7 ✓ |
| Round-1 findings | | 13 (6 extra) | 8 (1 extra, low) |

Same recall with 40 % fewer findings. The code context (R1) made two findings concrete.

## 0.3.1 fixes seen working

| Fix | Evidence |
|---|---|
| R1 code context | a1 F2, F5 cite the real code |
| R3 FOCUSED rounds | a1 r2: 2 findings, r3: `NO FINDINGS`; f1 r2: 1, r3: 0 |
| R5 checkpoint deferral | f1 run 2: checkpoint 2 red on 3.2's stale test → deferred → green after 3.2 |
| R7 tiers | a1 leaf 1.2 (L) ran on opus, 1.1 (S) on haiku |
| R9 same-wave read | no race in either run; `check-tasks` PASS |
| SUSPECT (0.2.0) | f1: `SUSPECT 3.2 tests/test_cart_discount.py:19` was the real stale test |

## New issues

| # | Sev | Where | Problem | Proposed fix |
|---|---|---|---|---|
| N1 | med | `skills/spec-run/SKILL.md:20-21`, `skills/spec-analyze/SKILL.md:15` | Reports arrive as a hand-back message; the Agent result says only "delivered as a message". A literal "no `STATUS:` line → failed" marks every leaf failed (f1 I1) | "Report may arrive as a hand-back message: read it there before checking `STATUS:`" |
| N2 | med | `agents/spec-analyst.md`, `skills/spec-analyze/SKILL.md:17` | Analyst still breaks option rules: two `SHALL` (f1 F1, a1 F10 B), A/B for different gaps (a1 F6), single non-NEEDS_OWNER option (a1 F7). The unchosen gap leaves no trace | Orchestrator check in step 3 before asking: split multi-gap findings, reject options with ≠1 `SHALL` |
| N3 | med | `skills/spec-analyze/SKILL.md:22` | Medium VERIFY findings go to Open Questions with no decision. Design then decides them silently (a1 I2) | One Resolve ask for high/medium VERIFY findings, no further recheck |
| N4 | med | eval harness (`CLAUDE.md`) | The Script sits in `CLAUDE.md`, which subagents also load. Analyst r3 and runner 1.2 mentioned the future 90 → 50 edit (f1 I2) | Move the Script out of `CLAUDE.md`; give it to the orchestrator only |
| N5 | low | `skills/spec-analyze/SKILL.md:15` | No `model` named for the analyst (a1 I3) | "omit `model` (frontmatter `sonnet`)" |
| N6 | low | `agents/spec-task-runner.md:14` | Runner fixed its own red property test and reported `COUNTEREXAMPLE: none` (a1 I4) | Any red property run → counterexample in the report; self-fix only with a NOTES line |
| N7 | low | `shared/scripts/spec.py` | A checkpoint can run after later-layer code has landed (a1 I5) | `check-tasks` warns when a leaf below a checkpoint sits in a wave ≤ the last wave above it |
| N8 | low | various | `SPEC` as a shell variable fails in zsh (f1 I6); option that supersedes a criterion (f1 I4); sync re-approve wording (f1 I5); `[-]*` mark (a1 I6); unquoted claim in a `NO FINDINGS` note (f1 I7) | One line each |

## Limits

- The slash command still did not expand. Every command ran as a manual load of the installed `SKILL.md`. The agents, the frontmatter and the routing are real.
- N4 means the subagents saw future script steps. The SUSPECT and sync results still hold: the stale test was found by `drift`, not by the runner.

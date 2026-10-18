# sdd v0.3.0: real plugin test

Date: 2026-10-18 · Plugin: `sdd@bao-plugins` v0.3.0, installed at project scope from a local directory marketplace · Orchestrator: Opus 5.5, effort medium (app metadata) · Mock project: [_mock-base](_mock-base) (`mockshop`, Python)

## Verdict

**3 of 3 runs PASS.** The real `sdd:spec-task-runner` and `sdd:spec-analyst` agent types loaded and ran: 35 dispatches, 0 `general-purpose` stand-ins. Size-based model routing works: each runner reported the model that `spec-run` passed. The Sonnet analyst found 7 of 7 planted defects in round 1, with no clear false positives.

Two problems remain:
1. **The analyze loop still grows the spec.** Gift cards went from 13 to 28 criteria and an idempotency and refund subsystem. Rounds 2 and 3 mostly found defects that the applied options created.
2. **The analyst has no code context.** In f1 its option invented API fields that clash with the real `sku`/`qty` API.

## Runs

| Run | Script | Result | Tests | Dispatches | Issues | Report |
|---|---|---|---|---|---|---|
| f1-discounts | Requirements-First + Analyze first → waves → hand edit 90 → 50 → sync → waves | PASS | 15 pass | 12 | 5 (2 med) | [report](f1-discounts/eval/report.md) · [patch](f1-discounts/code.patch) |
| b1-oversell | Bugfix → single → single `--optional` | PASS | 16 pass | 4 | 4 (low) | [report](b1-oversell/eval/report.md) · [patch](b1-oversell/code.patch) |
| a1-giftcards | spec-analyze (seeded, 7 defects) → resume → waves `--optional` | PASS | 21 pass | 19 | 11 (4 med) | [report](a1-giftcards/eval/report.md) · [patch](a1-giftcards/code.patch) |

I checked every run myself after it ended: the test suite passes, `spec.py check-tasks` prints `RESULT: PASS`, and all phases are `approved`. The b1 fix is correct: `shop/inventory.py:16` now compares `qty` with `available()`.

## What this test covered that the simulations did not

| Item | Simulated runs (v0.1–0.2) | This run |
|---|---|---|
| Plugin install (project scope, directory marketplace) | no | yes: `claude plugin list` shows v0.3.0 enabled |
| Agent types `sdd:spec-task-runner`, `sdd:spec-analyst` | `general-purpose` + pasted body | real types, all 35 dispatches |
| Agent frontmatter `model: sonnet` | no | analyst ran as Sonnet with no `model` passed |
| `model` override on each dispatch | no | haiku / sonnet / opus each confirmed by the agent |
| Agent `tools:` limits | no | analyst: Read, Glob, Grep only; runners wrote only their `Files` |
| Slash command expansion, `${CLAUDE_PLUGIN_ROOT}` in skill text | no | **still no** (see Limits) |

## Model routing

| Model | Runner dispatches | First-try done | Notes |
|---|---|---|---|
| haiku (Size S) | 7 | 7 | b1: one report lost its `NOTES:` prefix and cited line 18 (real: 16) |
| sonnet (Size M) | 16 | 15 | a1 leaf 1.1 returned a `placeholder` with no report. The file was written and Verify passed |
| opus (Size L + 1 escalation) | 4 | 4 | escalation of a1 1.1 (sonnet → opus) worked |
| analyst (frontmatter sonnet) | 8 rounds | – | f1: 4, a1: 4 |

Size labels: the drafter marked most leaves M (f1: 1 S of 5; b1: 2 S of 4; a1: 4 S, 3 L of 14). Haiku did every S leaf correctly on the first try, so the S tier pays off. The drafter could mark more leaves S.

## Analyst recall (a1, answer key kept out of the project)

| Key | Planted defect | Round 1 finding |
|---|---|---|
| K1 | 1.1 value 10–500 vs 2.3 balance up to 1000 | F4 high ✓ |
| K2 | 2.2 "promptly" | F3 medium ✓ |
| K3 | 4.1 never expire vs 4.2 void after 12 months | F1 high ✓ |
| K4 | `Merchant_Portal`, staff, store credit not in Glossary | F2 high ✓ (Merchant_Portal), F12 low (actor id). "store credit" missed |
| K5 | balance < subtotal → negative balance | F5 high ✓ |
| K6 | Payment_Provider decline or timeout | F7 high ✓ |
| K7 | concurrent redemption of one card | F6 high ✓ |
| Control | Requirement 5 (audit) clean | F9 (creation needs a ledger entry) is arguably valid; F12 low |

Recall 7/7 (K4 partial). Round 1: 13 findings, 7 key, 6 valid extras, 0 clear false positives. Haiku analyst in v0.1 scenario 05: 7/7 recall, 21 findings, 1 false positive, 3 arguable. Sonnet as the analyst default is justified.

Loop behavior:

| Run | Criteria before → after | FULL rounds | Findings per round | Open after VERIFY |
|---|---|---|---|---|
| f1 | 22 → 26 | 3 | 4, 5, 2 | 0 |
| a1 | 13 → 28 | 3 | 13, 6, 4 | 3 medium |

In a1, round 2 found F14 and F15: inconsistencies that the round-1 options created (2.1 vs the new 2.5/2.7; 404 vs 422). The deterministic EARS check in step 4 does not catch cross-criterion conflicts.

## Issues (merged, new in v0.3.0 runs)

| # | Sev | Where | Problem | Proposed fix |
|---|---|---|---|---|
| R1 | med | `agents/spec-analyst.md`, `skills/spec-analyze/SKILL.md:15` | Analyst sees only the requirements file. Options invent interfaces (f1 I1) | Caller passes stack + files the spec names. Analyst greps existing interfaces; option must fit them, else `NEEDS_OWNER` |
| R2 | med | `agents/spec-analyst.md:28` | Options hold 2 assertions or 2 `SHALL` (7× in a1, 1× in f1); A and B often complementary (a1 I3) | Self-check: one `SHALL`, one assertion per option; A and B mutually exclusive; second gap → second finding |
| R3 | med | `skills/spec-analyze/SKILL.md:22` | Scope growth: 13 → 28 criteria. Rounds 2+ chase defects created by options | Rounds 2+ report only INCONSISTENCY / CONFLICT and high. Show criteria growth at the gate; >50 % → recommend splitting the spec |
| R4 | med | `skills/spec-run/SKILL.md:21` | Runner reply with no `STATUS:` line (a1 D5) has no rule | No `STATUS:` → `failed`, show raw reply, Retry tier up |
| R5 | med | `skills/spec-run/SKILL.md:23` | On re-run, checkpoint goes red on test files of an in-scope leaf in a later wave (f1 I2) | Defer the checkpoint while a failing test file belongs to an unrun in-scope leaf |
| R6 | low | `agents/spec-task-runner.md:18` | Runner said `done` with foreign failures (f1 I3) | Foreign-file failures → `done` + `FOREIGN-FAIL: <files>`; own failures → `failed` |
| R7 | low | `skills/spec-run/SKILL.md:20` | Tier list is implicit ("your own model family") | One list: haiku → sonnet → opus |
| R8 | low | `agents/spec-task-runner.md:14` | `${CLAUDE_PLUGIN_ROOT}` inside an agent body may not resolve; one runner left out the property tag (a1 I7) | `spec-run` passes the resolved `correctness.md` path in the prompt; inline the tag rule in the agent |
| R9 | low | `shared/scripts/spec.py` check-tasks | Same-wave check reads `Files` only, misses `Verify` imports (a1 I8) | Scan backticked paths in `Do` / `Verify` against same-wave `Files` |
| R10 | low | `skills/spec-run/SKILL.md:22` | Group `[x]` while an optional leaf in it is `[ ]` (b1 I2) | Group `[x]` only when every leaf is `[x]`; else note "optional skipped" |
| R11 | low | `shared/artifacts/design.md` | Open Questions from analyze have no home in design (a1 I9) | Done-when: every Open Question is decided in Key decisions or marked out of scope |
| R12 | low | various | NEEDS_OWNER label (a1 I5), duplicate option parts (a1 I6), low + NEEDS_OWNER precedence (f1 I5), bugfix Criteria Classification (b1 I1), implied facts (b1 I3), NOTES format (b1 I4), count line (a1 I11) | One line each in the named file |

## Limits

- **Slash commands did not expand.** The app relays the first prompt of a started session as plain text, so every command ran as a manual load of the installed `SKILL.md`. The agents, the frontmatter and the routing are real. The skill-text expansion of `$ARGUMENTS` and `${CLAUDE_PLUGIN_ROOT}` is still unverified. Check it once by hand: open a session in `~/Documents/code/sdd-mock/b1-oversell`, then type `/sdd:spec-run cart-oversell --mode single`.
- The skills set `disable-model-invocation: true`, so an orchestrator cannot chain `spec-new` → `spec-run` by itself. A human must type each command. This is by design (zero context load), but it blocks fully automated runs.
- The sessions reported "effort low", but the app metadata says medium. Trust the metadata.

## Fixed in 0.3.1 (not re-run yet)

| # | Change |
|---|---|
| R1 | Analyst gets stack, source root, named files; greps interfaces; unknown name → `NEEDS_OWNER` |
| R2 | Option = one `SHALL`, one assertion; A/B exclusive; second gap → second finding |
| R3 | Rounds 2–3 in `FOCUSED` mode (conflicts + high only); growth `N0 → N` reported, >50 % → split advice |
| R4 | No `STATUS:` line → `failed`, raw reply shown, Retry |
| R5 | Checkpoint deferred while a failing test file belongs to an unrun in-scope leaf |
| R6 | Runner: own failure → `failed`; foreign only → `done` + `FOREIGN-FAIL` |
| R7 | Tiers fixed: S haiku, M sonnet, L opus; retry one up, opus stays |
| R8 | Agents take resolved rule paths from the caller; property tag rule inlined |
| R9 | `check-tasks`: same-wave leaf may not name another leaf's file in `Do` / `Verify` |
| R10 | Group `[x]` only when every leaf is `[x]`; checkpoint waits on in-scope leaves |
| R11 | Design Done-when: every Open Question decided or out of scope |
| R12 | NEEDS_OWNER sole option, asked at any severity; duplicate option parts dropped; bugfix design skips classification; implied facts stated; one-line NOTES; count line rule |


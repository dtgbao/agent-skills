# sdd v0.3.3: real plugin eval (f1, b1, a1)

Date: 2026-10-18 · Opus 5.5 medium orchestrator · Script outside `CLAUDE.md`

| Run | Result | Tests (verified) | Criteria growth |
|---|---|---|---|
| f1-discounts (all 5 commands) | PASS | 22 pass | 24 → 28 (+17 %) |
| b1-oversell | PASS | 13 pass | – |
| a1-giftcards | PASS | 13 pass | 12 → 23 (+92 %) |

All: `check-tasks` PASS, all phases `approved`. P1–P8 from 0.3.2 confirmed fixed (no test edit on red, fix flow, red pins exempt, bugfix coverage, decided findings skipped, second VERIFY, numbering).

## Medium issues → fixed in 0.3.4

| # | Source | Problem | Fix |
|---|---|---|---|
| M1 | f1 I1 | Runner skipped reading criteria | spec-run puts each cited criterion's text in the prompt; runner NOTES names the ids checked |
| M2 | f1 I2 | No rule where a NEEDS_OWNER answer goes | Interface or type → Glossary; behavior → criterion |
| M3 | a1 I1 | Analyst breaks its checklist (third round in a row) | Required `CHECK:` line per finding; spec-analyze rejects and repairs any value ≠ 1 |
| M4 | a1 I2 | Applied option contradicts another criterion | Step 4 cross-checks each changed criterion against criteria sharing a Glossary term |

## Low issues (open, for owner review)

| # | Source | Where | Problem → proposed fix |
|---|---|---|---|
| L1 | f1 I3 | `skills/spec-analyze/SKILL.md` | Apply can push a requirement over 7 criteria → split or supersede, log it |
| L2 | f1 I4 | `agents/spec-analyst.md` | A and B both reserve new numbers → number only A; B reuses A's id |
| L3 | f1 I5 | `agents/spec-analyst.md` | Option B with 2 SHALL (covered by M3 once in force) |
| L4 | f1 I6 | `agents/spec-task-runner.md` | Haiku cites wrong line numbers → cite from `git diff -U0` / `grep -n` |
| L5 | b1 I1 | `shared/gate.md` | Count line wrong for bugfix.md and bugfix design |
| L6 | b1 I2 | `shared/artifacts/bugfix-design.md` | Root-cause `file:line` not checked → `grep -n` before gate |
| L7 | b1 I3 | `shared/artifacts/bugfix-design.md` | API-level criterion forced into a property → allow example-only |
| L8 | a1 I3 | `skills/spec-analyze/SKILL.md` | Owner answers add interfaces that drive growth (+92 %) |
| L9 | a1 I4 | `skills/spec-analyze/SKILL.md` | Deferred proposals keep criterion numbers that later clash |
| L10 | a1 I5 | `shared/state.md` | zsh variable warning easy to miss → one copy-paste command form |

Plus open lows from 0.3.2: P9–P13 ([v0.3.2](../v0.3.2/README.md)).

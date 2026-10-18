# sdd v0.3.4: real plugin eval (f1, b1, a1)

Date: 2026-10-18 · Opus 5.5 medium · Reused the 0.3.3 sessions on folders reset to git baseline (app blocked new starts). Agents loaded the live 0.3.4 text (probe confirmed). Limit: each orchestrator remembers its 0.3.3 run.

| Run | Result | Tests (verified) | 0.3.4 checks |
|---|---|---|---|
| f1-discounts | PASS, 5/5 commands | 16 pass | M1 9/9 prompts held criterion text |
| b1-oversell | PASS | 14 pass | M1 5/5 |
| a1-giftcards | PASS | 16 pass | M2 4/4 owner answers placed right; M4 cross-check ran |

All: `check-tasks` PASS, all phases `approved`.

## Fixed and confirmed

M1 (criterion text in runner prompt), M2 (owner answer placement), M4 (cross-check of changed criteria: ran, found clashes F10, F11, F14, F15).

## Medium issues still open

| # | Where | Problem → proposed fix |
|---|---|---|
| Q1 | `skills/spec-analyze/SKILL.md:17`, `agents/spec-analyst.md:56` | `CHECK` is a self-report: 5 of 16 a1 findings and 2 f1 findings said pass but failed when counted → orchestrator recounts per option and ignores `CHECK` on mismatch; analyst lists assertions in `CHECK` |
| Q2 | same | `CHECK` target fails every correct `NEEDS_OWNER` finding (`shall=0`) → separate target `gaps=1 owner=sole` |
| Q3 | `skills/spec-analyze/SKILL.md:19` | Cross-check by shared term misses check-order clashes between rejection rules (a1 F16–F20) → list rejection criteria that can match the same input; their order must be stated |

## Low issues (open, for owner review)

Merged list: [../OPEN-ISSUES.md](../OPEN-ISSUES.md).

f1 I3–I6, b1 I1–I4, a1 I4–I5 (see each `eval/report.md`), plus L1–L10 from [v0.3.3](../v0.3.3/README.md).

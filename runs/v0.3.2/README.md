# sdd v0.3.2: real plugin eval (f1, b1, a1)

Date: 2026-10-18 · Opus 5.5 medium orchestrator · Script outside `CLAUDE.md` (N4 fixed).

| Run | Result | Tests (verified) | Note |
|---|---|---|---|
| f1-discounts | PARTIAL: commands 1–2 of 5 (usage limit) | 22 pass | growth 18 → 28 (+56 %), split advice fired |
| b1-oversell | PASS | 14 pass | pins red → fix → green; hand-back reports read per N1 |
| a1-giftcards | PASS | 23 pass | growth 12 → 27 (+125 %); analyst option rules broken 6×, repaired by step 3 |

All three: `check-tasks` PASS, all phases `approved`. N1 (hand-back), N3 (verify resolve), N4 (script leak) confirmed fixed.

## Open issues (next: 0.3.3)

| # | Sev | Where | Problem → fix |
|---|---|---|---|
| P1 | med | `agents/spec-task-runner.md:14` | Runner may edit its own red property test before the user picks (f1 I1) → on red property: report counterexample, stop, no test edit |
| P2 | med | `skills/spec-run/SKILL.md:24` | "Fix implementation" flow undefined (f1 I2) → re-dispatch owning code leaf with counterexample, same tier, then re-run test leaf |
| P3 | med | `skills/spec-run/SKILL.md:24` | `Expect: red` pin `done` with counterexample triggers the fix question (b1 I4) → skip step 6 for expected-red pins |
| P4 | med | `shared/scripts/spec.py` `criteria()` | Bugfix Current items `1.n` count as criteria to cite (b1 I3) → exclude `1.n` from coverage, or document |
| P5 | med | `agents/spec-analyst.md` | Option rules still broken 6× (a1 I1, f1 I3) → pre-output checklist |
| P6 | med | `agents/spec-analyst.md:30` | New criterion numbers clash across findings (a1 I2) → number in order across the round |
| P7 | med | `skills/spec-analyze/SKILL.md` | Decided findings re-raised in FOCUSED rounds (a1 I4) → pass decided ids + chosen options |
| P8 | med | `skills/spec-analyze/SKILL.md:24` | VERIFY-resolved edits never verified (a1 I3) → one more VERIFY on changed ids only, then park |
| P9 | low | `skills/spec-analyze/SKILL.md` | Growth metric counts one-assertion splits; >50 % fires on most money specs (a1 I6); split advice has no gate option (f1 I4) |
| P10 | low | `skills/spec-analyze/SKILL.md:21` | NEEDS_OWNER options undefined; answers add interfaces (a1 I5) → `Answer | Defer`, prefer Defer |
| P11 | low | `shared/gate.md:5` | Count line wrong for bugfix.md and bugfix design (b1 I1, I2) |
| P12 | low | `skills/spec-run/SKILL.md:23` | Checkpoint below only skipped `*` leaves: state that it runs and ticks (b1 I5) |
| P13 | low | runner/analyst | Verify should exercise each cited criterion (a1 I7) |

P1–P8 (medium) fixed in 0.3.3. P9–P13 (low) stay open for owner review.

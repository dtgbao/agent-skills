# sdd: open issues

As of round r4 (2026-10-19), after the rewrite. Sources: rounds v2, v3 and r4 in [README.md](README.md).

## Closed by the rewrite

The issues of rounds 0.4.x–0.5.x (Q4–Q12, L30–L54, I1–I8) are closed. They refer to files that the rewrite removed: `spec-analyze`, `agents/spec-analyst.md`, `agents/spec-task-runner.md`, `shared/gate.md`, `shared/artifacts/`, `shared/workflows/`. The old list is in git history. The main ones now have a script check:

| Old issue | Now |
|---|---|
| A red on an import, name or type error | `spec.py tdd run` asks for a stub and records no red |
| A runner writes the next test before green | `tdd run` refuses while a test for a later case exists |
| A test that passed at once with no proof | `tdd run` tries mutants on a temp copy; the case is done only when one kills the test |
| A signature change breaks the tests of earlier leaves (I1) | One runner owns a lane and runs its regression tests at the end of each slice |
| Sync unticked the wrong leaves | A case whose text or criterion changed reopens itself, and must change its test |

## Fixed in rounds v2–r4

| Issue | Fix | Confirmed |
|---|---|---|
| Sync deadlock: a stale test of a reopened case blocked green | The green check skips the tests of open cases | v3, r4 |
| The writer made 40 cases for 17 criteria | One case for each criterion; more values as a parametrized test | v3 (24 cases), r4 |
| The writer changed the requirements during the design | `approve design` refuses if the requirements changed after gate 1 | v3 (the guard fired) |
| One failed mutant search took 39 s | Limit: 15 mutants or 15 s | r4 |
| A criterion kept an old value after a hand edit (v3 low) | `drift` prints `OLD VALUE … criterion` and `… Design/Plan` lines | not run in an eval yet |

## Medium

| # | Problem | Proposed fix |
|---|---|---|
| M1 | sdd is 2–4× slower than strict /tdd. Costs: the spec phase (1–2 min), at least 2 runner calls for each case with a test run each, one subagent start for each lane | Measure the effect of `--inline` for 1-lane specs; start the next case's test in the same call as the green run |
| M2 | The bugfix flow (`## Bug`, `keep` cases) has no eval since the rewrite | Port `real/b1-oversell.md` to the new plugin, with a hidden suite |
| M3 | `--inline`, the counterexample question, and the retry tier path have no eval | Add a script that forces each one, for example a property with a planted wrong oracle |

## Low

| # | Problem | Proposed fix |
|---|---|---|
| L1 | f3 did not show an advantage for the gates: the tdd skill also asked the open questions | An eval where the open values are less obvious (a conflict between two rules) |
| L2 | `real/a1-giftcards.md`, `harness.md` scenarios 01–06 and `kiro/` use removed files | Remove them, or port a1 as a gate-1 test of open questions |
| L3 | The automatic mutants and the `Test:` target forms are tested only with pytest | An eval on a vitest or jest project |
| L4 | `drift` OLD VALUE lines also match unrelated numbers (for example `== 90` in another test) | Show the hits only for the lanes and criteria of the changed ids; mark them as hints |
| L5 | A reopened property case passes at once and needs a mutant; this costs time after each sync | Accept a changed property test that passes, when its bounds changed with the criterion |
| L6 | Typed-command expansion of the new skills is not verified (the evals load skills by hand) | Type `/sdd:spec-new` one time in a real session |

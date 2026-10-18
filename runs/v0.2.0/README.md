# sdd v0.2.0 rerun

Scenarios 03 and 06 (Sonnet), same briefs as v0.1.0. Method: [harness](../../../plugins/sdd/evals/harness.md).

| # | Result v0.1.0 → v0.2.0 | Old issues | New issues | Report |
|---|---|---|---|---|
| 03 Bugfix | PARTIAL → **PASS** | 9 fixed, 2 changed, 0 open | 6 (1 med fixed after run) | [report](03-bugfix-sonnet/report.md) |
| 06 Lifecycle | PARTIAL → PARTIAL | 11 fixed (2 with residual), 0 open | 6 (1 high, 1 med) | [report](06-lifecycle-sonnet/report.md) |

Key evidence:
- 03: pins ran without `--optional`. Exploration red (3 fail) → fix → 11 green. No `[-]` left.
- 06: hand edit 50 → 40 gave `DRIFT requirements`, `CHANGED 1.3, 2.3`, design + tasks `stale`. Sync unticked leaf 1.1. Run 2 set `MAX_LEN = 40`. `len(slugify('a'*45))` = 40. Final checkpoint red: test leaf 3.1 kept `"a"*49` because sync did not untick it.

## Fixed after the rerun (not re-run yet)

| Issue | Fix |
|---|---|
| 06v2-1, 03-13: tick marks gave false `DRIFT tasks` | `spec.py` hashes `tasks.md` with checkbox marks normalized |
| 03-12: approve on failing `tasks.md` | `spec.py approve tasks` refuses while `check-tasks` fails; gate runs the check first |
| 06v2-2, 06v2-3: stale ticked test leaf | `drift` prints `AFFECTS <id> -> <leaves>`. Sync unticks those leaves, their groups, and later checkpoints |
| 03-14: `Do` / `Verify` unchecked | `check-tasks` checks both |
| 03-15, 03-16: checkpoint scope, fix-leaf rule | Defined in `spec-run` step 3 and 5 |
| 06v2-4: Quick Plan resume | drafts present → final question |
| 06v2-5, 06v2-6: red checkpoint, "ask user" phrase | Red names the owning leaf, offers untick. Phrase removed |

## Check run after the patches

[v0.2.0-check/06](../v0.2.0-check/06-lifecycle-sonnet/report.md): **PASS**. Ticks gave `NO DRIFT`. Hand edit gave `CHANGED 1.4`, `AFFECTS 1.4 -> 1.1 1.2`, `CHANGED 2.3`, `AFFECTS 2.3 -> 3.1 3.2`. Sync unticked those 4 leaves, groups 1 and 3, checkpoints 2 and 4. Run 2: 9 passed, `len(slugify('a'*45))` = 40, no `[-]`, all phases `approved`. 06v2-1, -3, -6 fixed; -2 changed; -4, -5 fixed in text, not exercised.

Fixed after the check run (script self-test only):
- 03-17: `bugfix.md` Done-when splits a two-outcome defect into two items; example added.
- 06v3-1: baseline keeps criterion text. `drift` prints `SUSPECT <id> -> <leaf> <file:line> (<value>)` for leaves outside `AFFECTS` whose files still hold a number gone from the criterion (n; n±1 when n ≥ 10). Self-test: 50 → 40 flagged `tests/test_unique.py:2 (49)`. `spec-sync` step 4 unticks confirmed hits.

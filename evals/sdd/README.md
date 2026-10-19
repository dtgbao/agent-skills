# sdd evals

Evaluation of the [`sdd` plugin](../../plugins/sdd/README.md). Raw runs (reports, generated specs, logs, patches) are on branch **`eval-runs`**; this folder holds the method, the summary, and the open issues.

## Verdict (v0.5.0)

Round 0.4.2 passed every scenario (real f1, b1, a1; simulated 07a–c). Round 0.4.3 (Sonnet) checked the Q4–Q10 fixes: f1 PASS, a1 PARTIAL, and the gaps it found are fixed. Round 0.5.0 (Sonnet) checked the new vertical-slice task phase: f1 PARTIAL. Tracer bullet, seams, slice shape and property placement held. 6 of 25 cycles had no red because the tracer slice wrote too much code; that fix and the sync cap fix are not verified yet. Open: **9 medium, 24 low** in [OPEN-ISSUES.md](OPEN-ISSUES.md).

## Results

Rounds carry working labels (0.1.0–0.5.0). The plugin was unpublished during the evals, so its manifest stays at 0.1.0.

| Version | Method | Runs | Result | Main change confirmed |
|---|---|---|---|---|
| 0.1.0 | simulated, Sonnet/Haiku | 6 scenarios | 6 PARTIAL, 71 issues | baseline; cross-file contract breaks |
| 0.2.0 | simulated, Sonnet | 03 bugfix, 06 lifecycle (+ check) | 03 PASS, 06 PASS on check | `spec.py` drift + tasks checker; 20 of 22 issues fixed |
| 0.3.0 | real plugin, Opus orchestrator | f1, b1, a1 | 3/3 PASS | real agents, Size → model routing (haiku/sonnet/opus) |
| 0.3.1 | real | f1, a1 | 2/2 PASS | analyze growth +115 % → +42 %, code context |
| 0.3.2 | real | f1, b1, a1 | 2 PASS, f1 cut at 2/5 (usage limit) | hand-back reports, verify resolve, script kept out of `CLAUDE.md` |
| 0.3.3 | real | f1, b1, a1 | 3/3 PASS | red-property stop, fix flow, bugfix coverage |
| 0.3.4 | real (reused sessions) | f1, b1, a1 | 3/3 PASS | criterion text in runner prompt, owner-answer placement, cross-check |
| 0.4.0 | simulated, Sonnet | 07a vague, 07b clear, 07c defect | 3/3 PASS, 1 med + 7 low | `spec-brainstorm`: vague → confirmed playback, clear → one-line brief, defect → skip; no file written |
| 0.4.1 | simulated, Sonnet (fresh sessions) | 07a, 07b, 07c | 3/3 PASS, 6 new low | all 8 0.4.0 fixes held: defect exit, code facts in playback, Facts step reads code first |
| 0.4.2 | real (Opus) + simulated (Sonnet), fresh sessions | f1, b1, a1, 07a, 07b, 07c | 6/6 PASS, 7 med + 20 low new | 25 fixes: `CHECK` recount, check-order clashes, past-7 split, growth `+new/+split`, root-cause grep, brainstorm surface |
| 0.4.3 | real, Sonnet orchestrator | a1, f1 | f1 PASS, a1 PARTIAL | `CHECK` names the gap, owner keeps medium, Close step asks, literal oracles; gaps in runner rule and Close loop → fixed |
| 0.5.0 | real, Sonnet orchestrator | f1 (vertical slices) | PARTIAL | slice shape, tracer bullet, seams at the gate, properties in slices; 6/25 cycles no red (tracer overbuilt) → fixed |

Analyst recall on the seeded spec: 7/7 planted defects in round 1 (Haiku in 0.1.0, Sonnet in 0.3.x). Sonnet: same recall with fewer false positives.

## Layout

| Path | Role |
|---|---|
| [harness.md](harness.md), [briefs.md](briefs.md), [fixtures/](fixtures) | Simulated eval: skill text run as a slash command with a scripted user (cheap, any model). Scenario 07 tests `spec-brainstorm` (vague, clear, defect inputs) |
| [real/](real/README.md) | Real-plugin eval: mock shop project, eval rules, scripts, seeded spec (install, agents, routing) |
| [OPEN-ISSUES.md](OPEN-ISSUES.md) | Merged open issues |
| [kiro/](kiro/COMPARISON.md) | Kiro vs sdd artifact comparison + `measure.py` |
| `runs/` | Working dir for new runs (gitignored) |

## Run a new round

1. Real eval: follow [real/README.md](real/README.md); copy results to `runs/v<version>/`. Simulated: [harness.md](harness.md).
2. Add one row to Results; update [OPEN-ISSUES.md](OPEN-ISSUES.md).
3. Archive the run:

```bash
git worktree add ../eval-runs eval-runs
```

```bash
cp -R evals/sdd/runs/v<version> ../eval-runs/runs/ && git -C ../eval-runs add -A && git -C ../eval-runs commit -m "runs v<version>"
```

## Known limits

- Sessions started by the app get the first prompt as plain text, so skills ran by manual load. Verify `$ARGUMENTS` / `${CLAUDE_PLUGIN_ROOT}` expansion once by typing a command.
- 0.3.4 reused the 0.3.3 sessions (the app blocked new starts), so orchestrators remembered the earlier run.

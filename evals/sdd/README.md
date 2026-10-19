# sdd evals

Evaluation of the [`sdd` plugin](../../plugins/sdd/README.md). Raw runs (reports, generated specs, logs, patches) are on branch **`eval-runs`**. This folder holds the method, the summary and the open issues.

## Verdict (rewrite, round r4)

The plugin was rewritten after round 0.5.x: one `spec.md`, a thin main session, a `spec-writer` subagent, one `lane-runner` subagent for each lane, and a TDD loop that `spec.py` drives and checks.

In round r4, sdd and strict /tdd (Sonnet medium) both pass every hidden acceptance test on three features. sdd uses **1.1–1.55× the tokens** of strict /tdd (the target was below 2×). It is **2–4× slower**. Only sdd gives proof that each test was red before its code: the /tdd runs skip red runs, also when the prompt asks for one test at a time. Sonnet low also builds f1 correctly with the full process (round v3). Open: **3 medium, 6 low** in [OPEN-ISSUES.md](OPEN-ISSUES.md).

## Results: rewrite

All runs use Sonnet. Context tokens = the sum of all model calls, subagents included. "Acceptance" = a hidden suite in [`real/acceptance/`](real/acceptance) that the builder never sees.

| Round | Feature | Run | Acceptance | Time | Calls | Context tokens | Change confirmed |
|---|---|---|---|---|---|---|---|
| before | f1 (old text) | old plugin, high | – | 16.0 min | 140 | 8.6M | baseline: the orchestrator used 89% of the tokens; one subagent for each leaf |
| before | f1 (old text) | /tdd horizontal, high | – | 2.8 min | 25 | 2.0M | |
| v2 | f1 | sdd, medium/medium | 27/27 | 13.8 min | 152 | 5.6M | thin main session (24 calls); found a sync deadlock, 40 cases for 17 criteria |
| v2 | f1 | /tdd horizontal, medium / low | 27/27, 27/27 | 0.9 / 0.9 min | 7 / 8 | 0.5M / 0.6M | wrote all tests first, then all code |
| v3 | f1 | sdd, medium | 27/27 | 11.0 min | 95 | 3.2M | 2 calls for each cycle, automatic mutants, fewer cases, deadlock fixed |
| v3 | f1 | sdd, low (all Sonnet low) | 27/27 | 10.9 min | 90 | 2.8M | a low-effort model follows the full process |
| v3 | f1 | strict /tdd, medium / low | 27/27, 27/27 | 2.6 / 3.5 min | 24 / 32 | 1.9M / 2.6M | told to do one test at a time; the medium run ran tests only 2 times |
| r4 | f1 | sdd, medium | 27/27 | 9.9 min | 95 | 2.95M | speed fixes: one writer call for answers + design, 15 s mutant cap, regression at slice end |
| r4 | f2 | sdd, medium | 19/19 | 3.5 min | 62 | 1.5M | 3 lanes; shipping and tax ran in parallel, then the API lane |
| r4 | f2 | strict /tdd, medium | 19/19 | 1.7 min | 18 | 1.4M | |
| r4 | f3 | sdd, medium | 12/12 | 4.1 min | 46 | 1.4M | gate 1 asked 5 questions with recommended answers; the answers became criteria |
| r4 | f3 | strict /tdd, medium | 12/12 | 1.0 min | 13 | 0.97M | asked 1 combined question; 7 of 9 tests were never red |

Features: f1 discount codes, then a change of the percent range to 1–50 through a hand edit and `spec-sync`. f2 checkout quote over 3 modules. f3 bulk pricing with open values; the answers are in [`real/f3-answers.md`](real/f3-answers.md), and a run may read that file only when it asks a question.

## Results: old plugin (0.1.0–0.5.0)

Rounds carry working labels. The plugin was not published, so its manifest stays at 0.1.0. These rounds tested files that the rewrite removed (`spec-analyze`, `spec-analyst`, `tasks.md`, the leaf runner).

| Version | Method | Runs | Result | Main change confirmed |
|---|---|---|---|---|
| 0.1.0 | simulated, Sonnet/Haiku | 6 scenarios | 6 PARTIAL, 71 issues | baseline; cross-file contract breaks |
| 0.2.0 | simulated, Sonnet | 03 bugfix, 06 lifecycle | PASS | `spec.py` drift + tasks checker |
| 0.3.x | real plugin, Opus | f1, b1, a1 | PASS | real agents, model routing, analyze growth, criterion text in runner prompts |
| 0.4.x | simulated + real | 07a–c, f1, b1, a1 | PASS | `spec-brainstorm`; 25 analyze and runner fixes |
| 0.5.x | real, Sonnet | f1 | PARTIAL | vertical slices, STE text; prose rules for red and one test at a time failed, which led to the rewrite |

## Layout

| Path | Role |
|---|---|
| [real/](real/README.md) | Real-plugin eval: mock shop, eval rules for sdd and for /tdd, feature texts, scripts, hidden acceptance suites |
| [OPEN-ISSUES.md](OPEN-ISSUES.md) | Open issues |
| [harness.md](harness.md), [briefs.md](briefs.md), [fixtures/](fixtures) | Simulated eval of the old plugin. Scenario 07 (`spec-brainstorm`) still applies; the others use removed files |
| [kiro/](kiro/COMPARISON.md) | Kiro vs old sdd artifact comparison + `measure.py` |
| `runs/` | Working dir for new runs (gitignored) |

## Run a new round

1. Follow [real/README.md](real/README.md). Run sdd and the /tdd baseline at the same model and effort.
2. Grade each project with `real/acceptance/run.sh <feature> <project dir>`. Take time, calls and tokens from the session transcripts.
3. Add rows to Results, and update [OPEN-ISSUES.md](OPEN-ISSUES.md).
4. Archive the run:

```bash
git worktree add ../eval-runs eval-runs
```

```bash
cp -R evals/sdd/runs/<round> ../eval-runs/runs/ && git -C ../eval-runs add -A && git -C ../eval-runs commit -m "runs <round>"
```

## Known limits

- The app starts eval sessions with plain text, so the skills ran by manual load. `$ARGUMENTS` and `${CLAUDE_PLUGIN_ROOT}` expansion in a typed command is not verified for the rewrite.
- One run for each cell. The time numbers vary between runs.
- The scripted user and the builder are the same model. For f3, a run could read the answers file early; the transcripts show that the r4 runs read it only after they asked.

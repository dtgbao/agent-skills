# sdd eval

Evaluation of `plugins/sdd`. The v0.1.0 run (2026-10-17) sits at this level; later runs go to `v<version>/`. Read [FINDINGS.md](FINDINGS.md) first.

| Path | Content |
|---|---|
| [OPEN-ISSUES.md](OPEN-ISSUES.md) | **All open issues as of 0.3.4: 3 medium, 16 low** |
| [v0.3.4/README.md](v0.3.4/README.md) | 0.3.4: 3/3 PASS, 3 medium open (CHECK reliability, check order) |
| [v0.3.3/README.md](v0.3.3/README.md) | 0.3.3 real eval: 3/3 PASS, M1–M4 + lows L1–L10 |
| [v0.3.2/README.md](v0.3.2/README.md) | 0.3.2 real eval + open issues P1–P13 |
| [v0.3.1/README.md](v0.3.1/README.md) | Rerun of f1 and a1 on 0.3.1: loop converges, recall 7/7 |
| [v0.3.0/README.md](v0.3.0/README.md) | Real plugin test: installed plugin, real agents, Opus orchestrator, model routing |
| [v0.2.0/README.md](v0.2.0/README.md) | Rerun of 03 and 06 after the fixes |
| [FINDINGS.md](FINDINGS.md) | Verdict, model comparison, merged issues, proposed changes |
| [kiro/COMPARISON.md](kiro/COMPARISON.md) | Kiro specs vs sdd output: shape, metrics, parity changes |
| [briefs.md](../../plugins/sdd/evals/briefs.md) | Scenario prompts and scripted answers (in the plugin) |
| [harness.md](../../plugins/sdd/evals/harness.md) | Method: simulated skill, scripted user, report format (in the plugin) |
| [fixtures](../../plugins/sdd/evals/fixtures) | Clean fixture projects (in the plugin) |
| `NN-<scenario>/report.md` | Per-run report: step trace, Q&A, artifact checks, issues |
| `NN-<scenario>/workspace/` | Fixture after the run, with generated `docs/specs/<name>/` and code |

Rerun one scenario: copy the fixture to `v<version>/<id>/workspace/`, then give a session the harness and its brief.

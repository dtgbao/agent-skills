# Real-plugin eval

Runs the installed plugin with the real `sdd:spec-writer` and `sdd:lane-runner` agents, and compares it with a /tdd baseline on the same feature. A hidden acceptance suite grades both builds.

| File | Role |
|---|---|
| `mockshop/` | Base project (Python, oversell bug planted in `shop/inventory.py:16`) |
| `f1-feature.md`, `f2-feature.md`, `f3-feature.md` | Feature texts. f1 discount codes (with a later change), f2 checkout quote over 3 modules, f3 bulk pricing with open values |
| `f3-answers.md` | The owner's answers for f3. A run may read it only after it asks a question |
| `f1-discounts.md`, `f2-sdd.md`, `f3-sdd.md` | sdd Scripts |
| `f1-tdd.md` | /tdd baseline Script (the model may write all tests first) |
| `f1-tdd-strict.md`, `f2-tdd-strict.md`, `f3-tdd-strict.md` | /tdd baseline Scripts, one test at a time |
| `CLAUDE-sdd.md`, `CLAUDE-tdd.md` | Eval rules. Copy one into each project as `CLAUDE.md`. They hold no Script |
| `acceptance/` | Hidden suites `test_<f>_acceptance.py` and `run.sh`. Never copy them into a project |
| `b1-oversell.md`, `a1-giftcards.md`, `mockshop-seed/` | Old-plugin Scripts (bugfix, seeded analyze). Not ported to the rewrite yet |

Keep the Scripts outside the project: subagents load `CLAUDE.md`, so a Script there leaks later steps.

Setup for an sdd run (outside this repo):

```bash
cp -R mockshop ~/sdd-mock/f2-sdd && cp CLAUDE-sdd.md ~/sdd-mock/f2-sdd/CLAUDE.md
```

```bash
cd ~/sdd-mock/f2-sdd && claude plugin marketplace add <repo> --scope project && claude plugin install sdd@bao-plugins --scope project && git init -q && git add -A && git commit -qm baseline
```

For a /tdd run, copy `CLAUDE-tdd.md` and skip the plugin install. Start the session at the model and effort that you test. The first message names the Script file (and the RUN ARGS for sdd, for example `--model sonnet --effort low`).

The plugin cache is shared by all projects. Install the plugin for all runs before you start them, and do not install it again while a run is active.

Grade:

```bash
sh acceptance/run.sh f2 ~/sdd-mock/f2-sdd
```

a1 answer key (old plugin): K1 1.1 value 10–500 vs 2.3 balance up to 1000 · K2 2.2 "promptly" · K3 4.1 never expire vs 4.2 void after 12 months · K4 `Merchant_Portal`, staff, store credit not in Glossary · K5 balance < subtotal · K6 Payment_Provider failure · K7 concurrent redemption · Requirement 5 = clean control.

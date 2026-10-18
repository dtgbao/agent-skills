# Real-plugin eval

Runs the installed plugin with real `sdd:*` agents. Use it after each release. The simulated harness (`../harness.md`) is cheaper but cannot test install, agent types, frontmatter or model routing.

| File | Role |
|---|---|
| `mockshop/` | Base project (Python, oversell bug planted in `shop/inventory.py:16`) |
| `mockshop-seed/docs/` | Seeded gift-card spec for a1 (7 planted defects; key below) |
| `CLAUDE.md` | Eval rules. Copy into each project. Holds no Script |
| `f1-discounts.md`, `b1-oversell.md`, `a1-giftcards.md` | Scripts. Keep outside the project: subagents load `CLAUDE.md`, so a Script there leaks future steps |

Setup per run (outside this repo):

```bash
cp -R mockshop ~/sdd-mock/f1 && cp CLAUDE.md ~/sdd-mock/f1/
cd ~/sdd-mock/f1 && claude plugin marketplace add <repo> --scope project && claude plugin install sdd@bao-plugins --scope project && git init -q && git add -A && git commit -qm baseline
```

Start an Opus session in that folder. First message = the Script's first command; tell the session the Script file path. Read `eval/report.md` when it ends.

a1 answer key: K1 1.1 value 10–500 vs 2.3 balance up to 1000 · K2 2.2 "promptly" · K3 4.1 never expire vs 4.2 void after 12 months · K4 `Merchant_Portal`, staff, store credit not in Glossary · K5 balance < subtotal · K6 Payment_Provider failure · K7 concurrent redemption · Requirement 5 = clean control.

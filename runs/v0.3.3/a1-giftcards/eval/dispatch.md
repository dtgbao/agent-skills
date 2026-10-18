# Dispatch log

## D1 — analyst round 1
- subagent_type: `sdd:spec-analyst` · model passed: none (omitted per skill; frontmatter `sonnet`) · attempt 1 · STATUS: findings (9) · foreground
- Agent said: "Model: claude-sonnet-5-5. Tools: Read, Glob, Grep, SubagentHandback."
- Report arrived as a hand-back message, not in the tool result. Raw block: `eval/analyst-round-1.md`.

## D2 — analyst round 2
- subagent_type: `sdd:spec-analyst` · model passed: none (frontmatter `sonnet`) · attempt 1 · STATUS: findings (2: F10 high, F11 medium)
- Agent said: "Model: Sonnet 5.5 (claude-sonnet-5-5). Tools: Read, Glob, Grep, SubagentHandback."
- Hand-back message delivery. Raw block: `eval/analyst-round-2.md`. F10 is a defect that round-1 option F2 A introduced.

## D3 — analyst round 3
- subagent_type: `sdd:spec-analyst` · model passed: none (frontmatter `sonnet`) · attempt 1 · STATUS: findings (1: F12 high, NEEDS_OWNER)
- Agent said: "Model and tools: claude-sonnet-5-5 (Sonnet 5.5); Read, Glob, Grep, SubagentHandback."
- Hand-back message delivery. Raw block: `eval/analyst-round-3.md`. F12 option has extra text after the owner question (a draft criterion), outside the `NEEDS_OWNER: <question>` form.

## D4 — analyst VERIFY 1
- subagent_type: `sdd:spec-analyst` · model passed: none (frontmatter `sonnet`) · attempt 1 · STATUS: findings (4 medium: F13, F14, F15, F16)
- Agent said: "Running as Sonnet 5.5 (claude-sonnet-5-5) with the Read, Glob, Grep and SubagentHandback tools."
- Raw block: `eval/analyst-round-4-verify.md`. F14 option has two assertions (503 + error log) against the agent's own checklist.

## D5 — analyst VERIFY 2
- subagent_type: `sdd:spec-analyst` · model passed: none (frontmatter `sonnet`) · attempt 1 · STATUS: findings (1 medium: F17)
- Agent said: "Running as Sonnet 5.5 (claude-sonnet-5-5) with the tools Read, Glob, Grep and SubagentHandback."
- Raw block: `eval/analyst-round-5-verify.md`. Both F17 options hold two assertions (log + response).

## D6 — leaf 1.1 (wave 0)
- subagent_type: `sdd:spec-task-runner` · model passed: `haiku` (Size S) · attempt 1 · STATUS: done
- Agent said: "Model and tools: claude-haiku-5-5, with Read, Write, Edit, Bash, SubagentHandback." (Glob, Grep not named.)
```
TASK: 1.1
STATUS: done
FILES: shop/payments.py (new), shop/ledger.py (new)
TESTS: `python -c "from shop.payments import PaymentProvider, PaymentDeclined, PaymentError; from shop.ledger import Ledger, LedgerEntry, LedgerUnavailable"` -> exit 0; inline check: `Ledger(fail=True).append(e)` raises `LedgerUnavailable`, and a normal `append` stores the entry -> pass (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: Shapes follow design.md Payments and Ledger sections. In shop/ledger.py, `Ledger.append` raises `LedgerUnavailable` when `self.fail` is true, else appends. `Ledger` is a plain dataclass (not frozen), so `entries` and `fail` stay mutable. `LedgerEntry` is frozen. No test files written (leaf is Kind: code, no property tagging). Full pytest suite not run; the leaf's Verify command is the only check.
```

## D7 — leaf 1.2 (wave 1)
- subagent_type: `sdd:spec-task-runner` · model passed: `opus` (Size L) · attempt 1 · STATUS: done
- Agent said: "Run as: Opus 5.5 (claude-opus-5-5); tools Read, Write, Edit, Bash, SubagentHandback."
```
TASK: 1.2
STATUS: done
FILES: shop/gift_cards.py
TESTS: PYTHONPATH=. uv run --no-project python <scratchpad>/qc.py -> all quick checks OK; uv run --no-project --with pytest --with hypothesis python -m pytest -q -> 3 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: New file shop/gift_cards.py. It follows the design.md call tree. purchase takes int only (bool and float give 400). Ledger entries are written only when a value changes (redeem with no balance change and void of an already void card write no entry). On timeout, a refund failure is logged and the call still returns 504 (F17 option A). expire_unused skips a card when the ledger fails.
```
Extra prose after block: quick checks listed (purchase, redeem, 403, ledger-fail refund, 20 concurrent redeems, 364/365-day expiry). First quick-check run failed on its own script; fixed the script.

## D8 — leaf 3.1 (wave 2, parallel with D9)
- subagent_type: `sdd:spec-task-runner` · model passed: `sonnet` (Size M) · attempt 1 · STATUS: done
- Agent said: "Running as: Sonnet 5.5 (claude-sonnet-5-5); tools: Read, Write, Edit, Bash, SubagentHandback."
```
TASK: 3.1
STATUS: done
FILES: shop/api.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q -> 3 passed, 0 failed (expected: green). An ad-hoc script outside the repo also passed: POST /gift-cards returned 201 with a 16-char code, unknown-code redeem returned 404 unknown_card, and void without a staff actor returned 403 forbidden.
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: shop/api.py: new import on line 2. New /gift-cards block sits just before the `no route` fallback. The service is built with ctx.setdefault. GiftCardError maps to {status, body:{error}}. The cart routes are unchanged. Spec gap: purchase and redeem need a str actor_id, but the leaf says to pass ctx.get("actor"). I pass actor["id"], or "anonymous" when the actor is missing, and I pass the raw actor dict to void. Redeem with an unknown cart_id returns 404 {"error":"no cart"}, which the leaf does not specify.
```

## D9 — leaf 5.1 (wave 2, parallel with D8)
- subagent_type: `sdd:spec-task-runner` · model passed: `sonnet` (Size M) · attempt 1 · STATUS: done
- Agent said: "Running as: claude-sonnet-5-5 (Sonnet 5.5), tools: Read, Write, Edit, Bash, SubagentHandback."
```
TASK: 5.1
STATUS: done
FILES: tests/test_gift_cards_props.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_gift_cards_props.py -> 5 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: New file, one test per Properties 4, 5, 7, 8 and 9, each with a `Feature: gift-cards, Property N: <title>` tag comment. Each test uses 100 or more examples. P5 uses `max_examples=100` with real threads and a Barrier. P9 adds `@example` cases at the 365-day boundary (365 days and 365 days minus 1 second). P8 captures the `shop.gift_cards` log with a handler to check the ERROR record that holds `charge_ref`.
```

## D10 — leaf 5.2 (wave 3)
- subagent_type: `sdd:spec-task-runner` · model passed: `sonnet` (Size M) · attempt 1 · STATUS: done
- Agent said: "Running as: claude-sonnet-5-5 (Sonnet 5.5), with Read, Write, Edit, Bash and SubagentHandback."
```
TASK: 5.2
STATUS: done
FILES: tests/test_gift_cards_api.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_gift_cards_api.py -> 5 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: New file (untracked, so no git diff). It has Hypothesis tests for Properties 1, 2, 3 and 6, each with a `Feature: gift-cards, Property N: <title>` tag comment and max_examples=100. It also has the 100-redemption example test (under 2 s) for 2.2. All calls go through `handle` with fakes in `ctx`, and the redeem tests use a stub cart.
```

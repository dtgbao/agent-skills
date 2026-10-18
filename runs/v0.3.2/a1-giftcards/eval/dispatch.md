# Dispatch log

## D1 — spec-analyze round 1 (FULL)
- subagent_type: `sdd:spec-analyst` · model passed: none (omitted per skill; frontmatter `sonnet`) · attempt 1 · STATUS: findings (F1–F9)
- Agent self-report: "Model: Sonnet 5.5 (claude-sonnet-5-5)." Report came as a SubagentHandback message, not as the Agent result.
- Raw report: `eval/analyst-round-1.md`

## D2 — spec-analyze round 2 (FOCUSED)
- subagent_type: `sdd:spec-analyst` · model passed: none (frontmatter `sonnet`) · attempt 1 · STATUS: findings (F10–F11, both medium)
- Agent self-report: "Model: Sonnet 5.5 (claude-sonnet-5-5)". Hand-back message delivery.
- Raw report: `eval/analyst-round-2.md`

## D3 — spec-analyze round 3 (FOCUSED)
- subagent_type: `sdd:spec-analyst` · model passed: none (frontmatter `sonnet`) · attempt 1 · STATUS: findings (F12–F13, medium)
- Agent self-report: "Model: Sonnet 5.5 (claude-sonnet-5-5)". Raw: `eval/analyst-round-3.md`. Both findings propose id 3.6 (id clash; orchestrator renumbered F13 → 3.7).

## D4 — spec-analyze VERIFY
- subagent_type: `sdd:spec-analyst` · model passed: none (frontmatter `sonnet`) · attempt 1 · STATUS: findings (F14–F16 medium, F17 low)
- Agent self-report: "Model: Sonnet 5.5 (claude-sonnet-5-5)". Raw: `eval/analyst-round-4-verify.md`. F16 again mixes concrete A with NEEDS_OWNER B.

## D5 — spec-run leaf 1.1 (wave 0)
- subagent_type: `sdd:spec-task-runner` · model passed: `haiku` (Size S) · attempt 1 · STATUS: done
```
TASK: 1.1
STATUS: done
FILES: shop/payments.py (new)
TESTS: uv run --no-project --with pytest --with hypothesis python -c "<leaf Verify command>" -> 1 pass, 0 fail (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: shop/payments.py:1-32 adds PaymentError, RefundError, PaymentProvider Protocol, FakePaymentProvider (charge ids "ch_<n>", flags raise PaymentError/RefundError). Extra check: fail_charge/fail_refund raise as expected. No test file added (leaf Kind is code). Not committed.
Model: claude-haiku-5-5 (Haiku 5.5)
```

## D6 — spec-run leaf 1.2 (wave 0, same message as D5)
- subagent_type: `sdd:spec-task-runner` · model passed: `haiku` (Size S) · attempt 1 · STATUS: done
```
TASK: 1.2
STATUS: done
FILES: shop/ledger.py (new)
TESTS: uv run --no-project --with pytest --with hypothesis python -c "from shop.ledger import ListLedger, FailingLedger, LedgerError; ListLedger().append(1)" -> exit 0 (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: shop/ledger.py:1-29 adds frozen LedgerEntry, LedgerError, Ledger Protocol, ListLedger(list) with append, FailingLedger whose append raises LedgerError. Extra check: FailingLedger().append raises LedgerError, and LedgerEntry assignment raises FrozenInstanceError. Untracked shop/payments.py is not mine and was not touched.
Model: claude-haiku-5-5 (Haiku 5.5)
```

## D7 — spec-run leaf 1.3 (wave 1)
- subagent_type: `sdd:spec-task-runner` · model passed: `opus` (Size L) · attempt 1 · STATUS: done
```
TASK: 1.3
STATUS: done
FILES: /Users/baodang/Documents/code/sdd-mock/a1-giftcards-v032/shop/giftcards.py
TESTS: uv run --no-project --with pytest --with hypothesis python -c "...g.buy(1000,'u'); assert g.redeem(c,400,'u')==600" -> 1 pass, 0 fail, exit 0 (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: New file (untracked, so no git diff lines). It has buy/redeem/void with the design check order, and the Ledger write happens before the state change. buy refunds when the Ledger write fails and raises 503 refund_failed when the refund also fails. Codes are 16 chars from secrets.choice and a new code is made on collision. _now() makes clock() output UTC; a naive datetime is taken as UTC. No property tests: this leaf is code-only.
Model: Opus 5.5 (claude-opus-5-5)
```

## D8 — spec-run leaf 3.1 (wave 2)
- subagent_type: `sdd:spec-task-runner` · model passed: `sonnet` (Size M) · attempt 1 · STATUS: done
```
TASK: 3.1
STATUS: done
FILES: shop/api.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_cart.py -> 3 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: shop/api.py:2 import GiftCardError; routes added at :13-24 (POST /gift-cards, POST /gift-cards/{code}/void) and :41-46 (POST /carts/{id}/gift-card); existing cart routes unchanged. Redeem on an unknown cart returns 404 "no cart" before the gift-card path runs. Missing body keys (value_cents, code) raise KeyError and are not handled, because the spec does not say to.
Model: claude-sonnet-5-5 (Sonnet 5.5)
```

## D9 — spec-run leaf 5.1* (wave 2, same message as D8)
- subagent_type: `sdd:spec-task-runner` · model passed: `sonnet` (Size M) · attempt 1 · STATUS: done
```
TASK: 5.1
STATUS: done
FILES: tests/test_giftcards_props.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_giftcards_props.py -> 12 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: New file tests/test_giftcards_props.py; 12 Hypothesis tests, each with max_examples=100 (line 12) and a "Feature: gift-cards, Property N" tag comment. Property 11 asserts one Ledger entry per change, plus the zero-subtotal redeem edge case.
Model: Sonnet 5.5 (claude-sonnet-5-5)
```

## D10 — spec-run leaf 5.2 (wave 3)
- subagent_type: `sdd:spec-task-runner` · model passed: `sonnet` (Size M) · attempt 1 · STATUS: done
```
TASK: 5.2
STATUS: done
FILES: tests/test_giftcards_api.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_giftcards_api.py -> 8 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: New file tests/test_giftcards_api.py:1-85. It has 7 example tests through handle plus a 1000-redeem latency test (p95 < 2s). Redeem uses an empty cart (subtotal 0), so the balance stays at the purchased value.
Model: Sonnet 5.5 (claude-sonnet-5-5)
```


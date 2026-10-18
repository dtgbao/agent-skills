# Dispatch log

## D1 — analyze round 1
- subagent_type: `sdd:spec-analyst` · model passed: none (skill names no model; frontmatter `sonnet` applies) · attempt 1 · STATUS: OK (8 findings)
- Agent said: "Model: claude-sonnet-5-5. Tools: Read, Glob, Grep, SubagentHandback."
- Raw report: `eval/analyst-round-1.md`
- Note: F6 options A and B close two different gaps (not exclusive). F7 has a single non-NEEDS_OWNER option. Both break `agents/spec-analyst.md` Options rules.

## D2 — analyze round 2
- subagent_type: `sdd:spec-analyst` · model passed: none (frontmatter `sonnet`) · attempt 1 · STATUS: OK (2 findings)
- Agent said: "Running as Sonnet 5.5 (claude-sonnet-5-5)."
- Raw report: `eval/analyst-round-2.md`
- Note: F10 option B has two `SHALL` (breaks one-SHALL rule). F9 A ≈ 41 words.

## D3 — analyze round 3
- subagent_type: `sdd:spec-analyst` · model passed: none (frontmatter `sonnet`) · attempt 1 · STATUS: OK (NO FINDINGS)
- Agent said: "Model: Sonnet 5.5 (claude-sonnet-5-5)."
- Raw report: `eval/analyst-round-3.md`

## D4 — analyze VERIFY
- subagent_type: `sdd:spec-analyst` · model passed: none (frontmatter `sonnet`) · attempt 1 · STATUS: OK (3 findings: F11 medium, F12 medium, F13 low)
- Agent said: "Model: Sonnet 5.5 (claude-sonnet-5-5)."
- Raw report: `eval/analyst-round-verify.md`
- Not applied (skill: verify findings → Open Questions).

## D5 — leaf 1.1 (wave 0)
- subagent_type: `sdd:spec-task-runner` · Size S · model passed: `haiku` · attempt 1 · STATUS: done
- Agent said: "Haiku 5.5 (claude-haiku-5-5)"
```
TASK: 1.1
STATUS: done
FILES: shop/ledger.py (new), shop/payments.py (new)
TESTS: uv run --no-project --with pytest --with hypothesis python -c "from shop.ledger import Ledger, LedgerEntry, LedgerUnavailable; from shop.payments import FakePaymentProvider, PaymentFailed, RefundFailed" -> exit 0 (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: shop/ledger.py:L-classes LedgerEntry (frozen dataclass), LedgerUnavailable, Ledger(fail=False) with entries and append; shop/payments.py: PaymentFailed, RefundFailed, PaymentProvider Protocol, FakePaymentProvider(fail_charge, fail_refund) with charges and refunds. Full suite: 3 passed (tests/test_cart.py). No property tests in this leaf.
```

## D6 — leaf 1.2 (wave 1)
- subagent_type: `sdd:spec-task-runner` · Size L · model passed: `opus` · attempt 1 · STATUS: done
- Agent said: "Model: Opus 5.5 (claude-opus-5-5)."
```
TASK: 1.2
STATUS: done
FILES: shop/giftcards.py
TESTS: uv run --no-project --with pytest --with hypothesis python -c "from shop.giftcards import GiftCardStore; ... assert s.get(c.code).balance_cents==4000" -> 1 pass, 0 fail (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: New file. redeem at shop/giftcards.py:72-86 checks in this order: unknown, void, insufficient, ledger append, commit. void of a card that is already void returns the card and writes no ledger entry (design F12). get/create/redeem/void return copies made with dataclasses.replace. Timestamps come from now().astimezone(utc).isoformat() and end with "+00:00".
```

## D7 — leaf 1.3 (wave 2, parallel with D8)
- subagent_type: `sdd:spec-task-runner` · Size M · model passed: `sonnet` · attempt 1 · STATUS: done
- Agent said: "Model: Sonnet 5.5 (claude-sonnet-5-5)"
```
TASK: 1.3
STATUS: done
FILES: tests/test_giftcards.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_giftcards.py -> 3 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: tests/test_giftcards.py:11-100. P3, P4 and P6 each use max_examples=100 and a `Feature: gift-cards, Property N` tag comment. The first run of P6 failed because the test did not handle `CardVoid` after a void followed by a redeem. That was a test bug, not an implementation bug, and I fixed it by catching `CardVoid` (lines 83-85). `shop/api.py` was not touched.
```
- Note: runner hit a red property run and changed its own test without reporting a counterexample. correctness.md step 5 says the test stays unchanged until the user picks. The rule names only `/sdd:spec-run`, so it is not clear whether it binds a runner during authoring.

## D8 — leaf 3.1 (wave 2, parallel with D7)
- subagent_type: `sdd:spec-task-runner` · Size M · model passed: `sonnet` · attempt 1 · STATUS: done
- Agent said: "Model: Sonnet 5.5 (claude-sonnet-5-5)"
```
TASK: 3.1
STATUS: done
FILES: shop/api.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_cart.py -> 3 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: shop/api.py adds helpers _buy_gift_card, _void_gift_card and _redeem_gift_card. It also adds route dispatch ahead of the /carts/ block and a /gift-card branch inside it. A manual handle call to POST /gift-cards with value_cents=2000 returned 201 with a 16-char code. A staff void of that card returned 200 with status void.
```

## D9 — leaf 3.2 (wave 3)
- subagent_type: `sdd:spec-task-runner` · Size M · model passed: `sonnet` · attempt 1 · STATUS: done
- Agent said: "Model: Sonnet 5.5 (claude-sonnet-5-5)"
```
TASK: 3.2
STATUS: done
FILES: /Users/baodang/Documents/code/sdd-mock/a1-giftcards-v031/tests/test_giftcards_api.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_giftcards_api.py -> 5 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: tests/test_giftcards_api.py (new file) has P1, P2 and P5, each with a Feature tag comment and max_examples=100. It also has the 2.2 example (1000 redemptions in under 2 s) and the 4.1/4.2 example (injected clock +396 days; card stays active with its balance and can still be redeemed).
```


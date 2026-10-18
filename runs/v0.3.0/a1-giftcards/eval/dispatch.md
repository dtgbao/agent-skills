# Dispatches

## D1 · round 1 · FULL
- subagent_type: `sdd:spec-analyst` · model passed: `sonnet` · attempt 1 · foreground
- STATUS: findings F1–F13 (high 7, medium 3, low 3)
- Agent said: "Model: claude-sonnet-5-5 (Sonnet 5.5). Tools: Read, Glob, Grep, SubagentHandback."
- Raw report: `eval/analyst-round-1.md`

## D2 · round 2 · FULL
- subagent_type: `sdd:spec-analyst` · model passed: `sonnet` · attempt 1 · foreground
- STATUS: findings F14–F19 (high 1, medium 5, low 0)
- Agent said: "Running as Sonnet 5.5 (claude-sonnet-5-5). Tools: Read, Glob, Grep, SubagentHandback."
- Raw report: `eval/analyst-round-2.md`

## D3 · round 3 · FULL
- subagent_type: `sdd:spec-analyst` · model passed: `sonnet` · attempt 1 · foreground
- STATUS: findings F20–F23 (high 0, medium 3, low 1)
- Agent said: "Model: Sonnet 5.5 (claude-sonnet-5-5). Tools: Read, Glob, Grep, SubagentHandback."
- Raw report: `eval/analyst-round-3.md`

## D4 · verify · VERIFY
- subagent_type: `sdd:spec-analyst` · model passed: `sonnet` · attempt 1 · foreground
- STATUS: findings F24–F26 (medium 3). Not applied. Added to `## Open Questions` per skill step 5.
- Agent said: "Model: Sonnet 5.5 (claude-sonnet-5-5). Tools: Read, Glob, Grep, SubagentHandback."
- Raw report: `eval/analyst-round-verify.md`

## Wave 0 (spec-run)
| # | Leaf | Size | subagent_type | Model passed | Attempt | STATUS |
|---|---|---|---|---|---|---|
| D5 | 1.1 | M | sdd:spec-task-runner | sonnet | 1 | none (report = `placeholder`) → treated failed |
| D6 | 1.2 | S | sdd:spec-task-runner | haiku | 1 | done |
| D7 | 1.3 | S | sdd:spec-task-runner | haiku | 1 | done |
| D8 | 1.4 | S | sdd:spec-task-runner | haiku | 1 | done |

Raw reports:
```
D5: placeholder
```
```
TASK: 1.2
STATUS: done
FILES: shop/ledger.py (new)
TESTS: uv run --no-project python -c "<leaf Verify command>" -> 1 pass / 0 fail (expected: green)
COUNTEREXAMPLE: none
NOTES: Added LedgerUnavailable(Exception), frozen dataclass Entry(code, field, old, new, actor_id, at), and Ledger with entries, manual_refunds, append(). Verify printed OK, exit 0. Running as Haiku 5.5 (claude-haiku-5-5).
```
```
TASK: 1.3
STATUS: done
FILES: /Users/baodang/Documents/code/sdd-mock/a1-giftcards/shop/payments.py (new)
TESTS: uv run --no-project python -c "from shop.payments import ChargeResult, PaymentProvider; assert ChargeResult('timeout').charge_id is None" -> 1 pass / 0 fail (expected: green)
COUNTEREXAMPLE: none
NOTES: Contents copied from design.md "PaymentProvider (shop/payments.py)" section. Frozen ChargeResult dataclass and PaymentProvider Protocol with charge/refund/cancel. Run as model: claude-haiku-5-5 (Haiku 5.5).
```
```
TASK: 1.4
STATUS: done
FILES: shop/cart.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_cart.py -> 3 pass / 0 fail (expected: green). Extra check: Cart(Inventory({})).open is True -> True
COUNTEREXAMPLE: none
NOTES: Added `self.open = True` after `self.lines` in Cart.__init__. No other change. Model: claude-haiku-5-5 (Haiku 5.5).
```

| # | Leaf | Size | subagent_type | Model passed | Attempt | STATUS |
|---|---|---|---|---|---|---|
| D9 | 1.1 | M | sdd:spec-task-runner | opus (retry, tier up) | 2 | done |
```
TASK: 1.1
STATUS: done
FILES: /Users/baodang/Documents/code/sdd-mock/a1-giftcards/shop/giftcards.py (the previous attempt wrote it; this retry made no changes)
TESTS: uv run --no-project python -c "from shop.giftcards import GiftCardStore, GiftCard; ... assert s.lock(c) is s.lock(c)" -> 1/1 pass (expected: green)
COUNTEREXAMPLE: none
NOTES: I checked the file from the previous attempt against Do. It is complete. Extra checks pass: add() raises ValueError for -1 and 50001, 200 codes match [A-Z0-9]{16}, and the file has no time or expiry logic.
NOTES: add() returns the card, but design.md says it returns None. No caller depends on this.
NOTES: Model: Opus 5.5 (claude-opus-5-5).
```

## Wave 1
| # | Leaf | Size | subagent_type | Model passed | Attempt | STATUS |
|---|---|---|---|---|---|---|
| D10 | 1.5 | S | sdd:spec-task-runner | haiku | 1 | done |
```
TASK: 1.5
STATUS: done
FILES: tests/fakes.py (new)
TESTS: uv run --no-project python -c "<leaf Verify command>" -> 1 pass / 0 fail (expected: green)
COUNTEREXAMPLE: none
NOTES: Added FakePaymentProvider(result, refund_fails) with charges/refunds/cancels lists, FailingLedger(Ledger) raising LedgerUnavailable on append, and make_ctx(**over) with keys carts, inventory, giftcards, ledger, payments, staff_ids. Extra ad hoc checks passed (declined result, refund failure, FailingLedger, ctx keys). No pytest run; no test files written.
Model: claude-haiku-5-5 (Haiku 5.5).
```
Checkpoint 2: `pytest -q` → 3 passed. Green → [x].

## Wave 2
| # | Leaf | Size | subagent_type | Model passed | Attempt | STATUS |
|---|---|---|---|---|---|---|
| D11 | 3.1 | L | sdd:spec-task-runner | opus | 1 | done |
| D12 | 3.2 | L | sdd:spec-task-runner | opus | 1 | done |
| D13 | 3.3 | M | sdd:spec-task-runner | sonnet | 1 | done |
```
TASK: 3.1
STATUS: done
FILES: /Users/baodang/Documents/code/sdd-mock/a1-giftcards/shop/purchase.py
TESTS: uv run --no-project python -c "...buy({'value_dollars':25,'actor_id':'u1'}, c)... assert 201 and len(code)==16" -> 1 pass, 0 fail (expected: green)
COUNTEREXAMPLE: none
NOTES: Model: Opus 5.5 (claude-opus-5-5). buy() follows the design call tree. It stores only 201 responses under the idempotency key. Bool and float values give 422.
NOTES: More smoke checks pass: idempotent replay with one charge, 422 with no charge, timeout -> cancel + 402, ledger fail + refund fail -> 503 and one manual_refunds entry.
```
```
TASK: 3.2
STATUS: done
FILES: /Users/baodang/Documents/code/sdd-mock/a1-giftcards/shop/redeem.py
TESTS: Verify command (uv run --no-project python -c "... apply(...)['status']==200") -> 1 pass, 0 fail (expected: green)
COUNTEREXAMPLE: none
NOTES: apply() follows the design call tree: 422 -> 404 -> lock -> 409 -> ledger append (503 on LedgerUnavailable, no change) -> commit -> 200 {balance_cents, amount_due_cents}. Error body is {"error": <code>}.
NOTES: I also ran ad-hoc checks for overspend (500 balance, 1350 subtotal -> 0 balance, 850 due), unknown, short code, missing cart, void, and failing ledger (balance unchanged). All gave the expected result.
NOTES: Model: Opus 5.5 (claude-opus-5-5).
```
```
TASK: 3.3
STATUS: done
FILES: /Users/baodang/Documents/code/sdd-mock/a1-giftcards/shop/void.py
TESTS: uv run --no-project python -c "<Verify one-liner>" -> passed (prints ok) (expected: green)
COUNTEREXAMPLE: none
NOTES: Model: Sonnet 5.5 (claude-sonnet-5-5). void() returns {"status","body"}: 403 forbidden, 404 unknown_card, 409 card_void, 503 ledger_unavailable, 200 {code,status:"void"}. The ledger write comes before the status change, under the per-card lock. The error body key "error" matches the existing api.py style.
```
Checkpoint 4: pytest -q → 3 passed. Green → [x].

## Wave 3
| # | Leaf | Size | subagent_type | Model passed | Attempt | STATUS |
|---|---|---|---|---|---|---|
| D14 | 5.1 | M | sdd:spec-task-runner | sonnet | 1 | done |
| D15 | 5.2* | M | sdd:spec-task-runner | sonnet | 1 | done |
| D16 | 5.3* | L | sdd:spec-task-runner | opus | 1 | done |
| D17 | 5.4* | M | sdd:spec-task-runner | sonnet | 1 | done |
| D18 | 5.5* | M | sdd:spec-task-runner | sonnet | 1 | done |
```
TASK: 5.1
STATUS: done
FILES: /Users/baodang/Documents/code/sdd-mock/a1-giftcards/shop/api.py
TESTS: uv run --no-project python -c "...handle POST /gift-cards...assert status==201" -> pass (status 201, got a code) (expected: green)
COUNTEREXAMPLE: none
NOTES: Model: Sonnet 5.5 (claude-sonnet-5-5). Added imports and 3 routes before /carts. Void route takes the code from path segment 2. Only the 201 purchase path was run; the redeem and void routes were not exercised.
```
```
TASK: 5.2
STATUS: done
FILES: /Users/baodang/Documents/code/sdd-mock/a1-giftcards/tests/test_purchase.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_purchase.py -> 6 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none
NOTES: Model: Sonnet 5.5 (claude-sonnet-5-5). Properties 1, 2, 3, 4 and 10 are covered. Each uses 100 examples. Property 2 also has a missing-value example test. Float values such as 10.0 are rejected, as purshase.py requires type int.
```
```
TASK: 5.3
STATUS: done
FILES: /Users/baodang/Documents/code/sdd-mock/a1-giftcards/tests/test_redeem.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_redeem.py -> 5 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none
NOTES: Properties 5 (200 examples), 6 (100 examples, threads start together at a barrier, and the test checks that ledger old/new values form one chain), and 7 (200 examples) each have a tag comment. There are also example tests for 2.2 (p95 latency over 200 redemptions) and 4.1 (a card that no operation touches keeps its balance). The 4.1 test also calls void.void.
Model: Opus 5.5 (claude-opus-5-5).
```
```
TASK: 5.4
STATUS: done
FILES: /Users/baodang/Documents/code/sdd-mock/a1-giftcards/tests/test_void.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_void.py -> 2 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none
NOTES: Model: Sonnet 5.5 (claude-sonnet-5-5). Property 8 tests: staff void gives 200, status void, one ledger entry; non-staff, None or missing actor gives 403 forbidden with card and ledger unchanged.
```
```
TASK: 5.5
STATUS: done
FILES: /Users/baodang/Documents/code/sdd-mock/a1-giftcards/tests/test_ledger_audit.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_ledger_audit.py -> 2 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none
NOTES: Model: Sonnet 5.5 (claude-sonnet-5-5). Test 1: each successful change adds exactly one ledger entry with correct code, field, old, new, actor and UTC time; a failed op adds none and leaves the store unchanged. Test 2: with FailingLedger, every op returns 503 ledger_unavailable and the store and ledger stay unchanged. Each test runs 100 examples.
```
Checkpoint 6: pytest -q → 18 passed. Green → [x].
Note: `tests/test_void.py` has a docstring, not the `# Feature: gift-cards, Property 8: ...` tag comment (correctness.md step 4).

## Wave 4
| # | Leaf | Size | subagent_type | Model passed | Attempt | STATUS |
|---|---|---|---|---|---|---|
| D19 | 7.1* | M | sdd:spec-task-runner | sonnet | 1 | done |
```
TASK: 7.1
STATUS: done
FILES: /Users/baodang/Documents/code/sdd-mock/a1-giftcards/tests/test_api_giftcards.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_api_giftcards.py -> 3 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none
NOTES: Tests cover buy, partial redeem, redeem with amount due (1100), staff void, then redeem returns 409. Also cover non-staff void (403) and existing /carts routes. I ran as Sonnet 5.5 (claude-sonnet-5-5).
```
Checkpoint 8 (final): pytest -q → 21 passed. Green → [x]. `SPEC drift` → NO DRIFT. `check-tasks` → PASS.

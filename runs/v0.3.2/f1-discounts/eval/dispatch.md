# Dispatch log

## D1 — analyst round 1 (FULL)
- subagent_type: sdd:spec-analyst · model passed: omitted (frontmatter sonnet) · attempt 1 · STATUS: n/a (analyst) → 7 findings
- Agent said: "Running as Claude Sonnet 5.5 (claude-sonnet-5-5), with the Read, Glob, Grep and SubagentHandback tools."
- Report arrived as SubagentHandback message, not in the Agent result. Raw block: `eval/analyst-round-1.md`.

## D2 — analyst round 2 (FOCUSED)
- subagent_type: sdd:spec-analyst · model passed: omitted (frontmatter sonnet) · attempt 1 · STATUS: n/a → 2 findings (F8, F9, both medium)
- Agent said: "Running as claude-sonnet-5-5 (Sonnet 5.5) with Read, Glob, Grep, and SubagentHandback."
- Hand-back message again. Raw block: `eval/analyst-round-2.md`.

## D3 — analyst round 3 (FOCUSED)
- subagent_type: sdd:spec-analyst · model passed: omitted (frontmatter sonnet) · attempt 1 · STATUS: n/a → 1 finding (F10, high)
- Agent said: "Model: Sonnet 5.5 (claude-sonnet-5-5). Tools: Read, Glob, Grep, SubagentHandback."
- Raw block: `eval/analyst-round-3.md`. Note: option B repeats 2.7 text unchanged plus a rationale clause; not an exclusive alternative.

## D4 — analyst VERIFY (1.6, 1.7, 1.8, 2.6, 2.7, 2.8, 3.1, 3.2, 3.4, 4.6, 4.7, 4.8)
- subagent_type: sdd:spec-analyst · model passed: omitted (frontmatter sonnet) · attempt 1 · STATUS: n/a → NO FINDINGS
- Agent said: "Running as Sonnet 5.5 (claude-sonnet-5-5) with the Read, Glob, Grep and SubagentHandback tools."
- Raw block: `eval/analyst-round-verify.md`.

## D5 — leaf 1.1 (wave 0)
- subagent_type: sdd:spec-task-runner · Size M · model passed: sonnet · attempt 1 · STATUS: done
- Hand-back message, not in the Agent result.
```
TASK: 1.1
STATUS: done
FILES: /Users/baodang/Documents/code/sdd-mock/f1-discounts-v032/shop/discounts.py
TESTS: uv run --no-project --with pytest --with hypothesis python -c "from shop.discounts import CodeRegistry, discount_cents" -> exit 0 (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: Model: Sonnet 5.5 (claude-sonnet-5-5). New file shop/discounts.py (untracked, so no git diff). Expiry is checked with the regex `[0-9]{4}-[0-9]{2}-[0-9]{2}` and then date.fromisoformat. bool is rejected for value and min_subtotal_cents. get() returns None for an unhashable key. No property tests were in scope.
```

## D6 — leaf 1.2 (wave 1)
- subagent_type: sdd:spec-task-runner · Size M · model passed: sonnet · attempt 1 · STATUS: done (with COUNTEREXAMPLE)
```
TASK: 1.2
STATUS: done
FILES: /Users/baodang/Documents/code/sdd-mock/f1-discounts-v032/tests/test_discounts.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_discounts.py -> 7 pass / 0 fail (expected: green)
COUNTEREXAMPLE: First run was red on Property 2 (before my test fix). Shrunk input: first=('0','percent',1,0,'2000-01-01'), second call register('0','percent',0,0,'') raised InvalidCode (shop/discounts.py:47 value, :53 expiry) instead of DuplicateCode. Cause: the implementation validates fields before it checks for a duplicate. This matches the design pseudocode, where the duplicate check is last. The Property 2 text says "any fields", which does not match that order.
FOREIGN-FAIL: none
NOTES: Model: Sonnet 5.5 (claude-sonnet-5-5). I fixed only my test file. In tests/test_discounts.py:79-85 the second registration now uses a valid record with the same code, so Property 2 is weaker than its text. Spec issue for the caller: either reword Property 2 to "any valid fields" or move the duplicate check before field validation in register. Property 1 (:55) and Property 2 (:77) carry tag comments with max_examples=200. Example tests cover percent 0/1/90/91 and expiry 2026-02-30. I did not touch shop/discounts.py. git status also shows shop/cart.py modified, which another runner owns.
```

## D7 — leaf 3.1 (wave 1)
- subagent_type: sdd:spec-task-runner · Size S · model passed: haiku · attempt 1 · STATUS: done
```
TASK: 3.1
STATUS: done
FILES: shop/cart.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_cart.py -> 3 pass / 0 fail (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: Added `self.applied_code = None` (shop/cart.py:12), `discount_cents(today)` (shop/cart.py:28-29) and `total_cents(today)` (shop/cart.py:31-32). Module imported as `import shop.discounts as discounts` to avoid name clash with the method. `add`/`remove` untouched, so `applied_code` is never cleared. Smoke check: 2×TEA-01 with 10% code gives subtotal 900, discount 90, total 810. Model: claude-haiku-5-5 (Haiku 5.5).
```

## D8 — leaf 1.1 re-run (fix implementation after Property 2 counterexample)
- subagent_type: sdd:spec-task-runner · Size M · model passed: sonnet (not a failure retry, so no tier step) · attempt 2 · STATUS: done
```
TASK: 1.1
STATUS: done
FILES: shop/discounts.py
TESTS: uv run --no-project --with pytest --with hypothesis python -c "from shop.discounts import CodeRegistry, discount_cents" -> exit 0; full pytest -q -> 10 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none (earlier Property 2 counterexample first=('0','percent',1,0,'2000-01-01'), second=('0','percent',0,0,'') now raises DuplicateCode; the full suite, including the Property 2 test, passes)
FOREIGN-FAIL: none
NOTES: Model: Sonnet 5.5 (claude-sonnet-5-5). In CodeRegistry.register in shop/discounts.py, I moved the `if code in self._store: raise DuplicateCode` check to right after the Code_String check (about line 42). It used to sit just before the DiscountCode construction. Nothing else changed. git diff was empty because the file is untracked.
```

## D9 — leaf 1.2 re-run (restore Property 2 full text)
- subagent_type: sdd:spec-task-runner · Size M · model passed: sonnet · attempt 2 · STATUS: done
```
TASK: 1.2
STATUS: done
FILES: tests/test_discounts.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_discounts.py -> 7 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none on this run. I did not re-run the old implementation, so there was no red run this time. The earlier Property 2 counterexample is already with the caller.
FOREIGN-FAIL: none
NOTES: Model: Sonnet 5.5 (claude-sonnet-5-5). I restored Property 2 in tests/test_discounts.py (test_duplicate_rejected, lines 77-86). The first record is valid. The second registration uses the same Code_String and arbitrary kind, value, min and expiry (valid or not), and it must raise DuplicateCode. The test also asserts the stored record is unchanged. max_examples=200 and the tag comment are kept. The fixed implementation checks for duplicates at shop/discounts.py:42, before it validates the other fields.
```

## D10 — leaf 3.2 (wave 2)
- subagent_type: sdd:spec-task-runner · Size M · model passed: sonnet · attempt 1 · STATUS: done
```
TASK: 3.2
STATUS: done
FILES: /Users/baodang/Documents/code/sdd-mock/f1-discounts-v032/tests/test_cart_discount.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_cart_discount.py -> 9 pass / 0 fail (expected: green)
COUNTEREXAMPLE: none (the first run had 4 failures in my own test file: AttributeError, `st.assume` does not exist. I changed it to `hypothesis.assume`. These were not property failures.)
FOREIGN-FAIL: none
NOTES: Model: Sonnet 5.5 (claude-sonnet-5-5). The file has 9 tests with `@settings(max_examples=200)`. They cover Properties 3, 4 and 5, each with a tag comment. Each property is tested through `discount_cents` and through a `Cart` with `applied_code` set. Cart lines are set directly on the instance, which skips Inventory.
```

## D11 — leaf 5.1 (wave 2)
- subagent_type: sdd:spec-task-runner · Size M · model passed: sonnet · attempt 1 · STATUS: done
```
TASK: 5.1
STATUS: done
FILES: shop/api.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_cart.py -> 3 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: Model: Sonnet 5.5 (claude-sonnet-5-5). Edits in shop/api.py: imports and docstring at the top, POST/DELETE /discount branch before the /lines branch, GET widened, and a new `_totals` helper at the end. The manual `handle` call with a fake ctx returned 200 with discount_cents=90 and code A. A second code gave 409. GET returned the widened body. POST on a missing cart gave 404 "no cart". My manual DELETE call used the path "/carts/1" and got "no route", which is my test mistake. DELETE /carts/1/discount was not run by hand, and the existing tests don't cover it either.
```

## D12 — leaf 5.2 (wave 3)
- subagent_type: sdd:spec-task-runner · Size M · model passed: sonnet · attempt 1 · STATUS: done
```
TASK: 5.2
STATUS: done
FILES: tests/test_api_discount.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_api_discount.py -> 3 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: Model: Sonnet 5.5 (claude-sonnet-5-5). New file tests/test_api_discount.py holds Properties 6, 7 and 8 with tag comments and max_examples=200. Each example builds a fresh ctx. Property 6 uses a reference model for check order, a pre-applied code, a no-cart case, and a repeat apply.
```

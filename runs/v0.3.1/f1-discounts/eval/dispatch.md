# Dispatch log

## D1 — analyst round 1 (FULL)
- subagent_type: `sdd:spec-analyst` · model passed: none (skill names none; agent default sonnet) · attempt 1 · STATUS: OK (7 findings)
- Agent said: `claude-sonnet-5-5`, tools Read, Glob, Grep, SubagentHandback.
- Report arrived as a SubagentHandback message, not in the Agent tool result. Raw block: `eval/analyst-round-1.md`.

## D2 — analyst round 2 (FOCUSED)
- subagent_type: `sdd:spec-analyst` · model passed: none · attempt 1 · STATUS: OK (1 finding, F8 medium)
- Agent said: `claude-sonnet-5-5`, tools Read, Glob, Grep, SubagentHandback. Raw: `eval/analyst-round-2.md`.

## D3 — analyst round 3 (FOCUSED)
- subagent_type: `sdd:spec-analyst` · model passed: none · attempt 1 · STATUS: OK (NO FINDINGS)
- Agent said: `claude-sonnet-5-5`. Leak: it cites the Script's future "hand edit to 50" (project CLAUDE.md is in subagent context). Raw: `eval/analyst-round-3.md`.

## D4 — analyst VERIFY
- subagent_type: `sdd:spec-analyst` · model passed: none · attempt 1 · STATUS: OK (NO FINDINGS). Raw: `eval/analyst-round-verify.md`.

## D5 — run 1, wave 0, leaf 1.1
- subagent_type: `sdd:spec-task-runner` · Size M · model passed: `sonnet` · attempt 1 · STATUS: done
- Agent said: Sonnet 5.5 (claude-sonnet-5-5).
```
TASK: 1.1
STATUS: done
FILES: shop/discounts.py
TESTS: uv run --no-project --with pytest --with hypothesis python -c "import shop.discounts" -> exit 0 (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: Created shop/discounts.py (new file, lines 1-61) with DiscountCode, CodeRegistry, is_expired and discount_amount per design. __post_init__ also rejects bool and non-int value and min_subtotal_cents, and an unknown kind. I run as Sonnet 5.5 (claude-sonnet-5-5).
```

## D6 — run 1, wave 1, leaf 1.2 (parallel with D7, one message)
- subagent_type: `sdd:spec-task-runner` · Size M · model passed: `sonnet` · attempt 1 · STATUS: done
```
TASK: 1.2
STATUS: done
FILES: /Users/baodang/Documents/code/sdd-mock/f1-discounts-v031/tests/test_discounts.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_discounts.py -> 5 pass / 0 fail (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: Model: Sonnet 5.5 (claude-sonnet-5-5). New file tests/test_discounts.py: 4 property tests (P1, P2, P4, P5; max_examples=200, each with a Feature: discount-codes tag comment) plus the duplicate-add example test (1.6). The P5 test hard-codes the percent upper bound 90, so it must change if the bound edit to 50 lands.
```
- Leak: runner knows the Script's future "bound edit to 50" (project CLAUDE.md in subagent context).

## D7 — run 1, wave 1, leaf 3.1
- subagent_type: `sdd:spec-task-runner` · Size M · model passed: `sonnet` · attempt 1 · STATUS: done
```
TASK: 3.1
STATUS: done
FILES: shop/cart.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_cart.py -> 3 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: Added AlreadyApplied, applied_code, apply_code, clear_code, discount_cents, total_cents in shop/cart.py (imports at top, methods appended at end). Ran as Sonnet 5.5 (claude-sonnet-5-5).
```

## D8 — run 1, wave 2, leaf 3.2 (parallel with D9, one message)
- subagent_type: `sdd:spec-task-runner` · Size M · model passed: `sonnet` · attempt 1 · STATUS: done
```
TASK: 3.2
STATUS: done
FILES: tests/test_cart_discount.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_cart_discount.py -> 4 pass / 0 fail (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: New file tests/test_cart_discount.py: Property 3 hypothesis test (200 examples, tag comment line 40) plus 3 examples for 2.5, 5.3, 4.4. Ran as claude-sonnet-5-5 (Sonnet 5.5).
```

## D9 — run 1, wave 2, leaf 5.1
- subagent_type: `sdd:spec-task-runner` · Size M · model passed: `sonnet` · attempt 1 · STATUS: done
```
TASK: 5.1
STATUS: done
FILES: /Users/baodang/Documents/code/sdd-mock/f1-discounts-v031/shop/api.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_cart.py -> 3 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: Model: Sonnet 5.5 (claude-sonnet-5-5). api.py: POST /carts/<id>/code (order cart 404, 400, 404, 410, 422, 409, 200), DELETE clears code, GET adds code/discount_cents/total_cents via ctx["today"]. The handle docstring is not updated to mention ctx["codes"] and ctx["today"]. No test hits the new routes.
```

## D10 — run 1, wave 3, leaf 5.2
- subagent_type: `sdd:spec-task-runner` · Size M · model passed: `sonnet` · attempt 1 · STATUS: done
```
TASK: 5.2
STATUS: done
FILES: tests/test_api_codes.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_api_codes.py -> 5 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: Runs as Sonnet 5.5 (claude-sonnet-5-5). tests/test_api_codes.py:1 has the Property 6 tag. The property test at :36-85 uses 200 examples over 6 booleans and checks status, error and state. Four example tests follow: apply then GET, DELETE clears, DELETE with no code, DELETE on unknown cart. A first sed call failed on macOS, so I removed an unused line with grep instead.
```

## D11 — run 2, wave 0, leaf 1.1
- subagent_type: `sdd:spec-task-runner` · Size M · model passed: `sonnet` · attempt 1 · STATUS: done
```
TASK: 1.1
STATUS: done
FILES: shop/discounts.py
TESTS: uv run --no-project --with pytest --with hypothesis python -c "import shop.discounts" -> exit 0 (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: shop/discounts.py already existed and matched the design. Only change: line 7 PERCENT_MAX 90 -> 50 to match the edited requirement 1.2 and the design. Runs as Sonnet 5.5 (claude-sonnet-5-5). Other tests were not run (Verify is the import only).
```

## D12 — run 2, wave 1, leaf 1.2
- subagent_type: `sdd:spec-task-runner` · Size M · model passed: `sonnet` · attempt 1 · STATUS: done
```
TASK: 1.2
STATUS: done
FILES: tests/test_discounts.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_discounts.py -> 5 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: Model: Sonnet 5.5 (claude-sonnet-5-5). The file already held Properties 1, 2, 4, 5 (max_examples=200, tag comments) and the duplicate-add example test (1.6). Req 1.2 now caps percent at 50, so I changed the percent bound 90 to 50 at tests/test_discounts.py:18 (generator) and :59 (validation oracle). The file is untracked, so git diff shows nothing for it.
```

## D13 — run 2, wave 2, leaf 3.2
- subagent_type: `sdd:spec-task-runner` · Size M · model passed: `sonnet` · attempt 1 · STATUS: done
```
TASK: 3.2
STATUS: done
FILES: tests/test_cart_discount.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_cart_discount.py -> 4 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: Model: Sonnet 5.5 (claude-sonnet-5-5). The file already had the property test (200 examples, tag comment) and the 3 example tests. I changed the import at line 8 to add PERCENT_MAX and PERCENT_MIN. I changed the percent strategy at line 19 from a hard-coded 1..90 to PERCENT_MIN..PERCENT_MAX. The file is untracked, so git diff shows no output for it.
```


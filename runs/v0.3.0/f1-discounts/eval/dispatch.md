# Dispatch log

## D1 — round 1 (spec-analyze FULL)
- subagent_type: sdd:spec-analyst · model passed: none (skill names none; frontmatter `sonnet`) · attempt 1 · STATUS: 4 findings (3 medium, 1 low)
- Agent said: "Model: Sonnet 5.5 (claude-sonnet-5-5)"
- Raw report: `eval/analyst-round-1.md`

## D2 — round 2 (spec-analyze FULL)
- subagent_type: sdd:spec-analyst · model passed: none · attempt 1 · STATUS: 5 findings (4 medium, 1 low)
- Agent said: "Model: Sonnet 5.5 (claude-sonnet-5-5)"
- Raw report: `eval/analyst-round-2.md`

## D3 — round 3 (spec-analyze FULL)
- subagent_type: sdd:spec-analyst · model passed: none · attempt 1 · STATUS: 2 findings (1 medium, 1 low)
- Agent said: "Model: Sonnet 5.5 (claude-sonnet-5-5)"
- Raw report: `eval/analyst-round-3.md`

## D4 — verify (spec-analyze VERIFY)
- subagent_type: sdd:spec-analyst · model passed: none · attempt 1 · STATUS: NO FINDINGS
- Raw report: `eval/analyst-round-4-verify.md`

## D5 — leaf 1.1 (spec-run run 1, wave 0)
- subagent_type: sdd:spec-task-runner · model passed: sonnet (Size M) · attempt 1 · STATUS: done
```
TASK: 1.1
STATUS: done
FILES: /Users/baodang/Documents/code/sdd-mock/f1-discounts/shop/discounts.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q -> 3 passed, 0 failed (expected: green); import check passed
COUNTEREXAMPLE: none
NOTES: Model: Sonnet 5.5 (claude-sonnet-5-5). Percent/fixed range checks run after the type(x) is int check, so bool is rejected. Duplicate check uses upper-case key.
```

## D6 — leaf 1.2 (spec-run run 1, wave 1)
- subagent_type: sdd:spec-task-runner · model passed: haiku (Size S) · attempt 1 · STATUS: done
```
TASK: 1.2
STATUS: done
FILES: shop/cart.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_cart.py -> 3 pass / 0 fail (expected: green)
COUNTEREXAMPLE: none
NOTES: Added self.code slot, attach, detach, discount_cents(today) delegating to discounts.discount_cents, total_cents(today) = max(0, subtotal - discount). Full suite also 3 pass. Smoke check: 2x450 subtotal, 10% code -> discount 90, total 810; detach -> 900. Model: claude-haiku-5-5 (Haiku 5.5).
```

## D7 — leaf 1.3 (spec-run run 1, wave 2, parallel with D8)
- subagent_type: sdd:spec-task-runner · model passed: sonnet (Size M) · attempt 1 · STATUS: done
```
TASK: 1.3
STATUS: done
FILES: /Users/baodang/Documents/code/sdd-mock/f1-discounts/tests/test_discounts.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_discounts.py -> 4 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none
NOTES: Model: Sonnet 5.5 (claude-sonnet-5-5). Properties 1, 2 and 3 are tagged and run at max_examples of 200-300. Property 3 calls the pure discount_cents(), not Cart.discount_cents, so it does not depend on cart.py.
```

## D8 — leaf 3.1 (spec-run run 1, wave 2, parallel with D7)
- subagent_type: sdd:spec-task-runner · model passed: sonnet (Size M) · attempt 1 · STATUS: done
```
TASK: 3.1
STATUS: done
FILES: /Users/baodang/Documents/code/sdd-mock/f1-discounts/shop/api.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q -> 7 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none
NOTES: Model: Sonnet 5.5 (claude-sonnet-5-5). Manual handle() check: SAVE10 (10%) on a 900c cart gave 200 with discount_cents 90. A second apply gave 409. GET, DELETE (200, then 404 `no code applied`) and POST /lines totals all matched the spec.
- Line body uses `quantity` and `unit_price_cents`, per the design. `unit_price_cents` is validated and not used. Bool values are rejected (`type is int`). A body that is not a dict gives `bad code` or `bad line`.
```

## D9 — leaf 3.2 (spec-run run 1, wave 3)
- subagent_type: sdd:spec-task-runner · model passed: sonnet (Size M) · attempt 1 · STATUS: done
```
TASK: 3.2
STATUS: done
FILES: /Users/baodang/Documents/code/sdd-mock/f1-discounts/tests/test_api_discounts.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_api_discounts.py -> 8 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none
NOTES: Properties 4-7 use 200 examples each and carry the "# Feature: cart-discount-codes, Property N" tag comments. Example tests cover 2.7, 4.1, 4.2 and 4.4. I ran as Sonnet 5.5 (claude-sonnet-5-5). I did not run the full test suite.
```

## D10 — leaf 1.1 (spec-run run 2, wave 0)
- subagent_type: sdd:spec-task-runner · model passed: sonnet (Size M) · attempt 1 · STATUS: done
```
TASK: 1.1
STATUS: done
FILES: /Users/baodang/Documents/code/sdd-mock/f1-discounts/shop/discounts.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q -> 13 pass, 2 fail (expected: green)
COUNTEREXAMPLE: kind=percent, value=51 (raised ValueError in the test's own setup; see NOTES)
NOTES: I ran as Sonnet 5.5 (claude-sonnet-5-5). I changed the percent bound in register from 1–90 to 1–50. The rest of the module already matched the leaf. The import check was not run separately, but the tests import the module.
NOTES: The 2 failures are stale tests that I do not own, so I did not edit them. tests/test_api_discounts.py:60 and :120 generate percent values up to 90. test_apply_first_failing_check and test_apply_then_remove_restores now hit the new bound. tests/test_discounts.py:38 and :102 also still use 1–90. Change these test bounds to 1–50 (probably in the tests leaves).
```
- Orchestrator note: STATUS `done` taken as given (skill step 5). Verify "existing tests pass" did not hold (2 fail), but the failing tests belong to in-scope leaf 3.2. Counterexample is in a stale test, not an implementation defect.

## D11 — leaf 1.3 (spec-run run 2, wave 2)
- subagent_type: sdd:spec-task-runner · model passed: sonnet (Size M) · attempt 1 · STATUS: done
```
TASK: 1.3
STATUS: done
FILES: /Users/baodang/Documents/code/sdd-mock/f1-discounts/tests/test_discounts.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_discounts.py -> 4 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none
NOTES: Percent bound changed 90 -> 50 in the model (_model_ok) and in the percent_code generator. I added st.integers(45, 95) to int_like so the 50/51 boundary gets tested. shop/discounts.py already uses 1..50. Model: Sonnet 5.5 (claude-sonnet-5-5).
```

## D12 — leaf 3.2 (spec-run run 2, wave 3)
- subagent_type: sdd:spec-task-runner · model passed: sonnet (Size M) · attempt 1 · STATUS: done
```
TASK: 3.2
STATUS: done
FILES: /Users/baodang/Documents/code/sdd-mock/f1-discounts/tests/test_api_discounts.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_api_discounts.py -> 8 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none
NOTES: Changed percent bound 90 -> 50 at line 60 and line 120 (criterion 1.2). Line 120 draws one value for both kinds, so fixed codes in that test now only use 1-50. That is still valid. I ran as Sonnet 5.5 (claude-sonnet-5-5).
```


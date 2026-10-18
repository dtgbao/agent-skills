# Dispatch log

## D1 — analyst round 1 (FULL)
- subagent_type: sdd:spec-analyst · model passed: omitted (frontmatter sonnet, per spec-analyze step 2) · attempt 1 · STATUS: n/a (5 findings)
- Report came as hand-back message, not as the Agent tool result. Raw block: `eval/analyst-round-1.md`.

## D2 — analyst round 2 (FOCUSED)
- subagent_type: sdd:spec-analyst · model passed: omitted (frontmatter sonnet) · attempt 1 · STATUS: n/a (NO FINDINGS)
- Hand-back message. Raw block: `eval/analyst-round-2.md`.

## D3 — analyst VERIFY 1
- subagent_type: sdd:spec-analyst · model passed: omitted (frontmatter sonnet) · attempt 1 · STATUS: n/a (1 medium: F6)
- Hand-back message. Raw block: `eval/analyst-verify-1.md`.

## D4 — analyst VERIFY 2
- subagent_type: sdd:spec-analyst · model passed: omitted (frontmatter sonnet) · attempt 1 · STATUS: n/a (NO FINDINGS)
- Raw block: `eval/analyst-verify-2.md`.

## D5 — leaf 1.1 (wave 0)
- subagent_type: sdd:spec-task-runner · Size M · model passed: sonnet · attempt 1 · STATUS: done
```
TASK: 1.1
STATUS: done
FILES: /Users/baodang/Documents/code/sdd-mock/f1-discounts-v033/shop/discounts.py
TESTS: uv run --no-project --with pytest --with hypothesis python -c "...Verify one-liner..." -> pass (printed ok) (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: New file shop/discounts.py (untracked, so no git diff): DiscountError, DiscountCode, CODE_RE, MAX_CENTS, CodeRegistry.add/get, compute_discount. add() validates before storing, rejects bool, and checks for duplicates last. I did not read requirements.md or design.md, so I worked only from the leaf text.
```
- Note: runner says it skipped its step 1 (read criteria + design).

## D6 — leaf 1.2 (wave 1)
- subagent_type: sdd:spec-task-runner · Size M · model passed: sonnet · attempt 1 · STATUS: done
```
TASK: 1.2
STATUS: done
FILES: /Users/baodang/Documents/code/sdd-mock/f1-discounts-v033/tests/test_discounts.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_discounts.py -> 7 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: New file tests/test_discounts.py. Properties 1, 2, 4, 5 and 6 each have a tag comment, and Property 1 and Property 6 have two tests each. max_examples is 100, except 300 for the main Property 1 test.
```

## D7 — leaf 3.1 (wave 1, same message as D6)
- subagent_type: sdd:spec-task-runner · Size M · model passed: sonnet · attempt 1 · STATUS: done
```
TASK: 3.1
STATUS: done
FILES: shop/cart.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_cart.py -> 3 passed, 0 failed; inline python assert check -> OK (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: shop/cart.py:2 import, :11 applied_code init, :26-45 apply_code/remove_code/discount_cents/total_cents.
```

## D8 — leaf 3.2 (wave 2)
- subagent_type: sdd:spec-task-runner · Size M · model passed: sonnet · attempt 1 · STATUS: done
```
TASK: 3.2
STATUS: done
FILES: /Users/baodang/Documents/code/sdd-mock/f1-discounts-v033/tests/test_cart_discount.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_cart_discount.py -> 3 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: New file tests/test_cart_discount.py: Properties 3 and 8 use max_examples=100, Property 7 uses 200. Each has a tag comment. Property 7 compares apply_code to a reference model of the 2.7 order. Inventory stock is 10**9 per sku, so add never raises OutOfStock. No git diff line to cite because the file is untracked.
```

## D9 — leaf 5.1 (wave 2, same message as D8)
- subagent_type: sdd:spec-task-runner · Size M · model passed: sonnet · attempt 1 · STATUS: done
```
TASK: 5.1
STATUS: done
FILES: /Users/baodang/Documents/code/sdd-mock/f1-discounts-v033/shop/api.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q -> 10 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: shop/api.py: added _totals and the DiscountError import near the top, updated the ctx docstring, added a /discount branch before the /lines branch, and changed the GET body to lines, code and totals. I did not add new tests, so the routes are not covered by the existing suite.
```

## D10 — leaf 5.2 (wave 3)
- subagent_type: sdd:spec-task-runner · Size S · model passed: haiku · attempt 1 · STATUS: done
```
TASK: 5.2
STATUS: done
FILES: tests/test_api_discount.py (new)
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_api_discount.py -> 9 pass / 0 fail (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: Example tests cover 5.1 (200 totals on apply), 5.2 (400 unknown code, expired, below minimum; shop/api.py:23-26 maps DiscountError to 400), 5.3 (409 on second code; shop/api.py:24-25), 5.4 (DELETE 200 totals), 5.5 (GET keys, lines, code null before/after apply and delete; shop/api.py:44-45), 5.6 (400 bad code for missing body, missing code, and non-str code values; shop/api.py:17-19). Calls handle() directly with a fixed CodeRegistry and TODAY=2026-10-18. No Hypothesis property, so no tag comment was added.
```
- Note: file:line cites in NOTES do not match `git diff` (real DiscountError mapping is at shop/api.py:33-36).

## D11 — leaf 1.1 (run 2, wave 0)
- subagent_type: sdd:spec-task-runner · Size M · model passed: sonnet · attempt 1 · STATUS: done
```
TASK: 1.1
STATUS: done
FILES: /Users/baodang/Documents/code/sdd-mock/f1-discounts-v033/shop/discounts.py
TESTS: uv run --no-project --with pytest --with hypothesis python -c "<Verify>" -> printed ok, assertions pass (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: shop/discounts.py was already untracked (no git diff); it capped percent at 90, so I changed it to 50 per spec (the `1 <= code.value <= 50` line in CodeRegistry.add). Other rules matched the spec. shop/api.py and shop/cart.py are modified by others; I did not touch them.
```

## D12 — leaf 1.2 (run 2, wave 1)
- subagent_type: sdd:spec-task-runner · Size M · model passed: sonnet · attempt 1 · STATUS: done
```
TASK: 1.2
STATUS: done
FILES: /Users/baodang/Documents/code/sdd-mock/f1-discounts-v033/tests/test_discounts.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_discounts.py -> 7 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: The file already existed (untracked) and used percent bound 90. I changed it to 50 per criterion 1.2 at tests/test_discounts.py:14 and :30. I added st.integers(45, 55) to the Property 1 value generator at :44 so the 50/51 boundary is hit. Properties 1, 2, 4, 5 and 6 each have a tag comment and max_examples of at least 100.
```

## D13 — leaf 3.2 (run 2, wave 2)
- subagent_type: sdd:spec-task-runner · Size M · model passed: sonnet · attempt 1 · STATUS: done
```
TASK: 3.2
STATUS: done
FILES: tests/test_cart_discount.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_cart_discount.py -> 3 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: The file was untracked and already held Properties 3, 7 and 8 with tag comments and max_examples of 100 or 200. I changed the percent range at tests/test_cart_discount.py:30 from 1–90 to 1–50, as criterion 1.2 requires. The `git diff` stat is empty because the file is untracked.
```


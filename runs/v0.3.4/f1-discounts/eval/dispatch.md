# Dispatch log (plugin 0.3.4)

## D1 — analyst round 1 (FULL)
- subagent_type: sdd:spec-analyst · model passed: omitted (frontmatter sonnet) · attempt 1 · STATUS: n/a (6 findings)
- Hand-back message. Raw block: `eval/analyst-round-1.md`.

## D2 — analyst round 2 (FOCUSED)
- subagent_type: sdd:spec-analyst · model passed: omitted (frontmatter sonnet) · attempt 1 · STATUS: n/a (1 high NEEDS_OWNER: F7)
- Raw block: `eval/analyst-round-2.md`.

## D3 — analyst round 3 (FOCUSED)
- subagent_type: sdd:spec-analyst · model passed: omitted (frontmatter sonnet) · attempt 1 · STATUS: n/a (NO FINDINGS)
- Raw block: `eval/analyst-round-3.md`.

## D4 — analyst VERIFY 1
- subagent_type: sdd:spec-analyst · model passed: omitted (frontmatter sonnet) · attempt 1 · STATUS: n/a (F8 medium, F9 low)
- Raw block: `eval/analyst-verify-1.md`.

## D5 — analyst VERIFY 2
- subagent_type: sdd:spec-analyst · model passed: omitted (frontmatter sonnet) · attempt 1 · STATUS: n/a (F11 medium → Open Questions)
- Raw block: `eval/analyst-verify-2.md`.

## D6 — leaf 1.1 (run 1, wave 0)
- subagent_type: sdd:spec-task-runner · Size M · model passed: sonnet · attempt 1 · STATUS: done · prompt: `eval/prompt-1.1-run1.txt` (12 cited criteria)
```
TASK: 1.1
STATUS: done
FILES: /Users/baodang/Documents/code/sdd-mock/f1-discounts-v033/shop/discounts.py (new)
TESTS: uv run --no-project --with pytest --with hypothesis python -c "...(Verify one-liner)..." -> pass (rc=0) (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: Covers 1.1-1.7, 4.1-4.3, 4.5, 4.6 in shop/discounts.py (CodeBook.create validates kind, amount, range, code format, min_subtotal, valid_until, duplicate before storing; discount_for at the end of the file). bool is rejected for amount and min_subtotal.
```

## D7 — leaf 1.2 (run 1, wave 1)
- subagent_type: sdd:spec-task-runner · Size M · model passed: sonnet · attempt 1 · STATUS: done · prompt: `eval/prompt-1.2-run1.txt` (12 cited)
```
TASK: 1.2
STATUS: done
FILES: /Users/baodang/Documents/code/sdd-mock/f1-discounts-v033/tests/test_discounts.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_discounts.py -> 3 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: Covers 1.1-1.7 (Properties 1, 2: test_discounts.py) and 4.1-4.3, 4.5, 4.6 (Property 3). Each test has a Feature tag comment. max_examples is 300, 200 and 300. Generators follow design.md Testing Strategy rows 1-3.
```

## D8 — leaf 3.1 (run 1, wave 1, same message as D7)
- subagent_type: sdd:spec-task-runner · Size M · model passed: sonnet · attempt 1 · STATUS: done · prompt: `eval/prompt-3.1-run1.txt` (13 cited)
```
TASK: 3.1
STATUS: done
FILES: shop/cart.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_cart.py -> 3 passed, 0 failed; inline attach/detach check printed ok (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: 2.1-2.7, 3.1, 3.2, 4.3-4.6 covered in shop/cart.py (imports, `attached` in __init__, attach_code, detach_code, discount_cents, amount_due_cents; +25 lines). Checked only by the Verify commands, with no per-criterion tests. Attach refusals follow the 2.7 order and write nothing before a raise.
```
- Note: runner step 1 Done-when ("every cited criterion id has a test case or check in your Verify") did not hold; runner says so and still reports done.

## D9 — leaf 3.2 (run 1, wave 2)
- subagent_type: sdd:spec-task-runner · Size M · model passed: sonnet · attempt 1 · STATUS: done · prompt: `eval/prompt-3.2-run1.txt` (10 cited)
```
TASK: 3.2
STATUS: done
FILES: /Users/baodang/Documents/code/sdd-mock/f1-discounts-v033/tests/test_cart_codes.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_cart_codes.py -> 3 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: Covers 4.4 (P4, test_amount_due_identity), 2.1-2.7 (P5, test_attach_matches_precedence, reference function in 2.7 order, checks attached unchanged on refusal), 3.1/3.2 (P6, test_detach_idempotent); max_examples 200/300/200; one tag comment per property; the file is new and untracked, so there is no git diff.
```

## D10 — leaf 5.1 (run 1, wave 2, same message as D9)
- subagent_type: sdd:spec-task-runner · Size M · model passed: sonnet · attempt 1 · STATUS: done · prompt: `eval/prompt-5.1-run1.txt` (7 cited)
```
TASK: 5.1
STATUS: done
FILES: shop/api.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q -> 6 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: Covers 5.1-5.7 in shop/api.py. I added `_context_ok`, `_prices` and the guard before the cart lookup. The PUT, DELETE and GET code routes come after the lookup. No new tests: the leaf's Verify only asks for the existing suite to stay green.
```
- Note: same Done-when gap as D8 (Verify has no check per cited criterion).

## D11 — leaf 5.2 (run 1, wave 3)
- subagent_type: sdd:spec-task-runner · Size M · model passed: sonnet · attempt 1 · STATUS: done · prompt: `eval/prompt-5.2-run1.txt` (7 cited)
```
TASK: 5.2
STATUS: done
FILES: tests/test_api_codes.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_api_codes.py -> 7 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: 5.1 test_put_success_200; 5.2 test_put_refused_422_each_reason (4 reasons); 5.3 test_put_invalid_body_400 (missing and non-str); 5.4 test_delete_200; 5.5 test_get_code_null_and_set; 5.6 and 5.7 Property 7 test_bad_context_500_unchanged (max_examples=200, tag comment, PUT/DELETE/GET, missing and bad today, missing code_book, lines and attached unchanged). New untracked file, so no git diff lines.
```

## D12 — leaf 1.1 (run 2, wave 0)
- subagent_type: sdd:spec-task-runner · Size M · model passed: sonnet · attempt 1 · STATUS: done · prompt: `eval/prompt-1.1-run2.txt` (12 cited; 1.2 carries new text `1–50`)
```
TASK: 1.1
STATUS: done
FILES: shop/discounts.py
TESTS: uv run --no-project --with pytest --with hypothesis python -c "<Verify one-liner>" -> printed ok, assertions pass (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: Criteria 1.1-1.7, 4.1-4.3, 4.5, 4.6 covered. The file already existed untracked, so there is no git diff. It was otherwise correct. I fixed PERCENT_RANGE from (1, 90) to (1, 50) at shop/discounts.py:6 to meet 1.2. I ran only the Verify one-liner, not the pytest suite.
```

## D13 — leaf 1.2 (run 2, wave 1)
- subagent_type: sdd:spec-task-runner · Size M · model passed: sonnet · attempt 1 · STATUS: done · prompt: `eval/prompt-1.2-run2.txt` (leaf text same as run 1; only cited 1.2 text holds `1–50`)
```
TASK: 1.2
STATUS: done
FILES: tests/test_discounts.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_discounts.py -> 3 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: Covers 1.1-1.7 (Properties 1, 2) and 4.1, 4.2, 4.3, 4.5, 4.6 (Property 3). The file already existed as untracked. I changed the percent range from 1–90 to 1–50 in the reference model (`_expect_valid`) and in the `_valid_record` percent generator. Each property test has a tag comment, and `max_examples` is 300, 200 and 300.
```

## D14 — leaf 3.2 (run 2, wave 2)
- subagent_type: sdd:spec-task-runner · Size M · model passed: sonnet · attempt 1 · STATUS: done · prompt: `eval/prompt-3.2-run2.txt` (10 cited; Do holds the sync note `1–50 (criterion 1.2)`)
```
TASK: 3.2
STATUS: done
FILES: tests/test_cart_codes.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_cart_codes.py -> 3 passed, 0 failed (expected: green; run 3 times, all green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: Covers 4.4 (Property 4), 2.1-2.7 (Property 5, reference function in 2.7 order, max_examples=300), 3.1-3.2 (Property 6). The file was untracked and already existed. It failed because the `records` strategy generated percent amounts 51-90, and `CodeBook.create` rejects those (criterion 1.2). I split `records` into a percent strategy (1-50) and a fixed strategy (1-90000). Each of the three properties has its Feature tag comment and runs at least 200 examples, except Property 5 at 300.
```


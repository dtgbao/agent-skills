# Dispatches (plugin 0.3.4 rerun)

Each prompt is saved in eval/prompts/<leaf>.md (holds the cited criterion text).

## 1 — leaf 1.1 (pin red, Size S) — cmd 2
subagent_type: sdd:spec-task-runner · model passed: haiku · attempt 1 · STATUS: done
Report came as a hand-back message. COUNTEREXAMPLE present, but leaf is `Expect: red` pin with STATUS done → spec-run step 6 exempt → `[x]`.
```
TASK: 1.1
STATUS: done
FILES: tests/test_overbooking_repro.py (new file)
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_overbooking_repro.py -> 0 pass / 3 fail (expected: red)
COUNTEREXAMPLE: s=1, h=1, q=1 (Hypothesis shrunk input for test_property_fix_check). Reserve of q=1 did not raise OutOfStock, so the bug is shown. Test left unchanged.
FOREIGN-FAIL: none
NOTES: Covers 2.1 (test_two_carts_overbook), 2.2 (test_two_carts_overbook, available == 2 assert after the raise check), 2.3 (test_one_cart_overbooks), and Property 1 (test_property_fix_check, tagged `Feature: stock-overbooking, Property 1: Fix check`, max_examples=200). All 3 fail with "DID NOT RAISE OutOfStock", which is the stated bug. Test file lines: test_two_carts_overbook at tests/test_overbooking_repro.py:9, test_one_cart_overbooks at :18, property at :26. Ran as claude-haiku-5-5 (Haiku 5.5).
```

## 2 — leaf 1.2 (pin green, Size M) — cmd 2
subagent_type: sdd:spec-task-runner · model passed: sonnet · attempt 1 · STATUS: done
```
TASK: 1.2
STATUS: done
FILES: tests/test_overbooking_keep_inventory.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_overbooking_keep_inventory.py -> 4 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: Covers 3.1, 3.2, 3.3, 3.5, one test each, max_examples=200, Property 2 tag on each (new file, tests/test_overbooking_keep_inventory.py:1-62). Ran as Sonnet 5.5 (claude-sonnet-5-5).
```

## 3 — leaf 1.3 (pin green, Size S) — cmd 2
subagent_type: sdd:spec-task-runner · model passed: haiku · attempt 1 · STATUS: done
```
TASK: 1.3
STATUS: done
FILES: tests/test_overbooking_keep_cart.py (new)
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_overbooking_keep_cart.py -> 3 pass / 0 fail (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: Covers 3.4 (Hypothesis, max_examples=200, tag `Feature: stock-overbooking, Property 2: Preservation`, add then remove restores available, s in 1-40, q in 1-s), 3.6 (example: stock 2, add 1, add 3 raises OutOfStock, lines == {MUG-01: 1}), 3.7 (example via shop.api.handle, POST add qty 3 on stock 2 returns 409). Ran as model claude-haiku-5-5 (Haiku 5.5). Shop code not edited.
```

## 4 — leaf 2.1 (fix, Size S) — cmd 2
subagent_type: sdd:spec-task-runner · model passed: haiku · attempt 1 · STATUS: done
```
TASK: 2.1
STATUS: done
FILES: shop/inventory.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_overbooking_repro.py tests/test_overbooking_keep_inventory.py tests/test_overbooking_keep_cart.py tests/test_cart.py -> 13 pass / 0 fail (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: Criteria 2.1, 2.2, 2.3 covered by the verify run (repro, keep_inventory, keep_cart, test_cart all green). Changed guard at shop/inventory.py:18 from `qty > self._initial[sku]` to `qty > self.available(sku)`. The `qty < 1` check at line 16-17 is unchanged and still first. Model: claude-haiku-5-5 (Haiku 5.5).
```

## 5 — leaf 4.1* (optional stateful test, Size M) — cmd 3
subagent_type: sdd:spec-task-runner · model passed: sonnet · attempt 1 · STATUS: done
```
TASK: 4.1
STATUS: done
FILES: tests/test_overbooking_stateful.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_overbooking_stateful.py -> 1 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: Covers 2.1 (add rule expects OutOfStock iff qty > model free), 2.2 (invariant available == stock - cart lines, >= 0), 3.4 (remove rule checks available rises by the line qty); the state machine is in tests/test_overbooking_stateful.py (new file, so no git diff lines). Settings are max_examples=100, stateful_step_count=30. Ran as Sonnet 5.5 (claude-sonnet-5-5).
```

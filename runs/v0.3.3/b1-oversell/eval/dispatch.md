# Dispatches

## 1 — leaf 1.1 (exploration pin, Size S)
subagent_type: sdd:spec-task-runner · model passed: haiku · attempt 1 · STATUS: done
Report came as a hand-back message (Agent result said so).
```
TASK: 1.1
STATUS: done
FILES: tests/test_oversell_pin.py (new)
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_oversell_pin.py -> 0 pass / 3 fail (expected: red)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: Red for the stated bug. Example 1 (tests/test_oversell_pin.py:9-17): "DID NOT RAISE OutOfStock" (cart B add accepted). Example 2 (:20-34): "assert 200 == 409" (second POST accepted). Property 1 (:36-50, tag "Feature: cart-oversell, Property 1: Fix check", max_examples=100, uses assume(a+b > stock)): fails at first draw, stock=1, a=1, b=1, with "DID NOT RAISE OutOfStock". Cause is shop/inventory.py reserve(), which checks qty > initial stock, not available. Ran as model: Haiku 5.5 (claude-haiku-5-5).
```

## 2 — leaf 1.2 (preservation pins, Size M)
subagent_type: sdd:spec-task-runner · model passed: sonnet · attempt 1 · STATUS: done
Report came as a hand-back message.
```
TASK: 1.2
STATUS: done
FILES: tests/test_oversell_preservation.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_oversell_preservation.py -> 5 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: New file (untracked, so no git diff) with 5 Hypothesis tests, one per item 3.1-3.5, each max_examples=100 and tagged "Feature: cart-oversell, Property 2: Preservation". Model: Sonnet 5.5 (claude-sonnet-5-5).
```

## 3 — leaf 2.1 (fix, Size S)
subagent_type: sdd:spec-task-runner · model passed: haiku · attempt 1 · STATUS: done
Report came as a hand-back message.
```
TASK: 2.1
STATUS: done
FILES: shop/inventory.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_oversell_pin.py tests/test_oversell_preservation.py tests/test_cart.py -> 11 pass / 0 fail (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: shop/inventory.py:18 changed from `if qty > self._initial[sku]:` to `if qty > self.available(sku):` (git diff confirmed; qty < 1 check still at line 16, nothing else changed). Ran as claude-haiku-5-5 (Haiku 5.5).
```

## 4 — leaf 4.1* (optional API test, Size S) — cmd 3
subagent_type: sdd:spec-task-runner · model passed: haiku · attempt 1 · STATUS: done
Report came as a hand-back message.
```
TASK: 4.1
STATUS: done
FILES: tests/test_api_oversell.py (new)
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_api_oversell.py -> 2 pass / 0 fail (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: Model: claude-haiku-5-5 (Haiku 5.5). Tests cover same-cart 3+3 (409, body {"error": "out of stock"}, GET lines MUG-01 == 3) and two carts 3+2 (both 200). Fix is in shop/inventory.py:18 (`if qty > self.available(sku)`, per git diff). No property tag needed (example test). Leaf had no Expect, so default green applied.
```

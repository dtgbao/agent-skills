# Dispatches

## D1 — leaf 1.1 (run #1)
subagent_type: sdd:spec-task-runner · model passed: haiku (Size S) · attempt 1 · STATUS: done
```
TASK: 1.1
STATUS: done
FILES: tests/test_oversell_pin.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_oversell_pin.py -> 0 pass / 4 fail (expected: red)
COUNTEREXAMPLE: none
NOTES: Four failures, all from the bug. Three show "DID NOT RAISE OutOfStock" (cart B add 3 with stock 5 and cart A holding 3). The API test shows 200 where 409 is expected (2.4).
NOTES: Model: claude-haiku-5-5 (Haiku 5.5).
```

## D2 — leaf 1.2 (run #1)
subagent_type: sdd:spec-task-runner · model passed: sonnet (Size M) · attempt 1 · STATUS: done
```
TASK: 1.2
STATUS: done
FILES: /Users/baodang/Documents/code/sdd-mock/b1-oversell/tests/test_preservation_pin.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_preservation_pin.py -> 8 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none
NOTES: Example tests cover 3.1-3.6. Hypothesis test (max_examples=100) has the tag comment `Feature: cart-oversell, Property 2: Preservation`.
NOTES: Model: Sonnet 5.5 (claude-sonnet-5-5)
```

## D3 — leaf 2.1 (run #1)
subagent_type: sdd:spec-task-runner · model passed: haiku (Size S) · attempt 1 · STATUS: done
```
TASK: 2.1
STATUS: done
FILES: /Users/baodang/Documents/code/sdd-mock/b1-oversell/shop/inventory.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_oversell_pin.py tests/test_preservation_pin.py tests/test_cart.py -> 15 pass / 0 fail (expected: green)
COUNTEREXAMPLE: none
NOTES: Changed line 18 from `qty > self._initial[sku]` to `qty > self.available(sku)`. `qty < 1` check still first. No other changes.
Model: claude-haiku-5-5 (Haiku 5.5)
```
Orchestrator note: real line is 16, not 18 (git diff). Report format: model line lacks `NOTES:` prefix.

## D4 — leaf 2.2 (run #2, --optional)
subagent_type: sdd:spec-task-runner · model passed: sonnet (Size M) · attempt 1 · STATUS: done
```
TASK: 2.2
STATUS: done
FILES: /Users/baodang/Documents/code/sdd-mock/b1-oversell/tests/test_inventory_props.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_inventory_props.py -> 1 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none
NOTES: Property uses stock 0-50, 1-20 reserves of qty 1-20, max_examples=200. Asserts OutOfStock iff qty > available, available unchanged on raise, available >= 0. Tag comment included.
NOTES: Model: Sonnet 5.5 (claude-sonnet-5-5)
```
Orchestrator check: with `shop/inventory.py` reverted (git stash), this test fails (1 failed). Fix restored after.

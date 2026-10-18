# Dispatch log

## D1 — cmd 2, leaf 1.1 (pin, Size M)
- subagent_type: sdd:spec-task-runner · model passed: sonnet · attempt: 1 · STATUS: done
- Report came via SubagentHandback message, not in the Agent result.
- Orchestrator re-ran Verify: 3 failed (red, as expected).

```
TASK: 1.1
STATUS: done
FILES: /Users/baodang/Documents/code/sdd-mock/b1-oversell-v032/tests/test_oversell_pin.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_oversell_pin.py -> 0 pass / 3 fail (expected: red)
COUNTEREXAMPLE: stock=1, ops=[(0, 1), (0, 1)] (same cart reserves 1 twice with stock 1: no OutOfStock raised). Example test: cart B add 3 after cart A add 3 of 5 raises nothing. API test: the second POST returns 200, not 409.
FOREIGN-FAIL: none
NOTES: New file tests/test_oversell_pin.py (lines 1-50). Two example tests plus Property 1 (tag comment at line 26, max_examples=200). Fails because Inventory.reserve (shop/inventory.py:15) compares qty to _initial, not available. I did not view the available == -1 case. The shrunk counterexample shows the missing OutOfStock.
RAN-AS: claude-sonnet-5-5
```

## D2 — cmd 2, leaf 1.2 (pin, Size M)
- subagent_type: sdd:spec-task-runner · model passed: sonnet · attempt: 1 · STATUS: done
- Report via SubagentHandback. Orchestrator re-ran Verify: 7 passed (green, as expected).

```
TASK: 1.2
STATUS: done
FILES: tests/test_reserve_preserve.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_reserve_preserve.py -> 7 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: New file tests/test_reserve_preserve.py: examples for 3.1-3.6 (lines 10-40) and Property 2 Hypothesis test (max_examples=200, tagged "Feature: reserve-oversell, Property 2: Preservation") over reserve/release/remove with 3 carts.
RAN-AS: claude-sonnet-5-5
```

## D3 — cmd 2, leaf 2.1 (code, Size S)
- subagent_type: sdd:spec-task-runner · model passed: haiku · attempt: 1 · STATUS: done
- Report via SubagentHandback. `git diff shop/`: one line at shop/inventory.py:18, as specified.

```
TASK: 2.1
STATUS: done
FILES: shop/inventory.py
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q -> 13 passed, 0 failed (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: shop/inventory.py:18 changed from `if qty > self._initial[sku]:` to `if qty > self.available(sku):`. The `qty < 1` check at line 16 is unchanged and still first. Full suite (includes tests/test_oversell_pin.py) is green.
RAN-AS: Haiku 5.5 (claude-haiku-5-5)
```

## D4 — cmd 3, leaf 4.1* (test, Size S)
- subagent_type: sdd:spec-task-runner · model passed: haiku · attempt: 1 · STATUS: done
- Report via SubagentHandback.

```
TASK: 4.1
STATUS: done
FILES: tests/test_api_oversell.py (new)
TESTS: uv run --no-project --with pytest --with hypothesis python -m pytest -q tests/test_api_oversell.py -> 1 pass / 0 fail (expected: green)
COUNTEREXAMPLE: none
FOREIGN-FAIL: none
NOTES: Example test (no property). Builds ctx with Inventory({"MUG-01": 5}), POSTs /carts twice, POSTs qty 3 to /carts/1/lines (200) and /carts/2/lines (409 via shop/api.py OutOfStock branch), then GET /carts/2 shows no MUG-01 line. Shop code unchanged by this leaf; the uncommitted fix is at shop/inventory.py:18 (qty > self.available(sku)).
RAN-AS: claude-haiku-5-5
```

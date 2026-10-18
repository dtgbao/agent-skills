# spec-sync proposal (steps 3–5, plugin 0.3.4)

## Coverage (step 3)
- 29 criteria. Each is cited by ≥1 leaf and maps to a design component or property. Uncovered: none. Orphan refs: none. Components without criteria: none.
- changed: 1.2 (`outside 1–90` → `outside 1–50`). Component: Discounts module. Property 1. Leaves 1.1, 1.2.

## Evidence (step 4)
| Leaf | Was | Verdict | Evidence |
|---|---|---|---|
| 1.1 | [x] | todo | AFFECTS 1.2; `shop/discounts.py:6` `PERCENT_RANGE = (1, 90)` |
| 1.2* | [x] | todo | AFFECTS 1.2; `tests/test_discounts.py:28,56` use 90 |
| 3.1 | [x] | done (stays) | not cited by 1.2; `shop/cart.py` holds no bound |
| 3.2* | [x] | todo | SUSPECT confirmed: `tests/test_cart_codes.py:20` `amount=st.integers(1, 90)` builds percent records the book now refuses |
| 5.1 | [x] | done (stays) | not cited; `shop/api.py` holds no bound |
| 5.2* | [x] | done (stays) | not cited; `grep 90 tests/test_api_codes.py` = none |

## Proposed changes (step 5)
| Change | Target | Detail |
|---|---|---|
| edit leaf | 1.1 | Do: `percent amount is outside 1–90` → `1–50` |
| edit leaf | 3.2 | Do: add `Percent amounts are 1–50 (criterion 1.2).` (3.2 does not cite 1.2, so the runner would not get its text) |
| untick | 1.1, 1.2*, group 1, checkpoint 2 | AFFECTS |
| untick | 3.2*, group 3, checkpoint 4 | confirmed SUSPECT |
| untick | checkpoint 6 | every checkpoint after an unticked leaf |
| graph | none | deps and waves unchanged |

```diff
-- [x] 1. Discounts module
-  - [x] 1.1 Write `shop/discounts.py`
+- [ ] 1. Discounts module
+  - [ ] 1.1 Write `shop/discounts.py`
-      ... percent amount is outside 1–90; ...
+      ... percent amount is outside 1–50; ...
-  - [x]* 1.2 Property tests for the discounts module
+  - [ ]* 1.2 Property tests for the discounts module
-- [x] 2. Checkpoint ...
+- [ ] 2. Checkpoint ...
-- [x] 3. Cart code methods
+- [ ] 3. Cart code methods
-  - [x]* 3.2 Property tests for Cart code methods
+  - [ ]* 3.2 Property tests for Cart code methods
-    - Do: ... so `add` never raises.
+    - Do: ... so `add` never raises. Percent amounts are 1–50 (criterion 1.2).
-- [x] 4. Checkpoint ...
+- [ ] 4. Checkpoint ...
-- [x] 6. Checkpoint ...
+- [ ] 6. Checkpoint ...
```

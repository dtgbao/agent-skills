# spec-sync proposal (steps 3–5)

## Coverage (step 3)
- 28 criteria. All cited by ≥1 leaf, all mapped to a design component or property. Orphans: none. Uncovered: none.
- changed: 1.2 (text `1 to 90` → `1 to 50`). Component: Discount records and registry. Property 1. Leaves 1.1, 1.2.

## Evidence (step 4)
| Leaf | Was | Verdict | Evidence |
|---|---|---|---|
| 1.1 | [x] | todo | AFFECTS 1.2. `shop/discounts.py:35` `1 <= code.value <= 90` encodes old value |
| 1.2* | [x] | todo | AFFECTS 1.2. `tests/test_discounts.py:14,30` use 90 |
| 3.1 | [x] | done (stays) | not cited by 1.2; `shop/cart.py` holds no bound |
| 3.2* | [x] | todo | SUSPECT confirmed: `tests/test_cart_discount.py:30` `st.integers(1, 90)` builds now-invalid codes |
| 5.1 | [x] | done (stays) | not cited; `shop/api.py` holds no bound |
| 5.2* | [x] | done (stays) | not cited; `tests/test_api_discount.py` uses percent 10 only |

## Proposed changes (step 5)
| Change | Target | Detail |
|---|---|---|
| edit leaf | 1.1 | Do: `percent value not int 1–90` → `1–50` |
| edit leaf | 1.2 | Do: add `Percent bound 1–50 (criterion 1.2).` |
| edit leaf | 3.2 | Do: add `Valid percent values 1–50 (criterion 1.2).` |
| untick | 1.1, 1.2, group 1, checkpoint 2 | AFFECTS |
| untick | 3.2, group 3, checkpoint 4 | SUSPECT confirmed |
| untick | checkpoint 6 | every checkpoint after an unticked leaf |
| graph | none | deps and waves unchanged |

Diff (tasks.md):
```diff
-- [x] 1. Discount records and registry
-  - [x] 1.1 Create `shop/discounts.py`
+- [ ] 1. Discount records and registry
+  - [ ] 1.1 Create `shop/discounts.py`
-      ... percent value not int 1–90; ...
+      ... percent value not int 1–50; ...
-  - [x]* 1.2 Property tests for registry and discount function
+  - [ ]* 1.2 Property tests for registry and discount function
-    - Do: Hypothesis tests, ... Generators per design.md Testing Strategy.
+    - Do: Hypothesis tests, ... Generators per design.md Testing Strategy. Percent bound 1–50 (criterion 1.2).
-- [x] 2. Checkpoint ...
+- [ ] 2. Checkpoint ...
-- [x] 3. Cart discount methods
+- [ ] 3. Cart discount methods
-  - [x]* 3.2 Property tests for Cart apply, remove, totals
+  - [ ]* 3.2 Property tests for Cart apply, remove, totals
-    - Do: Hypothesis tests, ... so `add` never raises `OutOfStock`.
+    - Do: Hypothesis tests, ... so `add` never raises `OutOfStock`. Valid percent values 1–50 (criterion 1.2).
-- [x] 4. Checkpoint ...
+- [ ] 4. Checkpoint ...
-- [x] 6. Checkpoint ...
+- [ ] 6. Checkpoint ...
```

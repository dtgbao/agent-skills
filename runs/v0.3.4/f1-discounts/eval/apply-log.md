# Analyze apply log (spec-analyze step 4, plugin 0.3.4)

## Round 1
- F1 owner answer (interface/type) → Glossary `Current_Date`. Not a criterion (0.3.4 rule). Analyst id 5.6 unused.
- F2 owner answer (interface/type) → Glossary `Code_Book`. Not a criterion. Analyst id 5.7 unused.
- F3a A → 4.5 replaced (supersede): adds "overriding 4.1 and 4.2".
- F3b A → 4.6 replaced (supersede): same clause. Split from F3 option A, which changed two criteria.
- F4 A → new 2.7.
- F5 A → new 1.7.
- F6 low → `## Open Questions`.
- EARS: grep `SHALL.*SHALL` = 0. Counts per requirement: 7, 7, 2, 6, 5.
- Count 25 → 27.

### Cross-check of changed criteria (0.3.4 step 4)
| Changed | Shares a term with | Result |
|---|---|---|
| 1.7 (Kind, Amount) | 1.1, 1.2, 1.3 | no clash: non-int Amount is refused by 1.7 and also "outside range" in 1.2/1.3; both refuse |
| 2.7 (refusal reasons) | 2.2, 2.3, 2.4, 2.5, 2.6, 5.2 | no clash: 2.6 keeps state for any refusal; 5.2 maps all reasons to 422 |
| 4.5 (Min_Subtotal, Discount_Amount) | 4.1, 4.2, 4.3, 4.4, 2.4 | no clash: override clause resolves F3; 2.4 is attach-time, 4.5 is price-time |
| 4.6 (Valid_Until, Current_Date) | 4.1, 4.2, 2.3, 4.5 | no clash: 4.5 and 4.6 both give 0, so both true at once agree |
Clashes found: 0.

## Round 2
- F7 owner answer (interface/type) → Glossary `Cart code methods`. Not a criterion. Analyst id 2.8 unused.
- No criterion changed → cross-check: nothing to check. Count stays 27.

## Verify 1
- F8 A, split by repair → new 5.6 (status 500 `bad_context`) and new 5.7 (carts unchanged).
- F9 low → `## Open Questions`.

### Cross-check of changed criteria
| Changed | Shares a term with | Result |
|---|---|---|
| 5.6 (Handler, route in Req 5, status) | 5.1, 5.2, 5.3, 5.4, 5.5 | **clash**: `PUT /carts/<id>/code` with no `code` and no `ctx["today"]` → 5.3 says 400, 5.6 says 500. Both cannot hold. → new finding F10, back to step 3 |
| 5.7 (Cart unchanged) | 2.6, 3.1 | no clash |

## F10 (raised by cross-check, step 4 → step 3)
- TYPE: INCONSISTENCY · SEVERITY: medium · AFFECTS: 5.3, 5.6
- A) 5.6: add "before any body check" (500 wins). B) 5.3: body check first (400 wins).
- Chosen A → 5.6 replaced (supersede).
- Cross-check again: 5.6 vs 5.3 now ordered, no clash. vs 5.1/5.4/5.5: no clash (those need a good context).
- Count: 27 → 29. Requirement 5 has 7 criteria.
- F11 → Open Questions (left after final VERIFY). Growth 25 → 29 (+16 %).

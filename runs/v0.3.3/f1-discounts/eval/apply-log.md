# Analyze apply log (spec-analyze step 4)

## Round 1
- F1 (owner answer) → Glossary: Today/Expiry_Date as `datetime.date`, DiscountError, Cart discount methods. New 2.6 (raise DiscountError). Analyst id 2.6 kept.
- F2 A → new 2.7. Text "return the error" → "raise the first error" to match 2.6.
- F3 (owner answer) → Glossary Code_Registry entry. New 1.6 (`get` → None on miss). Analyst id 1.6 kept.
- F4 A → new 1.7. "calendar date" → "`datetime.date`" to match F1 answer.
- F5 A (analyst 2.9) supersedes 2.2 → 2.2 replaced. Logged as supersede; no new number. Keeps Req 2 at 7 criteria.
- Renumber: analyst 2.8/2.9/2.10 unused. No clash.
- EARS check: all 28 criteria one SHALL (grep `SHALL.*SHALL` = 0).
- Count: 24 → 28.

## Verify 1
- F6 (owner answer) → Glossary Discount_Code entry extended. No new criterion (Req 1 already at 7). Analyst id 1.8 unused.

# Q&A (scripted; AskUserQuestion not called)

Script rule: spec-analyze high/medium → option A. Low → deferred without asking (skill step 3).

## spec-analyze round 1

### Call 1 — Requirement 1
| Q | Finding | Options | Answer |
|---|---|---|---|
| 1 | F7 (high) payment decline/timeout | A) 1.3 402 `payment_failed` · B) 1.4 422 `invalid_amount` · Defer | A |
| 2 | F8 (medium) bound inclusivity, cents | A) whole-dollar 10–500 inclusive · B) NEEDS_OWNER · Defer | A |

### Call 2 — Requirement 2 (part 1)
| Q | Finding | Options | Answer |
|---|---|---|---|
| 1 | F3 (medium) "promptly" | A) 2 s for 95 % · B) NEEDS_OWNER · Defer | A |
| 2 | F4 (high) 1000 vs 500 dollar limit | A) 2.3 up to 500 dollars · B) 1.1 range 10–1000 · Defer | A |
| 3 | F5 (high) subtotal above balance | A) partial redeem, balance 0, return amount due · B) 422 `insufficient_balance` · Defer | A |
| 4 | F6 (high) concurrent redeem/void | A) apply in sequence, balance ≥ 0 · B) NEEDS_OWNER · Defer | A |

### Call 3 — Requirement 2 (part 2), 3, 4, 5
| Q | Finding | Options | Answer |
|---|---|---|---|
| 1 | F10 (medium) malformed code, closed Cart | A) 422 `invalid_request` · B) 429 `rate_limited` · Defer | A |
| 2 | F2 (high) Merchant_Portal not in Glossary | A) add Glossary entry · B) drop portal from 3.1 · Defer | A |
| 3 | F1 (high) never expire vs 12-month void | A) delete 4.2 · B) change 4.1 · Defer | A |
| 4 | F9 (medium) ledger fail after charge | A) 5.3 refund + 503 · B) 5.3 old value null · Defer | A |

Deferred without asking (low): F11, F12, F13.
No NEEDS_OWNER option was chosen (option A never was NEEDS_OWNER).

## spec-analyze round 2

### Call 4 — Requirement 1
| Q | Finding | Options | Answer |
|---|---|---|---|
| 1 | F16 (high) late charge after timeout | A) 1.6 cancel/refund late charge · B) NEEDS_OWNER · Defer | A |
| 2 | F17 (medium) out-of-range purchase value | A) 422 `invalid_request`, no charge · Defer (only one concrete option given) | A |

### Call 5 — Requirement 2, 3, 5
| Q | Finding | Options | Answer |
|---|---|---|---|
| 1 | F14 (medium) 2.1 vs 2.5 negative balance | A) condition 2.1 on subtotal ≤ balance · B) subtract lesser value · Defer | A |
| 2 | F15 (medium) 404 vs 422 for short code | A) 2.4 only for 16-char codes · B) 2.8 before lookup · Defer | A |
| 3 | F19 (medium) void without staff actor | A) 403 `forbidden`, no change · B) NEEDS_OWNER · Defer | A |
| 4 | F18 (medium) refund fails | A) record for manual refund + 503 · B) NEEDS_OWNER · Defer | A |

## spec-analyze round 3

### Call 6 — Requirement 1, 2, 3
| Q | Finding | Options | Answer |
|---|---|---|---|
| 1 | F21 (medium) repeated purchase request | A) idempotency key, return first result, no second charge · B) NEEDS_OWNER · Defer | A |
| 2 | F20 (medium) redemption error order | A) 422 → 404 → 409 · B) 404 → 409 → 422 · Defer | A |
| 3 | F23 (medium) non-staff actor id | A) 403 for missing or non-staff actor · B) NEEDS_OWNER · Defer | A |

Deferred without asking (low): F22.

## spec-analyze verify pass
No question asked. Skill step 5: verify findings go to `## Open Questions` and are listed to the user, not applied.
Listed: F24 (idempotency in-progress/mismatch), F25 (double redemption on one Cart), F26 (manual-refund record).

## spec-new

### Q1 — step 1: `docs/specs/gift-cards/` exists
Options: Resume | New name → Answer: Resume (scripted). `SPEC drift` → NO DRIFT. First phase not approved: `design`.

### Q2 — gate design
Shown: `design.md: 8 components, 10 properties`. Options: Approve | Request changes → Answer: Approve (scripted). `SPEC approve design` → APPROVED.

### Q3 — gate tasks
`check-tasks` → RESULT: PASS (21 checks). Shown: `tasks.md: 11 leaves, 5 waves`. Options: Approve | Request changes → Answer: Approve (scripted). `SPEC approve tasks` → APPROVED.
Then told user: `/sdd:spec-run gift-cards`.

## spec-run
Mode `waves` from `--mode`; no question. `--optional` → `*` leaves in scope.

### Q4 — wave 0, leaf 1.1 has no report block
Runner hand-back text was only `placeholder` (no TASK/STATUS). File `shop/giftcards.py` exists and the leaf Verify passes when run by the orchestrator. Skill only marks `done` → `[x]`, so I treat it as `failed`.
Options: Retry | Skip | Stop → Answer: Retry (scripted: "failed leaf → Retry once"). Tier up: sonnet → opus.

### spec-run end
No red checkpoint. No counterexample. No further questions.

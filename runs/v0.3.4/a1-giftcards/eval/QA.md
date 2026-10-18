# QA log (plugin 0.3.4)

## spec-analyze round 1

Repairs (see `check-audit.md`): F1 B narrowed; F6 split into F6a/F6b (one option each → A | Defer); F8 A extra assertion dropped at apply. No low findings.

### Call 1 — Requirement 1
| Q | Options | Answer | Source |
|---|---|---|---|
| F6a (high, FAILURE): Payment_Provider declines | A) 1.3 402 `payment_declined`, no Gift_Card · Defer | A | Script: high/medium → A |
| F6b (high, FAILURE): Payment_Provider fails for another reason | A) 1.x IF charge fails for a reason other than a decline → 502 `payment_failed`, no Gift_Card · Defer | A | Script |
| F7 (medium, EDGE): value outside 10–500 or not whole | A) 1.4 400 `invalid_amount`, charge nothing · B) 1.4 outside 1000–50000 cents · Defer | A | Script |

### Call 2 — Requirement 2
| Q | Options | Answer | Source |
|---|---|---|---|
| F2 (medium, AMBIGUITY): "promptly" | A) 2.2 within 2 seconds · B) 95% within 500 ms · Defer | A | Script |
| F3 (high, EDGE): subtotal > balance | A) 2.5 409 `insufficient_balance`, balance unchanged · B) 2.5 balance → 0, `remaining_cents` · Defer | A | Script |
| F4 (medium, CONFLICT): 1000 vs 500 limit | A) 2.3 balance > 1000 dollars → 422 `balance_too_high` · B) 2.3 redeem 0.01–500 · Defer | A | Script |
| F9 (medium, EDGE): concurrent redemptions | A) 2.6 one at a time, never below 0 · B) 2.6 409 `card_busy` · Defer | A | Script |

### Call 3 — Requirements 3, 4, 5
| Q | Options | Answer | Source |
|---|---|---|---|
| F5 (medium, NEEDS_OWNER): What is the Merchant_Portal? Shop_API method + path that voids a card, and how the Shop_API identifies the staff actor? | owner answer · Defer | Most conservative concrete value: Merchant_Portal = staff web UI outside this repo; it calls `POST /gift-cards/<code>/void` on the Shop_API. Staff actor = `ctx["actor"]` with `role == "staff"`; anything else (missing actor included) is not staff and may not void. | Script: NEEDS_OWNER → conservative value (logged) |
| F1 (high, INCONSISTENCY): never expire vs 12-month void | A) 4.1 keep `active` until staff voids or balance reaches 0; delete 4.2 · B) 4.1 void balance unchanged (narrowed) · Defer | A | Script |
| F8 (medium, CONFLICT): ledger fails after charge | A) 5.3 refund the charge (+ create no Gift_Card) · B) 5.3 ledger before charge · Defer | A | Script |

### Cross-check findings (step 4 → back to step 3 before round 2)
| Q | Options | Answer | Source |
|---|---|---|---|
| F10 (high, INCONSISTENCY, orchestrator cross-check): 2.1 subtracts any subtotal; 2.5 rejects subtotal > balance | A) 2.1: WHEN a shopper applies an `active` Gift_Card code to a Cart whose subtotal is at most the Gift_Card balance, THE Shop_API SHALL subtract the Cart subtotal from the Gift_Card balance. · Defer | A | Script: high → A |
| F11 (medium, INCONSISTENCY, orchestrator cross-check): 4.1 "until … the balance reaches 0" ends `active` with no other status | A) 4.1: THE Shop_API SHALL keep a Gift_Card `active` with its balance until a staff member voids it under 3.1. · Defer | A | Script: medium → A |

## spec-analyze round 2

Repairs: F13 asks two questions (two gaps) → split F13a / F13b.

### Call 4 — Requirement 5
| Q | Options | Answer | Source |
|---|---|---|---|
| F12 (medium, NEEDS_OWNER): HTTP status and error when the 5.3 refund fails? | owner answer · Defer | Most conservative concrete value: HTTP 503, error `refund_failed`. | Script: NEEDS_OWNER → conservative (logged) |
| F13a (medium, NEEDS_OWNER): missing `ctx["actor"]` on a change request — reject (status, error) or fixed actor id? | owner answer · Defer | Most conservative concrete value: reject, HTTP 401, error `actor_required`, change nothing. | Script (logged) |
| F13b (medium, NEEDS_OWNER): ledger "old value" on creation? | owner answer · Defer | Most conservative concrete value: `null` (JSON) / `None` (Python). | Script (logged) |

### Cross-check findings (round 2 apply)
| Q | Options | Answer | Source |
|---|---|---|---|
| F14 (medium, INCONSISTENCY, cross-check): 5.2 vs 5.4 error code when the ledger and the refund both fail | A) 5.4: IF the refund in 5.3 fails, THEN THE Shop_API SHALL return HTTP 503 with error `refund_failed` instead of `ledger_unavailable`. · Defer | A | Script |
| F15 (high, INCONSISTENCY, cross-check): void with no actor: 3.3 gives 403, 5.5 gives 401 | A) 5.5: IF a purchase or redemption request has no `ctx["actor"]`, THEN THE Shop_API SHALL return HTTP 401 with error `actor_required` and change nothing. · Defer | A | Script |

## spec-analyze round 3
| Q | Options | Answer | Source |
|---|---|---|---|
| F16 (medium, INCONSISTENCY): 4.1 "with its balance" vs 2.1 redemption | A) 4.1 active until staff void, no expiry (trailing clause dropped, see check-audit) · Defer | A | Script |

## spec-analyze VERIFY 1 (one Resolve + Apply)
| Q | Options | Answer | Source |
|---|---|---|---|
| F18 (medium, INCONSISTENCY): void card + subtotal > balance: `card_void` or `insufficient_balance`? | A) 3.2 `card_void` whatever the subtotal · B) 2.5 only for `active` cards · Defer | A | Script |
| F17 (medium, CONFLICT): no actor + bad amount/code: which error wins? | A) 5.5 401 before any other check · B) 5.5 401 only after checks pass · Defer | A | Script |

## spec-new (resume)
| Q | Options | Answer | Source |
|---|---|---|---|
| `docs/specs/gift-cards/` exists. Resume or new name? | Resume · New name | Resume | Script |

Resume: `SPEC drift` → NO DRIFT; first phase not approved = `design`.

### Gate — design
Shown: `design.md: 4 components, 12 properties` (analyze ran: criteria 12 → 20).

| Q | Options | Answer | Source |
|---|---|---|---|
| Approve design? | Approve · Request changes | Approve | Script |

### Gate — tasks
`check-tasks` RESULT: PASS (1 WARN: checkpoint 4 shares a wave with later-layer leaf 5.1). Shown: `tasks.md: 5 leaves, 4 waves`.

| Q | Options | Answer | Source |
|---|---|---|---|
| Approve tasks? | Approve · Request changes | Approve | Script |

Then told user: `/sdd:spec-run gift-cards`.


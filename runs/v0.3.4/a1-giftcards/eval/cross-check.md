# Cross-check of changed criteria (M4, spec-analyze step 4)

Each changed criterion vs every criterion that shares a term with it.

## Round 1 apply
| Changed | Compared with (shared term) | Clash? | Note |
|---|---|---|---|
| 1.3 decline → 402 | 1.1, 1.5 (Payment_Provider, charge) | no | 1.5 excludes decline |
| 1.4 invalid_amount | 1.1 (10–500 dollars) | no | same range |
| 1.5 other failure → 502 | 1.1, 1.3, 5.3 | no | |
| 2.2 within 2 s | 2.1 (redemption) | no | |
| 2.3 > 1000 → 422 | 1.1 (≤500), 2.5 (balance) | no clash | unreachable under 1.1, but both can hold. Noted only. |
| 2.5 subtotal > balance → 409, unchanged | **2.1** (subtotal, balance) | **yes → F10** | 2.1 subtracts for any subtotal; 2.5 leaves balance unchanged for the same input |
| 2.6 serialize | 2.1, 2.5 (balance) | no | |
| 3.3 non-staff → 403 | 3.1 (void, staff), Glossary Actor | no | |
| 4.1 active until void or balance 0 | **Glossary Gift_Card status (`active` \| `void`)**, 2.1, 2.5, 3.1 | **yes → F11** | at balance 0 the card stops being `active`, but no other status exists and 3.2/2.x do not say what a 0-balance card does |
| 4.2 removed | — | — | superseded by F1 A |
| 5.3 refund | 5.1, 5.2 (ledger write fails) | no | 5.2 already rejects the change |
| 2.1 (F10 A) | 2.5, 2.6 | no | second pass |
| 4.1 (F11 A) | 3.1, 3.2 | no | second pass |

## Round 2 apply
| Changed | Compared with (shared term) | Clash? | Note |
|---|---|---|---|
| Glossary Ledger_Entry | 5.1 | no | 5.1 lists the same fields |
| 5.4 refund fails → 503 `refund_failed` | **5.2** (ledger write fails → 503 `ledger_unavailable`), 5.3 | **yes → F14** | same input (ledger fail + refund fail) gives two error codes |
| 5.5 no actor → 401 `actor_required` | **3.3** + Glossary Actor (missing actor is not staff → 403 `forbidden`) | **yes → F15** | void with no actor: 401 vs 403 |
| 5.5 | 1.4, 2.4, 2.5 (other rejections) | no clash | order of checks is a design choice; noted |
| 5.4 (F14 A) | 5.2 | no | second pass |
| 5.5 (F15 A) | 3.3, Glossary Actor | no | second pass: void keeps 403 |

Miss: round-1 cross-check of 4.1 vs 2.1 said "no". Round 3 analyst found the clash (F16). The orchestrator compared status, not balance.

## Round 3 apply
| Changed | Compared with | Clash? | Note |
|---|---|---|---|
| 4.1 (F16 A) | 2.1, 2.5, 3.1, 3.2 | no | balance not named any more |

## VERIFY 1 apply
| Changed | Compared with | Clash? | Note |
|---|---|---|---|
| 3.2 (F18 A) | 2.5, 2.1, 3.3 | no | 3.2 now states it wins |
| 5.5 (F17 A) | 1.4, 2.4, 2.5, 3.3 | no | 5.5 states it runs first; 3.3 (void) out of 5.5 scope |

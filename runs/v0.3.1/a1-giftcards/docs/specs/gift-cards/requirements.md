# Requirements Document

## Introduction

Gift cards for mockshop. Shoppers buy gift cards and redeem them at checkout. Staff can void cards.

## Glossary

- **Shop_API**: the `handle(request, ctx)` entry point in `shop/api.py`.
- **Gift_Card**: a record with a 16-character code, a balance in cents, and a status (`active` | `void`).
- **Cart**: a shopper's open cart with lines and a subtotal in cents.
- **Payment_Provider**: the external card payment service.
- **Actor**: the request field `actor` = `{"id", "role"}` that names the caller; `role` is `shopper` or `staff`.

## Requirements

### Requirement 1: Buy a gift card

**User Story:** As a shopper, I want to buy a gift card, so that I can give store credit.

#### Acceptance Criteria

1. WHEN a shopper buys a Gift_Card with a value of 10–500 dollars, THE Shop_API SHALL charge the Payment_Provider and create an `active` Gift_Card with that balance.
2. WHEN a Gift_Card is created, THE Shop_API SHALL return its 16-character code.
3. IF the Payment_Provider charge fails, THEN THE Shop_API SHALL return HTTP 402 with error `payment_failed` and create no Gift_Card.

### Requirement 2: Redeem a gift card

**User Story:** As a shopper, I want to pay with a gift card, so that I can use my credit.

#### Acceptance Criteria

1. WHEN a shopper applies an `active` Gift_Card code to a Cart, THE Shop_API SHALL subtract the Cart subtotal from the Gift_Card balance.
2. THE Shop_API SHALL return the redemption response within 2 seconds for 95% of requests.
3. IF the code does not match any Gift_Card, THEN THE Shop_API SHALL return HTTP 404 with error `unknown_card`.
4. IF the Cart subtotal exceeds the Gift_Card balance, THEN THE Shop_API SHALL reject the redemption with HTTP 422 and error `insufficient_balance`, leaving the balance unchanged.
5. WHEN two redemptions of one Gift_Card run at the same time, THE Shop_API SHALL apply them one after the other so the final balance is never below 0 cents.

### Requirement 3: Void a gift card

**User Story:** As a staff member, I want to void a gift card, so that lost or stolen cards cannot be used.

#### Acceptance Criteria

1. WHEN an Actor with role `staff` sends `POST /gift-cards/<code>/void`, THE Shop_API SHALL set the Gift_Card status to `void`.
2. WHILE a Gift_Card is `void`, THE Shop_API SHALL reject redemption with HTTP 409 and error `card_void`.
3. IF a void request comes from an Actor whose role is not `staff`, THEN THE Shop_API SHALL return HTTP 403 with error `forbidden` and leave the Gift_Card status unchanged.
4. IF a redemption request targets a `void` Gift_Card, THEN THE Shop_API SHALL return HTTP 409 with error `card_void` before any balance check, even when the Cart subtotal exceeds the balance.

### Requirement 4: Expiry

**User Story:** As a shopper, I want my gift card to keep its value, so that I can use it later.

#### Acceptance Criteria

1. THE Shop_API SHALL keep Gift_Card balances forever; Gift_Cards never expire.
2. WHEN a Gift_Card is unused for 12 months, THE Shop_API SHALL keep its status `active`.

### Requirement 5: Audit

**User Story:** As a finance officer, I want a ledger of gift card changes, so that I can reconcile balances.

#### Acceptance Criteria

1. WHEN a Gift_Card balance or status changes, THE Shop_API SHALL append a ledger entry with the code, old value, new value, actor id, and UTC timestamp.
2. IF the ledger write fails, THEN THE Shop_API SHALL reject the change with HTTP 503 and error `ledger_unavailable`.
3. IF the ledger write fails during gift card purchase after a successful charge, THEN THE Shop_API SHALL refund the charge through the Payment_Provider and create no Gift_Card.

## Open Questions

- F8 · EDGE · low — Actor id for system changes (no human actor) and old value at card creation are undefined in 5.1.
- F11 · FAILURE · medium (verify) — 5.3 gives no HTTP response and no rule for a failed refund. Candidate: 5.4 return HTTP 503 `refund_failed`, no Gift_Card.
- F12 · EDGE · medium (verify) — void of an unknown code has no result; 403 vs 404 order unclear. Candidate: 3.5 staff + unknown code → HTTP 404 `unknown_card`.
- F13 · EDGE · low (verify) — void request with no `actor` field or unknown `role`. Candidate: treat as non-staff → HTTP 403 `forbidden`.

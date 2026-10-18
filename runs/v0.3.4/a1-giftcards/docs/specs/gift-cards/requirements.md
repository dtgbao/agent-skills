# Requirements Document

## Introduction

Gift cards for mockshop. Shoppers buy gift cards and redeem them at checkout. Staff can void cards.

## Glossary

- **Shop_API**: the `handle(request, ctx)` entry point in `shop/api.py`.
- **Gift_Card**: a record with a 16-character code, a balance in cents, and a status (`active` | `void`).
- **Cart**: a shopper's open cart with lines and a subtotal in cents.
- **Payment_Provider**: the external card payment service.
- **Merchant_Portal**: the staff web UI outside this repo. It voids a Gift_Card through the Shop_API route `POST /gift-cards/<code>/void`.
- **Actor**: the caller, given in `ctx["actor"]` as `{"id": str, "role": "shopper" | "staff"}`. A missing `ctx["actor"]` is not staff.
- **Ledger_Entry**: one ledger record `{code, old, new, actor_id, at}`; `old` is `null` when the entry records Gift_Card creation; `at` is a UTC timestamp.

## Requirements

### Requirement 1: Buy a gift card

**User Story:** As a shopper, I want to buy a gift card, so that I can give store credit.

#### Acceptance Criteria

1. WHEN a shopper buys a Gift_Card with a value of 10–500 dollars, THE Shop_API SHALL charge the Payment_Provider and create an `active` Gift_Card with that balance.
2. WHEN a Gift_Card is created, THE Shop_API SHALL return its 16-character code.
3. IF the Payment_Provider declines the charge, THEN THE Shop_API SHALL return HTTP 402 with error `payment_declined` and create no Gift_Card.
4. IF the purchase value is outside 10–500 dollars or not a whole number of dollars, THEN THE Shop_API SHALL return HTTP 400 with error `invalid_amount` and charge nothing.
5. IF the Payment_Provider charge fails for a reason other than a decline, THEN THE Shop_API SHALL return HTTP 502 with error `payment_failed` and create no Gift_Card.

### Requirement 2: Redeem a gift card

**User Story:** As a shopper, I want to pay with a gift card, so that I can use my credit.

#### Acceptance Criteria

1. WHEN a shopper applies an `active` Gift_Card code to a Cart whose subtotal is at most the Gift_Card balance, THE Shop_API SHALL subtract the Cart subtotal from the Gift_Card balance.
2. THE Shop_API SHALL return the response to a redemption request within 2 seconds.
3. IF a Gift_Card balance exceeds 1000 dollars, THEN THE Shop_API SHALL reject redemption with HTTP 422 and error `balance_too_high`.
4. IF the code does not match any Gift_Card, THEN THE Shop_API SHALL return HTTP 404 with error `unknown_card`.
5. IF the Cart subtotal exceeds the Gift_Card balance, THEN THE Shop_API SHALL return HTTP 409 with error `insufficient_balance` and leave the balance unchanged.
6. WHEN two redemptions of one Gift_Card run concurrently, THE Shop_API SHALL apply them one at a time so the balance never goes below 0.

### Requirement 3: Void a gift card

**User Story:** As a staff member, I want to void a gift card, so that lost or stolen cards cannot be used.

#### Acceptance Criteria

1. WHEN a staff member voids a Gift_Card through the Merchant_Portal, THE Shop_API SHALL set the Gift_Card status to `void`.
2. WHILE a Gift_Card is `void`, THE Shop_API SHALL reject redemption with HTTP 409 and error `card_void`, whatever the Cart subtotal.
3. IF a void request comes from an Actor that is not staff, THEN THE Shop_API SHALL return HTTP 403 with error `forbidden` and leave the Gift_Card status unchanged.

### Requirement 4: Expiry

**User Story:** As a shopper, I want my gift card to keep its value, so that I can use it later.

#### Acceptance Criteria

1. THE Shop_API SHALL keep a Gift_Card `active`, with no expiry date, until a staff member voids it under 3.1.

### Requirement 5: Audit

**User Story:** As a finance officer, I want a ledger of gift card changes, so that I can reconcile balances.

#### Acceptance Criteria

1. WHEN a Gift_Card balance or status changes, THE Shop_API SHALL append a ledger entry with the code, old value, new value, actor id, and UTC timestamp.
2. IF the ledger write fails, THEN THE Shop_API SHALL reject the change with HTTP 503 and error `ledger_unavailable`.
3. IF the ledger write fails after a Payment_Provider charge, THEN THE Shop_API SHALL refund the charge.
4. IF the refund in 5.3 fails, THEN THE Shop_API SHALL return HTTP 503 with error `refund_failed` instead of `ledger_unavailable`.
5. IF a purchase or redemption request has no `ctx["actor"]`, THEN THE Shop_API SHALL return HTTP 401 with error `actor_required` before any amount, code or balance check, and change nothing.

## Open Questions

- F19 (CONFLICT, medium): a `void` Gift_Card with a balance over 1000 dollars matches 2.3 (422 `balance_too_high`) and 3.2 (409 `card_void`). Left after the last VERIFY pass. Options: A) 3.2 wins whatever the balance; B) 2.3 wins even when `void`.
- F20 (INCONSISTENCY, medium): 5.5 lists amount, code and balance checks but not the `void` status check, so no actor + `void` card can give 401 or 409. Left after the last VERIFY pass. Options: A) 401 before any check, `void` included; B) 401 after the `void` check.

# Requirements Document

## Introduction

Gift cards for mockshop. Shoppers buy gift cards and redeem them at checkout. Staff can void cards.

## Glossary

- **Shop_API**: the `handle(request, ctx)` entry point in `shop/api.py`.
- **Gift_Card**: a record with a 16-character code, a balance in cents, and a status (`active` | `void`).
- **Cart**: a shopper's open cart with lines and a subtotal in cents.
- **Payment_Provider**: the external card payment service.
- **Merchant_Portal**: the staff web app that calls Shop_API with a staff actor id.

## Requirements

### Requirement 1: Buy a gift card

**User Story:** As a shopper, I want to buy a gift card, so that I can give store credit.

#### Acceptance Criteria

1. WHEN a shopper buys a Gift_Card with a whole-dollar value from 10 to 500 dollars inclusive, THE Shop_API SHALL charge the Payment_Provider that value.
2. WHEN a Gift_Card is created, THE Shop_API SHALL return its 16-character code.
3. IF the Payment_Provider declines the charge or does not respond within 10 seconds, THEN THE Shop_API SHALL return HTTP 402 with error `payment_failed`.
4. IF the Payment_Provider declines the charge or does not respond within 10 seconds, THEN THE Shop_API SHALL create no Gift_Card.
5. WHEN the Payment_Provider charge for a Gift_Card purchase succeeds, THE Shop_API SHALL create an `active` Gift_Card with a balance equal to the charged value.
6. IF the Payment_Provider does not respond within 10 seconds, THEN THE Shop_API SHALL cancel or refund any charge that the Payment_Provider later confirms for that purchase.
7. IF the purchase value is not a whole-dollar value from 10 to 500 dollars inclusive, THEN THE Shop_API SHALL return HTTP 422 with error `invalid_request`.
8. IF the purchase value is not a whole-dollar value from 10 to 500 dollars inclusive, THEN THE Shop_API SHALL not charge the Payment_Provider.
9. WHEN the Shop_API receives a purchase request with an idempotency key that it already processed, THE Shop_API SHALL return the first result.
10. WHEN the Shop_API receives a purchase request with an idempotency key that it already processed, THE Shop_API SHALL not charge the Payment_Provider again.

### Requirement 2: Redeem a gift card

**User Story:** As a shopper, I want to pay with a gift card, so that I can use my credit.

#### Acceptance Criteria

1. WHEN a shopper applies an `active` Gift_Card code to a Cart with a subtotal not above the Gift_Card balance, THE Shop_API SHALL subtract the Cart subtotal from the Gift_Card balance.
2. THE Shop_API SHALL respond to a redemption request within 2 seconds for 95 percent of requests.
3. THE Shop_API SHALL accept Gift_Cards with a balance up to 500 dollars.
4. IF the code is 16 characters and does not match any Gift_Card, THEN THE Shop_API SHALL return HTTP 404 with error `unknown_card`.
5. WHEN the Cart subtotal exceeds the Gift_Card balance, THE Shop_API SHALL set the Gift_Card balance to 0.
6. WHEN the Cart subtotal exceeds the Gift_Card balance, THE Shop_API SHALL return the remaining amount due in cents.
7. THE Shop_API SHALL apply concurrent redemptions and voids on one Gift_Card in sequence, so that the balance never falls below 0.
8. IF the code is not 16 characters or the Cart is not open, THEN THE Shop_API SHALL return HTTP 422 with error `invalid_request`.
9. THE Shop_API SHALL check redemption requests in this order: `invalid_request` (422), `unknown_card` (404), `card_void` (409), and return the first error that applies.

### Requirement 3: Void a gift card

**User Story:** As a staff member, I want to void a gift card, so that lost or stolen cards cannot be used.

#### Acceptance Criteria

1. WHEN a staff member voids a Gift_Card through the Merchant_Portal, THE Shop_API SHALL set the Gift_Card status to `void`.
2. WHILE a Gift_Card is `void`, THE Shop_API SHALL reject redemption with HTTP 409 and error `card_void`.
3. IF a void request has no staff actor id or the actor id does not belong to a staff member, THEN THE Shop_API SHALL return HTTP 403 with error `forbidden`.
4. IF a void request has no staff actor id or the actor id does not belong to a staff member, THEN THE Shop_API SHALL not change the Gift_Card.

### Requirement 4: Expiry

**User Story:** As a shopper, I want my gift card to keep its value, so that I can use it later.

#### Acceptance Criteria

1. THE Shop_API SHALL keep Gift_Card balances forever; Gift_Cards never expire.

### Requirement 5: Audit

**User Story:** As a finance officer, I want a ledger of gift card changes, so that I can reconcile balances.

#### Acceptance Criteria

1. WHEN a Gift_Card balance or status changes, THE Shop_API SHALL append a ledger entry with the code, old value, new value, actor id, and UTC timestamp.
2. IF the ledger write fails, THEN THE Shop_API SHALL reject the change with HTTP 503 and error `ledger_unavailable`.
3. IF the ledger write for a new Gift_Card fails after the Payment_Provider charge, THEN THE Shop_API SHALL refund the charge.
4. IF the refund of a charge fails, THEN THE Shop_API SHALL record the charge for manual refund.

## Open Questions

| ID | Type | Severity | Affects | Question |
|---|---|---|---|---|
| F11 | EDGE | low | 3.1 | Voiding an already `void` or unknown card is not defined. Balance after void is not defined. |
| F12 | ASSUMPTION | low | 5.1 | "ledger" and "actor id" are not in the Glossary. Actor for system changes is not defined. |
| F13 | AMBIGUITY | low | 4.2 (deleted) | Start of the 12-month period. Moot: 4.2 deleted by F1 option A. |
| F22 | EDGE | low | 5.1, 1.5 | Old value and actor id in the ledger entry for card creation and shopper redemption. |
| F24 | EDGE | medium | 1.9, 1.10 | Duplicate idempotency key while the first request runs, or with a different value. Key retention and Glossary entry. (verify) |
| F25 | EDGE | medium | 2.1, 2.5, 2.7 | Repeated redemption on the same Cart can subtract twice. One or several Gift_Cards per Cart. (verify) |
| F26 | FAILURE | medium | 5.3, 5.4, 1.6 | Manual-refund record place, data, and HTTP response. Cancel vs refund in 1.6. (verify) |

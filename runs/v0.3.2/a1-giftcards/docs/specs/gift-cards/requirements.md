# Requirements Document

## Introduction

Gift cards for mockshop. Shoppers buy gift cards and redeem them at checkout. Staff can void cards.

## Glossary

- **Shop_API**: the `handle(request, ctx)` entry point in `shop/api.py`.
- **Gift_Card**: a record with a 16-character code, a balance in cents, and a status (`active` | `void`).
- **Cart**: a shopper's open cart with lines and a subtotal in cents.
- **Payment_Provider**: the external card payment service, given as `ctx["payments"]` with `charge(amount_cents) -> charge_id` and `refund(charge_id)`.
- **Merchant_Portal**: the staff client that sends void requests to the Shop_API as `POST /gift-cards/{code}/void`.
- **Actor**: the caller of a request, given as `ctx["actor"]` = `{"id": str, "role": "shopper" | "staff"}`. The actor id is `ctx["actor"]["id"]`.
- **Ledger**: the append-only list of Gift_Card change entries at `ctx["ledger"]`.

## Requirements

### Requirement 1: Buy a gift card

**User Story:** As a shopper, I want to buy a gift card, so that I can give store credit.

#### Acceptance Criteria

1. WHEN a shopper buys a Gift_Card with a value of 10–500 dollars, THE Shop_API SHALL charge the Payment_Provider and create an `active` Gift_Card with that balance.
2. WHEN a Gift_Card is created, THE Shop_API SHALL return its 16-character code.
3. IF the Payment_Provider charge fails, THEN THE Shop_API SHALL return HTTP 402 with error `payment_failed`.
4. IF the Payment_Provider charge fails, THEN THE Shop_API SHALL create no Gift_Card.
5. IF a shopper buys a Gift_Card with a value outside 10–500 dollars, THEN THE Shop_API SHALL return HTTP 400 with error `bad_value`.
6. IF a shopper buys a Gift_Card with a value outside 10–500 dollars, THEN THE Shop_API SHALL not charge the Payment_Provider.
7. IF the Ledger write fails after the Payment_Provider charge for a new Gift_Card, THEN THE Shop_API SHALL refund that charge through the Payment_Provider.
8. IF the Payment_Provider refund fails after a Ledger write failure for a new Gift_Card, THEN THE Shop_API SHALL return HTTP 503 with error `refund_failed`.

### Requirement 2: Redeem a gift card

**User Story:** As a shopper, I want to pay with a gift card, so that I can use my credit.

#### Acceptance Criteria

1. WHEN a shopper applies an `active` Gift_Card code to a Cart, THE Shop_API SHALL subtract the Cart subtotal from the Gift_Card balance.
2. THE Shop_API SHALL return the response to a redemption request within 2 seconds for 95% of requests.
3. IF a Gift_Card balance is above 1000 dollars, THEN THE Shop_API SHALL reject redemption with HTTP 422 and error `balance_too_high`.
4. IF the code does not match any Gift_Card, THEN THE Shop_API SHALL return HTTP 404 with error `unknown_card`.
5. IF the Cart subtotal is greater than the Gift_Card balance, THEN THE Shop_API SHALL return HTTP 422 with error `insufficient_balance`.
6. IF the Cart subtotal is greater than the Gift_Card balance, THEN THE Shop_API SHALL leave the Gift_Card balance unchanged.
7. WHILE a Gift_Card balance is above 1000 dollars, WHEN the Cart subtotal is greater than the balance, THE Shop_API SHALL return HTTP 422 with error `balance_too_high`.

### Requirement 3: Void a gift card

**User Story:** As a staff member, I want to void a gift card, so that lost or stolen cards cannot be used.

#### Acceptance Criteria

1. WHEN a staff member voids a Gift_Card through the Merchant_Portal, THE Shop_API SHALL set the Gift_Card status to `void`.
2. WHILE a Gift_Card is `void`, THE Shop_API SHALL reject redemption with HTTP 409 and error `card_void`.
3. IF a void request code does not match any Gift_Card, THEN THE Shop_API SHALL return HTTP 404 with error `unknown_card`.
4. WHEN a staff member voids a Gift_Card that is already `void`, THE Shop_API SHALL return HTTP 200.
5. IF a void request comes from an Actor whose role is not `staff`, THEN THE Shop_API SHALL return HTTP 403 with error `forbidden`.
6. IF a void request comes from an Actor whose role is not `staff` and the code matches no Gift_Card, THEN THE Shop_API SHALL return HTTP 403 with error `forbidden`.
7. WHILE a Gift_Card is `void`, WHEN a redemption also meets the condition of 2.3 or 2.5, THE Shop_API SHALL return HTTP 409 with error `card_void`.

### Requirement 4: Expiry

**User Story:** As a shopper, I want my gift card to keep its value, so that I can use it later.

#### Acceptance Criteria

1. THE Shop_API SHALL keep Gift_Card balances forever; Gift_Cards never expire.
2. WHEN an `active` Gift_Card has had no redemption for 12 months, THE Shop_API SHALL keep its status `active`.

### Requirement 5: Audit

**User Story:** As a finance officer, I want a ledger of gift card changes, so that I can reconcile balances.

#### Acceptance Criteria

1. WHEN a Gift_Card balance or status changes, THE Shop_API SHALL append a Ledger entry with the code, old value, new value, actor id, and UTC timestamp.
2. IF the Ledger write fails, THEN THE Shop_API SHALL reject the change with HTTP 503 and error `ledger_unavailable`.
3. WHEN a Gift_Card is created, THE Shop_API SHALL write old value `null` in its Ledger entry.

## Open Questions

- F17 · AMBIGUITY · low · Requirement 2.2: no load condition or measurement window, so a test cannot fail on it. Proposed: "WHILE the Shop_API serves up to 10 redemption requests per second, THE Shop_API SHALL return 95% of redemption responses within 2 seconds, measured over 1000 requests."

# Requirements Document

## Introduction

Gift cards for mockshop. Shoppers buy gift cards and redeem them at checkout. Staff can void cards.

## Glossary

- **Shop_API**: the `handle(request, ctx)` entry point in `shop/api.py`.
- **Gift_Card**: a record with a 16-character code, a balance in cents, and a status (`active` | `void`).
- **Cart**: a shopper's open cart with lines and a subtotal in cents.
- **Payment_Provider**: the external card payment service, reached as `ctx["payment_provider"]`: `charge(amount_cents, charge_ref)` takes a `charge_ref` that the Shop_API makes before the charge; `refund(charge_ref)` undoes that charge and raises an exception on failure.
- **Actor**: the caller, given as `ctx["actor"] = {"id": str, "role": "shopper" | "staff"}`. A missing `ctx["actor"]` is not `staff`.
- **Error_Log**: the Python `logging` logger named `shop.gift_cards`, level `ERROR`.

## Requirements

### Requirement 1: Buy a gift card

**User Story:** As a shopper, I want to buy a gift card, so that I can give store credit.

#### Acceptance Criteria

1. WHEN a shopper buys a Gift_Card with a value of 10–500 dollars, THE Shop_API SHALL charge the Payment_Provider and create an `active` Gift_Card with that balance.
2. WHEN a Gift_Card is created, THE Shop_API SHALL return its 16-character code.
3. IF the Payment_Provider declines the charge or returns an error, THEN THE Shop_API SHALL return HTTP 402 with error `payment_failed` and create no Gift_Card.
4. IF the purchase value is outside 10–500 dollars or not a whole number of dollars, THEN THE Shop_API SHALL return HTTP 400 with error `invalid_amount` and not charge the Payment_Provider.
5. IF the Payment_Provider does not answer within 10 seconds, THEN THE Shop_API SHALL return HTTP 504 with error `payment_timeout` and create no Gift_Card.
6. IF the Payment_Provider does not answer within 10 seconds, THEN THE Shop_API SHALL call `ctx["payment_provider"].refund(charge_ref)` with the `charge_ref` it sent.

### Requirement 2: Redeem a gift card

**User Story:** As a shopper, I want to pay with a gift card, so that I can use my credit.

#### Acceptance Criteria

1. WHEN a shopper applies an `active` Gift_Card code to a Cart whose subtotal is at most the Gift_Card balance, THE Shop_API SHALL subtract the Cart subtotal from the Gift_Card balance.
2. THE Shop_API SHALL respond to a redemption request within 2 seconds for 95% of requests.
3. THE Shop_API SHALL accept Gift_Cards with a balance up to 500 dollars.
4. IF the code does not match any Gift_Card, THEN THE Shop_API SHALL return HTTP 404 with error `unknown_card`.
5. IF the Cart subtotal exceeds the Gift_Card balance, THEN THE Shop_API SHALL set the balance to 0 cents and return the remaining amount due in cents.
6. WHEN two redemptions of one code run at the same time, THE Shop_API SHALL apply them one after the other so the balance never falls below 0 cents.

### Requirement 3: Void a gift card

**User Story:** As a staff member, I want to void a gift card, so that lost or stolen cards cannot be used.

#### Acceptance Criteria

1. WHEN a staff member sends `POST /gift-cards/<code>/void` to the Shop_API, THE Shop_API SHALL set the Gift_Card status to `void`.
2. WHILE a Gift_Card is `void`, THE Shop_API SHALL reject redemption with HTTP 409 and error `card_void`.
3. IF a void request comes from an Actor whose `ctx["actor"]["role"]` is not `staff`, THEN THE Shop_API SHALL return HTTP 403 with error `forbidden` and leave the Gift_Card status unchanged.
4. IF a staff member sends `POST /gift-cards/<code>/void` with a code that matches no Gift_Card, THEN THE Shop_API SHALL return HTTP 404 with error `unknown_card`.

### Requirement 4: Expiry

**User Story:** As a shopper, I want my gift card to keep its value, so that I can use it later.

#### Acceptance Criteria

1. THE Shop_API SHALL keep a Gift_Card balance unchanged except by redemption under 2.1 or 2.5.
2. WHEN a Gift_Card is unused for 12 months, THE Shop_API SHALL set its status to `void`.

### Requirement 5: Audit

**User Story:** As a finance officer, I want a ledger of gift card changes, so that I can reconcile balances.

#### Acceptance Criteria

1. WHEN a Gift_Card balance or status changes, THE Shop_API SHALL append a ledger entry with the code, old value, new value, actor id, and UTC timestamp.
2. IF the ledger write fails, THEN THE Shop_API SHALL reject the change with HTTP 503 and error `ledger_unavailable`.
3. IF the ledger write fails during Gift_Card creation, THEN THE Shop_API SHALL refund the charge through `ctx["payment_provider"].refund(charge_ref)`.
4. IF `refund(charge_ref)` raises an exception during 5.3, THEN THE Shop_API SHALL return HTTP 503 with error `refund_failed` instead of `ledger_unavailable`.
5. IF `refund(charge_ref)` raises an exception during 5.3, THEN THE Shop_API SHALL write the `charge_ref` to the Error_Log.

## Open Questions

- F9 (EDGE, low): Ledger actor id and old value are not defined for changes with no user actor (12-month void in 4.2, card creation in 1.1). Proposed: 5.6 WHEN a change has no user actor, THE Shop_API SHALL write the actor id `system` in the ledger entry.
- F17 (FAILURE, medium): `refund(charge_ref)` can raise during 1.6 (timeout refund); no response or log is given. Left after the last VERIFY pass. Options: A) 1.7 write `charge_ref` to the Error_Log and still return HTTP 504 `payment_timeout`; B) 1.7 return HTTP 503 `refund_failed` and write `charge_ref` to the Error_Log.

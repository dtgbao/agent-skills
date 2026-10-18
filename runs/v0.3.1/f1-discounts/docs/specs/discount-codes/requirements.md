# Requirements Document

## Introduction

Discount codes let a shopper reduce a cart's subtotal. An operator defines codes. Each code gives a percent off or a fixed amount in cents off, may need a minimum subtotal, and has an expiry date. A shopper applies one code to a cart through the API. The cart reports the discount and the total after discount.

## Glossary

- **Discount_Code**: a record with a `code` string, a `Discount_Kind`, a `value`, a `min_subtotal_cents`, and an `expires_on` date.
- **Discount_Kind**: `percent` or `fixed`.
- **Code_Registry**: the store of Discount_Code records, keyed by `code`, held in `ctx["codes"]`.
- **Cart**: the existing `shop.cart.Cart`, with lines and `subtotal_cents()`.
- **Applied_Code**: the one Discount_Code a Cart holds, or none.
- **Subtotal**: `Cart.subtotal_cents()`, an integer in cents ≥ 0.
- **Discount_Amount**: integer cents taken off the Subtotal.
- **Total**: Subtotal minus Discount_Amount, integer cents.
- **Today**: the current date, given as `ctx["today"]` (a `datetime.date`).
- **API**: `shop.api.handle(request, ctx)`.

## Requirements

### Requirement 1: Define a discount code

**User Story:** As an operator, I want to define discount codes, so that shoppers can use them.

#### Acceptance Criteria

1. WHEN an operator creates a Discount_Code with a `code` of 1–20 characters from A–Z, 0–9 and `-`, THE Code_Registry SHALL store it under that `code`.
2. IF a Discount_Code has Discount_Kind `percent` and a `value` outside the integers 1–50, THEN THE Code_Registry SHALL reject it with `ValueError`.
3. IF a Discount_Code has Discount_Kind `fixed` and a `value` that is not an integer ≥ 1 cent, THEN THE Code_Registry SHALL reject it with `ValueError`.
4. IF a Discount_Code has a `min_subtotal_cents` that is not an integer ≥ 0, THEN THE Code_Registry SHALL reject it with `ValueError`.
5. IF a Discount_Code has a `code` that does not match the format in 1.1, THEN THE Code_Registry SHALL reject it with `ValueError`.
6. IF a Discount_Code has a `code` already in the Code_Registry, THEN THE Code_Registry SHALL reject it with `ValueError` and keep the existing record.

### Requirement 2: Apply a code to a cart

**User Story:** As a shopper, I want to apply a discount code to my cart, so that I pay less.

#### Acceptance Criteria

1. WHEN a shopper sends `POST /carts/<id>/code` with a known, unexpired `code` and the Subtotal ≥ its `min_subtotal_cents`, THE API SHALL set it as the Applied_Code and return status 200.
2. IF the `code` is not in the Code_Registry, THEN THE API SHALL return status 404 with error `unknown code`.
3. IF Today is after the code's `expires_on`, THEN THE API SHALL return status 410 with error `code expired`.
4. IF the Subtotal is below the code's `min_subtotal_cents`, THEN THE API SHALL return status 422 with error `minimum not met`.
5. IF the Cart already holds an Applied_Code, THEN THE API SHALL return status 409 with error `code already applied` and keep the existing Applied_Code.
6. IF a `POST /carts/<id>/code` request meets more than one of 5.2, 2.7, 2.2–2.5, THEN THE API SHALL return the status of the first met condition in the order 5.2, 2.7, 2.2, 2.3, 2.4, 2.5.
7. IF the `POST /carts/<id>/code` body has no `code` or a `code` that is not a string, THEN THE API SHALL return status 400 with error `bad code`.

### Requirement 3: Compute the discount

**User Story:** As a shopper, I want to see the discount and total, so that I know what I will pay.

#### Acceptance Criteria

1. WHILE a Cart holds a `percent` Applied_Code, THE Cart SHALL compute Discount_Amount as floor(Subtotal × `value` / 100) cents.
2. WHILE a Cart holds a `fixed` Applied_Code, THE Cart SHALL compute Discount_Amount as min(`value`, Subtotal) cents.
3. WHILE a Cart holds no Applied_Code, THE Cart SHALL compute Discount_Amount as 0 cents.
4. THE Cart SHALL compute Total as Subtotal minus Discount_Amount, and Total SHALL be in the range 0–Subtotal cents.
5. WHEN a shopper sends `GET /carts/<id>`, THE API SHALL return `discount_cents`, `total_cents`, and the Applied_Code `code` or null.

### Requirement 4: Keep the discount valid as the cart changes

**User Story:** As an operator, I want a code to stop working when its rules no longer hold, so that shoppers do not get discounts they do not qualify for.

#### Acceptance Criteria

1. IF the Subtotal falls below the Applied_Code's `min_subtotal_cents`, THEN THE Cart SHALL compute Discount_Amount as 0 cents.
2. IF Today is after the Applied_Code's `expires_on`, THEN THE Cart SHALL compute Discount_Amount as 0 cents.
3. WHILE a Cart holds an Applied_Code with Subtotal below its `min_subtotal_cents` or Today after its `expires_on`, THE Cart SHALL use the 0-cent Discount_Amount of 4.1–4.2 in place of 3.1–3.2.
4. THE Cart SHALL take Today only as a `today: datetime.date` argument to `Cart.discount_cents(today)` and `Cart.total_cents(today)`.

### Requirement 5: Remove a code

**User Story:** As a shopper, I want to remove the code from my cart, so that I can use another code.

#### Acceptance Criteria

1. WHEN a shopper sends `DELETE /carts/<id>/code`, THE API SHALL clear the Applied_Code and return status 200.
2. IF the cart id is unknown on any `/carts/<id>/code` request, THEN THE API SHALL return status 404 with error `no cart`.
3. WHEN a shopper sends `DELETE /carts/<id>/code` to a Cart with no Applied_Code, THE API SHALL return status 200 and leave the Cart unchanged.

## Open Questions

- F7 (EDGE, low, deferred): `expires_on` has no validation rule; a non-date value fails only when the code is applied.

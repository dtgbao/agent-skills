# Requirements Document

## Introduction

Discount codes let a shopper reduce the price of a cart. An operator defines each code with a percent or a fixed amount off, an optional minimum subtotal, and an expiry date. A shopper applies one code to a cart through the API, and the cart shows the discount and the total after the discount. A cart holds at most one code.

## Glossary

- **Discount_Code**: an operator-defined record with a Code_String, a Discount_Kind, a value, a Minimum_Subtotal, and an Expiry_Date.
- **Code_String**: the text a shopper enters; 1–20 characters from `A–Z`, `0–9`, and `-`.
- **Discount_Kind**: `percent` (integer 1–90, percent off the Subtotal) or `fixed` (integer ≥1, cents off the Subtotal).
- **Minimum_Subtotal**: integer cents ≥0 that the Subtotal must reach for the code to apply; 0 = no minimum.
- **Expiry_Date**: ISO 8601 calendar date (`YYYY-MM-DD`); the code is valid through the end of that date (UTC) and invalid after it.
- **Code_Registry**: the component that stores Discount_Codes and looks them up by Code_String; the Cart_API gets it from `ctx["codes"]`.
- **Cart**: the existing `shop.cart.Cart`; holds lines and at most one Applied_Code.
- **Applied_Code**: the Discount_Code currently attached to a Cart.
- **Subtotal**: sum of line price × quantity in cents (`Cart.subtotal_cents()`).
- **Discount_Amount**: cents taken off the Subtotal by the Applied_Code.
- **Total**: Subtotal − Discount_Amount, in cents.
- **Cart_API**: the existing `shop.api.handle(request, ctx)` entry point.
- **Clock**: a zero-argument callable that returns the current UTC date as `datetime.date`; the Cart_API gets it from `ctx["clock"]`.

## Requirements

### Requirement 1: Define discount codes

**User Story:** As an operator, I want to define discount codes, so that shoppers can get a set reduction.

#### Acceptance Criteria

1. WHEN an operator registers a Discount_Code with a valid Code_String, Discount_Kind, value, Minimum_Subtotal, and Expiry_Date, THE Code_Registry SHALL store it and return it on lookup by that Code_String.
2. IF a percent value is outside the integer range 1–90, THEN THE Code_Registry SHALL reject the registration with a validation error.
3. IF a fixed value is not an integer ≥1 cent, THEN THE Code_Registry SHALL reject the registration with a validation error.
4. IF the Code_String is empty, longer than 20 characters, or holds a character outside `A–Z`, `0–9`, `-`, THEN THE Code_Registry SHALL reject the registration with a validation error.
5. IF a Code_String is already registered, THEN THE Code_Registry SHALL reject the second registration with a duplicate error.
6. IF the Minimum_Subtotal is not an integer ≥0, THEN THE Code_Registry SHALL reject the registration with a validation error.
7. IF the Expiry_Date is not a real calendar date in `YYYY-MM-DD` form, THEN THE Code_Registry SHALL reject the registration with a validation error.
8. IF the Discount_Kind is not `percent` or `fixed`, THEN THE Code_Registry SHALL reject the registration with a validation error.

### Requirement 2: Apply a code to a cart

**User Story:** As a shopper, I want to apply a discount code to my cart, so that I pay less.

#### Acceptance Criteria

1. WHEN a shopper sends `POST /carts/<id>/discount` with a registered, unexpired Code_String and the Subtotal is at least the Minimum_Subtotal, THE Cart_API SHALL attach the code to the Cart and return status 200 with `subtotal_cents`, `discount_cents`, and `total_cents`.
2. IF the Code_String is not registered, THEN THE Cart_API SHALL return status 404 with error `unknown code`.
3. IF the Clock date is after the Expiry_Date, THEN THE Cart_API SHALL return status 410 with error `code expired`.
4. IF the Subtotal is below the Minimum_Subtotal, THEN THE Cart_API SHALL return status 422 with error `minimum not met`.
5. IF the request body has no `code` field or the field is not a string, THEN THE Cart_API SHALL return status 400 with error `bad code`.
6. IF the `code` field is a string that is not a valid Code_String, THEN THE Cart_API SHALL return status 400 with error `bad code`.
7. WHEN more than one error condition holds for `POST /carts/<id>/discount`, THE Cart_API SHALL return the error of the first failing check in this order: 400, 404, 410, 422, 409.
8. WHEN a shopper sends `POST` or `DELETE /carts/<id>/discount` for a cart id that does not exist, THE Cart_API SHALL return status 404 with error `no cart` before it runs any other check.

### Requirement 3: One code per cart

**User Story:** As a shop owner, I want each cart to hold at most one code, so that discounts do not stack.

#### Acceptance Criteria

1. WHILE a Cart has an Applied_Code, WHEN a shopper applies a different valid, registered, unexpired Code_String whose Minimum_Subtotal the Subtotal meets, THE Cart_API SHALL return status 409 with error `code already applied`.
2. WHILE a Cart has an Applied_Code, WHEN a shopper applies the same Code_String again and the code is unexpired and the Subtotal is at least the Minimum_Subtotal, THE Cart_API SHALL return status 200 with the current totals.
3. WHEN a shopper sends `DELETE /carts/<id>/discount`, THE Cart_API SHALL remove the Applied_Code and return status 200 with `discount_cents` equal to 0.
4. WHEN the Cart_API returns status 409 with error `code already applied`, THE Cart SHALL keep its Applied_Code unchanged.

### Requirement 4: Compute the discount

**User Story:** As a shopper, I want to see the correct discount, so that I know what I will pay.

#### Acceptance Criteria

1. WHERE the Applied_Code has Discount_Kind `percent`, THE Cart SHALL set Discount_Amount to floor(Subtotal × value ÷ 100) cents.
2. WHERE the Applied_Code has Discount_Kind `fixed`, THE Cart SHALL set Discount_Amount to the smaller of the value and the Subtotal.
3. THE Cart SHALL keep the Total in the range 0 to Subtotal cents.
4. WHEN a shopper sends `GET /carts/<id>`, THE Cart_API SHALL return `subtotal_cents`, `discount_cents`, `total_cents`, and the Applied_Code's Code_String or null.
5. WHILE a Cart has no Applied_Code, THE Cart SHALL set Discount_Amount to 0.
6. WHILE the Subtotal of a Cart is below the Minimum_Subtotal of its Applied_Code, THE Cart SHALL set Discount_Amount to 0.
7. WHILE the Clock date is after the Expiry_Date of the Applied_Code, THE Cart SHALL set Discount_Amount to 0.
8. WHILE the Clock date is after the Expiry_Date of the Applied_Code, THE Cart SHALL keep the Applied_Code attached.

## Open Questions

- F7 (EDGE, low, deferred): `DELETE /carts/<id>/discount` on a Cart with no Applied_Code is not specified (200 with `discount_cents` 0, or 404 `no code applied`).

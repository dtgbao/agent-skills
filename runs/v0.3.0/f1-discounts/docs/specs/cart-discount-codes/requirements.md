# Requirements Document

## Introduction

Shoppers enter a discount code on a cart to lower the price. An operator defines codes in a code registry. A code gives a percent off or a fixed amount in cents off the cart subtotal. A code may need a minimum subtotal and has an expiry date. A cart holds at most one code. The cart API reports the subtotal, the discount, and the total in cents.

## Glossary

- **Shop_API**: the `handle(request, ctx)` function in `shop/api.py`; dict in, dict out.
- **Cart**: a shopper's cart in `shop/cart.py`; holds lines and at most one Discount_Code.
- **Code_Registry**: the operator-defined map from Code_String to Discount_Code, passed in `ctx`.
- **Discount_Code**: a record with a Code_String, a Discount_Kind, a Discount_Value, a Minimum_Subtotal, and an Expiry_Date.
- **Code_String**: the text a shopper enters; 1–20 characters from `A–Z`, `a–z`, `0–9`, `-`; stored and matched without regard to letter case.
- **Discount_Kind**: `percent` or `fixed`.
- **Discount_Value**: an integer; for `percent`, 1–50 (percent); for `fixed`, 1–10,000,000 (cents).
- **Minimum_Subtotal**: an integer number of cents, 0–10,000,000; 0 means no minimum.
- **Expiry_Date**: an ISO 8601 calendar date (`YYYY-MM-DD`); the code is valid up to and including this date.
- **Today**: the current calendar date, read from `ctx["today"]`.
- **Subtotal**: sum of unit price × quantity over cart lines, in cents.
- **Discount_Amount**: the cents taken off the Subtotal by the applied Discount_Code.
- **Total**: Subtotal minus Discount_Amount, in cents.
- **Operator**: the person who defines Discount_Codes in the Code_Registry.
- **Shopper**: the person who uses a Cart through the Shop_API.

## Requirements

### Requirement 1: Define discount codes

**User Story:** As an Operator, I want to define discount codes with bounded values, so that no code gives an invalid discount.

#### Acceptance Criteria

1. WHEN the Operator registers a Discount_Code with a valid Code_String, Discount_Kind, Discount_Value, Minimum_Subtotal, and Expiry_Date, THE Code_Registry SHALL store it under its upper-case Code_String.
2. IF the Discount_Kind is `percent` and the Discount_Value is outside 1–50, THEN THE Code_Registry SHALL reject the Discount_Code with a ValueError.
3. IF the Discount_Kind is `fixed` and the Discount_Value is outside 1–10,000,000, THEN THE Code_Registry SHALL reject the Discount_Code with a ValueError.
4. IF the Code_String, Discount_Kind, Discount_Value, Minimum_Subtotal, or Expiry_Date does not match its Glossary format, THEN THE Code_Registry SHALL reject the Discount_Code with a ValueError.
5. IF the Operator registers a Code_String that the Code_Registry already holds (any letter case), THEN THE Code_Registry SHALL reject the Discount_Code with a ValueError.

### Requirement 2: Apply a code to a cart

**User Story:** As a Shopper, I want to apply a discount code to my cart, so that I pay less.

#### Acceptance Criteria

1. WHEN the Shopper sends `POST /carts/<id>/discount` with a body `code` and no error in criteria 2.2 to 2.7 applies, THE Shop_API SHALL attach the code to the Cart and return status 200 with `subtotal_cents`, `discount_cents`, and `total_cents`.
2. IF the body `code` is missing or does not match the Code_String format, THEN THE Shop_API SHALL return status 400 with error `bad code` and leave the Cart unchanged.
3. IF the body `code` matches no Discount_Code in the Code_Registry, THEN THE Shop_API SHALL return status 404 with error `unknown code` and leave the Cart unchanged.
4. IF Today is after the Expiry_Date of the named Discount_Code, THEN THE Shop_API SHALL return status 422 with error `code expired` and leave the Cart unchanged.
5. IF the Subtotal is below the Minimum_Subtotal of the named Discount_Code, THEN THE Shop_API SHALL return status 422 with error `minimum not met` and leave the Cart unchanged.
6. IF the Cart already holds a Discount_Code, THEN THE Shop_API SHALL return status 409 with error `code already applied` and leave the Cart unchanged.
7. IF the cart id names no Cart, THEN THE Shop_API SHALL return status 404 with error `no cart`.
8. THE Shop_API SHALL check conditions in this order and return the first error: no cart, bad code, unknown code, code already applied, code expired, minimum not met.
9. IF `ctx["today"]` is missing or is not a `YYYY-MM-DD` date, THEN THE Shop_API SHALL raise a ValueError before any other check, for every request that reads a Cart, and leave every Cart unchanged.
10. THE Shop_API SHALL treat a body `code` as well-formed only when it is a string of 1–20 characters from `A–Z`, `a–z`, `0–9`, `-`.

### Requirement 3: Compute the discount

**User Story:** As a Shopper, I want the discount computed the same way every time, so that the price I see is correct.

#### Acceptance Criteria

1. WHILE the Cart holds a `percent` Discount_Code whose Minimum_Subtotal is met and whose Expiry_Date is not before Today, THE Cart SHALL set Discount_Amount to floor(Subtotal × Discount_Value ÷ 100) cents.
2. WHILE the Cart holds a `fixed` Discount_Code whose Minimum_Subtotal is met and whose Expiry_Date is not before Today, THE Cart SHALL set Discount_Amount to the smaller of Discount_Value and Subtotal, in cents.
3. WHILE the Cart holds no Discount_Code, THE Cart SHALL set Discount_Amount to 0 cents.
4. THE Cart SHALL set Total to the larger of 0 and Subtotal minus Discount_Amount, in cents.
5. WHILE the Cart holds a Discount_Code and the Subtotal is below its Minimum_Subtotal, THE Cart SHALL set Discount_Amount to 0 cents.
6. WHILE the Cart holds a Discount_Code and Today is after its Expiry_Date, THE Cart SHALL set Discount_Amount to 0 cents.

### Requirement 4: Show and remove the code

**User Story:** As a Shopper, I want to see and remove the code on my cart, so that I can change my mind.

#### Acceptance Criteria

1. WHEN the Shopper sends `GET /carts/<id>`, THE Shop_API SHALL return `lines`, `subtotal_cents`, `discount_code` (upper-case Code_String or null), `discount_cents`, and `total_cents`.
2. WHEN the Shopper sends `POST /carts/<id>/lines` and the line is added, THE Shop_API SHALL return status 200 with `subtotal_cents`, `discount_cents`, and `total_cents`.
3. WHEN the Shopper sends `DELETE /carts/<id>/discount` and the Cart holds a Discount_Code, THE Shop_API SHALL detach the code and return status 200 with `discount_cents` equal to 0.
4. IF the Shopper sends `DELETE /carts/<id>/discount` and the Cart holds no Discount_Code, THEN THE Shop_API SHALL return status 404 with error `no code applied`.
5. IF the body of `POST /carts/<id>/lines` lacks an integer `unit_price_cents` of 0–10,000,000 or an integer `quantity` of 1–1,000, THEN THE Shop_API SHALL return status 400 with error `bad line` and leave the Cart unchanged.

## Open Questions

- F4 (EDGE, low, deferred): unknown cart id rule is stated only for `POST /carts/<id>/discount`; GET cart, POST lines, and DELETE discount have no rule, and DELETE order against `no code applied` is unclear.
- F9 (ASSUMPTION, low, deferred): `ctx` key for the Code_Registry, the Operator registration call name, and the shape of each `lines` item are not named.
- F11 (EDGE, low, deferred): a request body that is absent or not an object is not specified for `POST /carts/<id>/discount`.

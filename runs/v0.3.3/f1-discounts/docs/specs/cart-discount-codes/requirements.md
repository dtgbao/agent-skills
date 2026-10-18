# Requirements Document

## Introduction

Shoppers enter a discount code on a cart to lower its total. A code takes a percent (1–50) or a fixed amount in cents off the cart subtotal. A code may need a minimum subtotal and has an expiry date. A cart holds at most one code. Operators define codes in a registry. The shop core (`shop/`) and its dict-in, dict-out API (`shop/api.py`) expose the feature.

## Glossary

- **Cart**: the `shop.cart.Cart` object. Holds lines and a subtotal in integer cents.
- **Subtotal**: sum of line price × quantity in integer cents, from `Cart.subtotal_cents()`.
- **Discount_Code**: a record with a Code_String, one Discount_Kind, a Value, a Minimum_Subtotal, and an Expiry_Date. Type: frozen dataclass `shop.discounts.DiscountCode(code_string: str, kind: str, value: int, minimum_subtotal: int, expiry_date: date)`. The constructor does not validate; only `CodeRegistry.add` raises `ValueError`.
- **Code_String**: the text a shopper enters. 1–20 characters, uppercase letters `A–Z` and digits `0–9` only.
- **Discount_Kind**: `percent` or `fixed`.
- **Value**: for `percent`, an integer 1–50 (percent). For `fixed`, an integer 1–10,000,000 (cents).
- **Minimum_Subtotal**: an integer 0–10,000,000 cents. Default 0.
- **Expiry_Date**: a `datetime.date`. The code is usable through the end of that date, inclusive.
- **Today**: the current date as a `datetime.date`, passed in by the caller (`ctx["today"]` in the API). The shop core never reads the system clock.
- **Code_Registry**: a `shop.discounts.CodeRegistry` object that stores Discount_Codes keyed by Code_String. `add(code: DiscountCode) -> None`, `get(code_string: str) -> DiscountCode | None`. `ctx["codes"]` in the API.
- **DiscountError**: the exception `shop.discounts.DiscountError`. Its message is the error text.
- **Applied_Code**: the one Discount_Code a Cart holds, or none.
- **Discount**: the amount in integer cents taken off the Subtotal.
- **Total**: Subtotal minus Discount, in integer cents.
- **Cart discount methods**: `Cart.apply_code(code_string: str, registry: CodeRegistry, today: date) -> None`, `Cart.remove_code() -> None`, `Cart.discount_cents(today: date) -> int`, `Cart.total_cents(today: date) -> int`.
- **Shop_API**: the `shop.api.handle(request, ctx)` function.

## Requirements

### Requirement 1: Define discount codes

**User Story:** As an operator, I want to define discount codes, so that shoppers can use them.

#### Acceptance Criteria

1. WHEN an operator adds a Discount_Code with a valid Code_String, Discount_Kind, Value, Minimum_Subtotal, and Expiry_Date, THE Code_Registry SHALL store it so a lookup by that Code_String returns it.
2. IF the Discount_Kind is `percent` and the Value is not an integer from 1 to 50, THEN THE Code_Registry SHALL reject the code with a `ValueError`.
3. IF the Discount_Kind is `fixed` and the Value is not an integer from 1 to 10,000,000, THEN THE Code_Registry SHALL reject the code with a `ValueError`.
4. IF the Code_String is not 1–20 characters of `A–Z` and `0–9`, or the Minimum_Subtotal is not an integer from 0 to 10,000,000, THEN THE Code_Registry SHALL reject the code with a `ValueError`.
5. IF an operator adds a Discount_Code whose Code_String the Code_Registry already holds, THEN THE Code_Registry SHALL reject the code with a `ValueError` and keep the stored code unchanged.
6. WHEN `get` is called with a Code_String the Code_Registry does not hold, THE Code_Registry SHALL return `None`.
7. IF the Discount_Kind is not `percent` or `fixed`, or the Expiry_Date is not a `datetime.date`, THEN THE Code_Registry SHALL reject the code with a `ValueError` and store nothing.

### Requirement 2: Apply a code to a cart

**User Story:** As a shopper, I want to apply a discount code to my cart, so that I pay less.

#### Acceptance Criteria

1. WHEN a shopper applies a Code_String that the Code_Registry holds, Today is on or before its Expiry_Date, and the Subtotal is at least its Minimum_Subtotal, THE Cart SHALL set that Discount_Code as its Applied_Code.
2. IF the applied text is not an exact, case-sensitive match to a Code_String the Code_Registry holds, THEN THE Cart SHALL reject the apply with error `unknown code` and keep its Applied_Code unchanged.
3. IF Today is after the Expiry_Date of the code, THEN THE Cart SHALL reject the apply with error `expired` and keep its Applied_Code unchanged.
4. IF the Subtotal is less than the Minimum_Subtotal of the code, THEN THE Cart SHALL reject the apply with error `below minimum` and keep its Applied_Code unchanged.
5. IF the Cart already has an Applied_Code, THEN THE Cart SHALL reject the apply with error `code already applied` and keep its Applied_Code unchanged.
6. WHEN the Cart rejects an apply, THE Cart SHALL raise a DiscountError whose message is the error text.
7. WHEN an apply fails more than one of 2.2–2.5, THE Cart SHALL raise the first error in this order: `code already applied`, `unknown code`, `expired`, `below minimum`.

### Requirement 3: Remove a code from a cart

**User Story:** As a shopper, I want to remove the code from my cart, so that I can use a different code.

#### Acceptance Criteria

1. WHEN a shopper removes the code from a Cart that has an Applied_Code, THE Cart SHALL set its Applied_Code to none.
2. WHEN a shopper removes the code from a Cart that has no Applied_Code, THE Cart SHALL complete without error and keep its Applied_Code as none.

### Requirement 4: Compute discount and total

**User Story:** As a shopper, I want to see the discount and the total, so that I know what I will pay.

#### Acceptance Criteria

1. WHILE the Applied_Code has Discount_Kind `percent`, THE Cart SHALL compute the Discount as floor(Subtotal × Value ÷ 100) cents.
2. WHILE the Applied_Code has Discount_Kind `fixed`, THE Cart SHALL compute the Discount as the smaller of Value and Subtotal, in cents.
3. WHILE the Cart has no Applied_Code, THE Cart SHALL compute the Discount as 0 cents.
4. THE Cart SHALL compute the Total as Subtotal minus Discount, in cents.
5. WHILE the Subtotal is less than the Minimum_Subtotal of the Applied_Code, THE Cart SHALL compute the Discount as 0 cents.
6. WHILE Today is after the Expiry_Date of the Applied_Code, THE Cart SHALL compute the Discount as 0 cents.

### Requirement 5: Discount routes in the API

**User Story:** As a client developer, I want API routes for discount codes, so that a storefront can use them.

#### Acceptance Criteria

1. WHEN the Shop_API gets `POST /carts/<id>/discount` with body `{"code": <Code_String>}` and the apply succeeds, THE Shop_API SHALL return status 200 with body fields `subtotal_cents`, `discount_cents`, and `total_cents`.
2. IF the apply is rejected with `unknown code`, `expired`, or `below minimum`, THEN THE Shop_API SHALL return status 400 with body `{"error": <that error text>}`.
3. IF the apply is rejected with `code already applied`, THEN THE Shop_API SHALL return status 409 with body `{"error": "code already applied"}`.
4. WHEN the Shop_API gets `DELETE /carts/<id>/discount` for an existing cart, THE Shop_API SHALL return status 200 with body fields `subtotal_cents`, `discount_cents`, and `total_cents`.
5. WHEN the Shop_API gets `GET /carts/<id>`, THE Shop_API SHALL return the body fields `lines`, `subtotal_cents`, `discount_cents`, `total_cents`, and `code` (the Applied_Code's Code_String or null).
6. IF the `POST /carts/<id>/discount` body has no `code` field or a `code` that is not a string, THEN THE Shop_API SHALL return status 400 with body `{"error": "bad code"}`.

## Open Questions

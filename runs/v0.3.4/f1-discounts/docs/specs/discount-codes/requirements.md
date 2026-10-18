# Requirements Document

## Introduction

This feature lets a shopper put one discount code on a cart. The code lowers the amount due. The shop operator creates the codes. A code takes either a percent (1–50) or a fixed number of cents off the cart subtotal. A code can need a minimum subtotal. Every code has a last valid date. The feature lives in the shop core and in its request handler.

## Glossary

- **Shop**: the `shop` package: `Cart`, `Inventory`, `CATALOG`, and the request handler `handle`.
- **Operator**: a person or script that creates discount codes.
- **Shopper**: a person who uses a cart through the Handler.
- **Handler**: the function `shop.api.handle(request, ctx)`.
- **Cart**: an instance of `shop.cart.Cart`.
- **Subtotal**: the value of `Cart.subtotal_cents()`, in integer cents, 0 or more.
- **Discount_Code**: an operator-made record with a Code, a Kind, an Amount, a Min_Subtotal, and a Valid_Until date.
- **Code**: a string of 3–16 characters, each an uppercase letter `A–Z`, a digit `0–9`, or `-`.
- **Kind**: `percent` or `fixed`.
- **Amount**: an integer. Kind `percent`: 1–50 (percent). Kind `fixed`: 1–1,000,000 (cents).
- **Min_Subtotal**: an integer number of cents, 0–1,000,000. 0 means no minimum.
- **Valid_Until**: the last calendar date on which the code can be used.
- **Code_Book**: the set of Discount_Codes the Operator has created, one per Code. Type `shop.discounts.CodeBook`, held in `ctx["code_book"]`. The Operator creates a code with `CodeBook.create(code, kind, amount, min_subtotal, valid_until)`, which raises `ValueError` on refusal.
- **Current_Date**: the calendar date that the caller passes in for each operation, as a `datetime.date`. The Handler reads it from `ctx["today"]`. Each Cart method that needs it takes it as the argument `today`.
- **Attached_Code**: the Discount_Code a Cart holds. A Cart holds zero or one.
- **Cart code methods**: `Cart.attach_code(code, code_book, today) -> None`, `Cart.detach_code() -> None`, `Cart.discount_cents(today) -> int`, `Cart.amount_due_cents(today) -> int`. A refused attach raises `shop.discounts.AttachRefused`; its `reason` attribute holds the reason string.
- **Discount_Amount**: the cents taken off the Subtotal.
- **Amount_Due**: Subtotal minus Discount_Amount, in cents.

## Requirements

### Requirement 1: Create discount codes

**User Story:** As an operator, I want to create discount codes, so that I can run promotions.

#### Acceptance Criteria

1. WHEN the Operator creates a Discount_Code whose fields are all in range, THE Code_Book SHALL hold that Discount_Code under its Code.
2. IF the Kind is `percent` and the Amount is outside 1–50, THEN THE Code_Book SHALL refuse the Discount_Code and stay unchanged.
3. IF the Kind is `fixed` and the Amount is outside 1–1,000,000, THEN THE Code_Book SHALL refuse the Discount_Code and stay unchanged.
4. IF the Code does not match the Code format, THEN THE Code_Book SHALL refuse the Discount_Code and stay unchanged.
5. IF the Min_Subtotal is outside 0–1,000,000, THEN THE Code_Book SHALL refuse the Discount_Code and stay unchanged.
6. IF the Code_Book already holds a Discount_Code with the same Code, THEN THE Code_Book SHALL refuse the new Discount_Code and keep the old one.
7. IF the Kind is not `percent` or `fixed`, or the Amount is not an integer, THEN THE Code_Book SHALL refuse the Discount_Code and stay unchanged.

### Requirement 2: Attach a code to a cart

**User Story:** As a shopper, I want to put a code on my cart, so that the amount due goes down.

#### Acceptance Criteria

1. WHEN the Shopper attaches a Code that is in the Code_Book, Current_Date is on or before Valid_Until, and the Subtotal is at least Min_Subtotal, THE Cart SHALL make that Discount_Code its Attached_Code.
2. IF the Code is not in the Code_Book, THEN THE Cart SHALL refuse the attach with reason `code_not_found`.
3. IF Current_Date is after Valid_Until, THEN THE Cart SHALL refuse the attach with reason `code_expired`.
4. IF the Subtotal is less than Min_Subtotal, THEN THE Cart SHALL refuse the attach with reason `minimum_not_met`.
5. IF the Cart already has an Attached_Code, THEN THE Cart SHALL refuse the attach with reason `code_already_attached`.
6. WHEN the Cart refuses an attach, THE Cart SHALL keep its Attached_Code as it was before the attach.
7. IF more than one refusal condition holds, THEN THE Cart SHALL refuse with the first reason in the order `code_not_found`, `code_already_attached`, `code_expired`, `minimum_not_met`.

### Requirement 3: Detach a code

**User Story:** As a shopper, I want to take the code off my cart, so that I can try another code.

#### Acceptance Criteria

1. WHEN the Shopper detaches the code from a Cart, THE Cart SHALL have no Attached_Code.
2. IF the Cart has no Attached_Code when the Shopper detaches, THEN THE Cart SHALL finish without an error.

### Requirement 4: Price the cart

**User Story:** As a shopper, I want to see the discount and the amount due, so that I know the price.

#### Acceptance Criteria

1. WHILE the Attached_Code has Kind `percent`, THE Cart SHALL report Discount_Amount = floor(Subtotal × Amount / 100) cents.
2. WHILE the Attached_Code has Kind `fixed`, THE Cart SHALL report Discount_Amount = min(Amount, Subtotal) cents.
3. WHILE the Cart has no Attached_Code, THE Cart SHALL report Discount_Amount = 0 cents.
4. THE Cart SHALL report Amount_Due = Subtotal − Discount_Amount cents.
5. WHILE the Subtotal is less than the Attached_Code's Min_Subtotal, THE Cart SHALL report Discount_Amount = 0 cents, overriding 4.1 and 4.2.
6. WHILE Current_Date is after the Attached_Code's Valid_Until, THE Cart SHALL report Discount_Amount = 0 cents, overriding 4.1 and 4.2.

### Requirement 5: Discount routes

**User Story:** As a storefront developer, I want handler routes for codes, so that the web page can attach, detach, and show them.

#### Acceptance Criteria

1. WHEN the Handler gets `PUT /carts/<id>/code` with body `{"code": <string>}` and the attach succeeds, THE Handler SHALL answer status 200 with `subtotal_cents`, `discount_cents`, and `amount_due_cents`.
2. IF the attach is refused, THEN THE Handler SHALL answer status 422 with body `{"error": <reason>}`.
3. IF the body of `PUT /carts/<id>/code` lacks `code` or `code` is not a string, THEN THE Handler SHALL answer status 400 with body `{"error": "invalid_body"}`.
4. WHEN the Handler gets `DELETE /carts/<id>/code`, THE Handler SHALL answer status 200 with `subtotal_cents`, `discount_cents`, and `amount_due_cents`.
5. WHEN the Handler gets `GET /carts/<id>`, THE Handler SHALL add `code`, `discount_cents`, and `amount_due_cents` to the existing body, with `code` null when the Cart has no Attached_Code.
6. IF `ctx["today"]` is missing or not a `datetime.date`, or `ctx["code_book"]` is missing, on a request to a route in Requirement 5, THEN THE Handler SHALL answer status 500 with body `{"error": "bad_context"}` before any body check.
7. WHEN the Handler answers status 500 with `bad_context`, THE Handler SHALL leave every Cart's lines and Attached_Code unchanged.

## Open Questions

- F6 (AMBIGUITY, low, deferred): type of `code` in the `GET /carts/<id>` body when a code is attached (Code string or full record).
- F9 (EDGE, low, deferred): no refusal rule for a non-integer Min_Subtotal or a Valid_Until that is not a `datetime.date`.
- F11 (INCONSISTENCY, medium, deferred): order of 5.6 (500 `bad_context`) against the existing 404 `no cart` when both apply.

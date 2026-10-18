# Analyst round 2 (FOCUSED) — raw output

Delivered via SubagentHandback message from agent ab31b300d7a972a37.

```
Running as claude-sonnet-5-5 (Sonnet 5.5) with Read, Glob, Grep, and SubagentHandback.

ID: F8
TYPE: EDGE
SEVERITY: medium
AFFECTS: Requirement 2.2, Requirement 2.7, Requirement 3.3
QUOTE: "THE Cart_API SHALL return the error of the first failing check in this order: 400, 404, 410, 422, 409."
ISSUE: The spec does not say what happens when the cart id is unknown. `shop/api.py` already returns 404 `no cart` before any route check, and 2.2 also uses 404, for `unknown code`. The order in 2.7 does not place this error.
OPTIONS:
  A) 2.8: WHEN a shopper sends `POST` or `DELETE /carts/<id>/discount` for a cart id that does not exist, THE Cart_API SHALL return status 404 with error `no cart` before it runs any other check.
  B) 2.8: WHEN a shopper sends `POST /carts/<id>/discount` for a cart id that does not exist and the body has a valid `code`, THE Cart_API SHALL return status 404 with error `no cart` after the 400 check.

ID: F9
TYPE: EDGE
SEVERITY: medium
AFFECTS: Requirement 4.1, Requirement 4.4, Requirement 2.3
QUOTE: "WHERE the Applied_Code has Discount_Kind `percent`, THE Cart SHALL set Discount_Amount to floor(Subtotal × value ÷ 100) cents."
ISSUE: Requirement 4.6 sets Discount_Amount to 0 when the Subtotal falls below the minimum. The spec says nothing about an Applied_Code that expires after it was attached. `GET /carts/<id>` could still show the discount or show 0.
OPTIONS:
  A) 4.7: WHILE the Clock date is after the Expiry_Date of the Applied_Code, THE Cart SHALL set Discount_Amount to 0 and keep the Applied_Code attached.
  B) 4.7: WHILE the Clock date is after the Expiry_Date of the Applied_Code, THE Cart_API SHALL keep Discount_Amount unchanged on `GET /carts/<id>`, because expiry is checked only when a code is applied.
```

# Checkpoints (plugin 0.3.4)

- Run 1, checkpoint 2: 6 passed → [x]
- Run 1, checkpoint 4: 9 passed → [x]
- Run 1, checkpoint 6 (final): 16 passed → [x]
- Run 2, checkpoint 2: 1 failed (tests/test_cart_codes.py::test_attach_matches_precedence, ValueError from CodeBook.create at shop/discounts.py:41), 15 passed → deferred (file in Files of in-scope leaf 3.2, not yet run)
- Run 2, checkpoint 2 (re-run after 3.2), 4, 6: 16 passed → [x]

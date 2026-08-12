---
title: Avoid Circular Imports
impact: CRITICAL
tags: architecture, imports, dependencies
---

## Avoid Circular Imports

Keep imports directed toward lower-level contracts. Move shared types or functions into a neutral
module instead of relying on imports performed inside functions to hide a cycle.

**Incorrect:**

```python
# users.py imports orders.py while orders.py imports users.py.
def load_user_orders() -> None:
    from app.orders import load_orders
    load_orders()
```

**Correct:**

```python
from typing import Protocol

class OrderReader(Protocol):
    def load_for_user(self, user_id: int) -> list[int]: ...

def load_user_orders(user_id: int, reader: OrderReader) -> list[int]:
    return reader.load_for_user(user_id)
```

**Compatibility:** Python initializes an imported module once; partially initialized cycles remain fragile.

References:

- [Python: The Import System](https://docs.python.org/3/reference/import.html)
- [Python FAQ: Circular Imports](https://docs.python.org/3/faq/programming.html#what-are-the-best-practices-for-using-import-in-a-module)


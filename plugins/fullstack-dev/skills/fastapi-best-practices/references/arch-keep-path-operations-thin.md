---
title: Keep Path Operations Thin
impact: HIGH
tags: architecture, routes, services
---

## Keep Path Operations Thin

Limit path operations to transport work: receive validated values, invoke a focused use case, and
return its result. Keep reusable business rules in ordinary typed Python functions or objects.

**Incorrect:**

```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/prices")
def price(quantity: int, unit_price: int) -> dict[str, int]:
    total = quantity * unit_price
    return {"total": total}
```

**Correct:**

```python
from fastapi import FastAPI

app = FastAPI()

def calculate_total(quantity: int, unit_price: int) -> int:
    return quantity * unit_price

@app.post("/prices")
def price(quantity: int, unit_price: int) -> dict[str, int]:
    return {"total": calculate_total(quantity, unit_price)}
```

**Compatibility:** Introduce a service or repository only when reuse or complexity justifies it.

References:

- [FastAPI: Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [FastAPI: Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/)


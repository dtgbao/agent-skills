---
title: Version Breaking APIs With Router Prefixes
impact: MEDIUM
tags: api, versioning, routers
---

## Version Breaking APIs With Router Prefixes

Keep compatible changes in the current API. When a contract must break, isolate the new endpoints
behind a separate router prefix and operate both versions for an explicit migration window.

**Incorrect:**

```python
@app.get("/users/{user_id}")
def user(user_id: int) -> dict[str, str]:
    return {"full_name": "Ada Lovelace"}
```

**Correct:**

```python
from fastapi import APIRouter, FastAPI

v1 = APIRouter(prefix="/api/v1")
v2 = APIRouter(prefix="/api/v2")

app = FastAPI()
app.include_router(v1)
app.include_router(v2)
```

**Compatibility:** URI versioning is a convention, not a FastAPI requirement; follow an existing contract strategy.

References:

- [FastAPI: APIRouter](https://fastapi.tiangolo.com/reference/apirouter/)
- [FastAPI: Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/)


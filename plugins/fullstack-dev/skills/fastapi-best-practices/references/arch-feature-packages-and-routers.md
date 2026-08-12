---
title: Organize Features With Packages and Routers
impact: CRITICAL
tags: architecture, packages, routers
---

## Organize Features With Packages and Routers

Group related endpoints and dependencies in Python packages, expose an `APIRouter`, and compose
routers in the application entrypoint. Do not let one module accumulate the whole API.

**Incorrect:**

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users")
def users() -> list[dict[str, str]]:
    return []
```

**Correct:**

```python
from fastapi import APIRouter, FastAPI

users_router = APIRouter(prefix="/users", tags=["users"])

@users_router.get("")
def list_users() -> list[dict[str, str]]:
    return []

app = FastAPI()
app.include_router(users_router)
```

**Compatibility:** `APIRouter` is a core FastAPI API. Match the repository's existing package layout.

References:

- [FastAPI: Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/)


---
title: Centralize Authentication and Authorization
impact: CRITICAL
tags: security, authorization, dependencies
---

## Centralize Authentication and Authorization

Express authentication, active-user checks, roles, and scopes as dependencies. Do not repeat
ad-hoc token or ownership checks in each path operation.

**Incorrect:**

```python
def delete_item(token: str) -> None:
    if token != "admin":
        raise PermissionError
```

**Correct:**

```python
from typing import Annotated
from fastapi import Depends, HTTPException

def require_admin() -> str:
    user_role = "admin"
    if user_role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    return user_role

Admin = Annotated[str, Depends(require_admin)]

def delete_item(_: Admin) -> None:
    return None
```

**Compatibility:** Use `Security` and OAuth2 scopes when the authorization model is scope-based.

References:

- [FastAPI: Security](https://fastapi.tiangolo.com/tutorial/security/)
- [FastAPI: OAuth2 Scopes](https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/)


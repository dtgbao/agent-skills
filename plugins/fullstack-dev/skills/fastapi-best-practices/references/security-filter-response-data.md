---
title: Filter Response Data
impact: CRITICAL
tags: security, response-model, serialization
---

## Filter Response Data

Declare an output type or `response_model` so FastAPI validates and filters returned data. Never
return persistence entities or input models that contain secrets.

**Incorrect:**

```python
from pydantic import BaseModel

class UserRecord(BaseModel):
    email: str
    password_hash: str

def get_user() -> UserRecord:
    return UserRecord(email="a@example.com", password_hash="secret")
```

**Correct:**

```python
from pydantic import BaseModel

class UserPublic(BaseModel):
    email: str

def get_user() -> UserPublic:
    return UserPublic(email="a@example.com")
```

**Compatibility:** Pydantic 2 narrows nested subclass serialization to the annotated type by default.

References:

- [FastAPI: Response Model](https://fastapi.tiangolo.com/tutorial/response-model/)
- [Pydantic: Serialization](https://docs.pydantic.dev/latest/concepts/serialization/)


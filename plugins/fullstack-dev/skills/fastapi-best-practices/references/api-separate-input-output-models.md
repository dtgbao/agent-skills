---
title: Separate Input and Output Models
impact: HIGH
tags: api, pydantic, schemas
---

## Separate Input and Output Models

Use purpose-specific Pydantic models for create, update, internal, and public representations.
Serialize with Pydantic 2 APIs instead of copying dictionaries by hand.

**Incorrect:**

```python
from pydantic import BaseModel

class User(BaseModel):
    email: str
    password: str
    id: int | None = None
```

**Correct:**

```python
from pydantic import BaseModel, ConfigDict

class UserCreate(BaseModel):
    email: str
    password: str

class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: str

data = UserCreate(email="a@example.com", password="secret").model_dump()
```

**Compatibility:** Pydantic 2 uses `model_dump()` and `model_config`; detect v1 before changing existing code.

References:

- [FastAPI: Extra Models](https://fastapi.tiangolo.com/tutorial/extra-models/)
- [Pydantic: Migration Guide](https://docs.pydantic.dev/latest/migration/)


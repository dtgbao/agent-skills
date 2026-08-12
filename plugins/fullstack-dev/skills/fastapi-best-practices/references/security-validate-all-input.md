---
title: Validate All Untrusted Input
impact: CRITICAL
tags: security, validation, pydantic
---

## Validate All Untrusted Input

Describe bodies, paths, queries, headers, and cookies with constrained types. Treat validation as a
boundary concern; do not pass raw dictionaries into business or persistence code.

**Incorrect:**

```python
def create_user(payload: dict[str, object]) -> dict[str, object]:
    return payload
```

**Correct:**

```python
from typing import Annotated
from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=100)]
    age: Annotated[int, Field(ge=0, le=130)]

def create_user(payload: UserCreate) -> UserCreate:
    return payload
```

**Compatibility:** Use Pydantic 2 validators and strict mode only where coercion is unsafe.

References:

- [FastAPI: Request Body](https://fastapi.tiangolo.com/tutorial/body/)
- [Pydantic: Strict Mode](https://docs.pydantic.dev/latest/concepts/strict_mode/)


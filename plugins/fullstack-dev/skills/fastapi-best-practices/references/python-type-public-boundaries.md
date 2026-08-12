---
title: Type Public Boundaries
impact: CRITICAL
tags: python, typing, contracts
---

## Type Public Boundaries

Annotate path operations, dependencies, services, and adapters. FastAPI derives validation and
OpenAPI from annotations, while type checkers verify internal calls before runtime.

**Incorrect:**

```python
def find_user(user_id):
    return {"id": user_id}
```

**Correct:**

```python
from collections.abc import Mapping
from datetime import UTC, datetime

def find_user(user_id: int) -> Mapping[str, int]:
    return {"id": user_id}

def observed_at() -> datetime:
    return datetime.now(UTC)
```

**Compatibility:** Examples use built-in generics and timezone-aware UTC values. Avoid the deprecated
`datetime.utcnow()` constructor in Python 3.12+.

References:

- [FastAPI: Python Types Intro](https://fastapi.tiangolo.com/python-types/)
- [Python: typing](https://docs.python.org/3/library/typing.html)
- [Python: datetime](https://docs.python.org/3/library/datetime.html#datetime.datetime.utcnow)

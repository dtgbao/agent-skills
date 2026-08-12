---
title: Use Protocols for Narrow Ports
impact: HIGH
tags: python, protocols, architecture
---

## Use Protocols for Narrow Ports

Describe the behavior a use case needs with a small `Protocol`. Avoid forcing adapters and test
doubles to inherit from a framework-aware base class.

**Incorrect:**

```python
class UserService:
    def __init__(self, database: object) -> None:
        self.database = database
```

**Correct:**

```python
from typing import Protocol

class UserReader(Protocol):
    def get(self, user_id: int) -> dict[str, int] | None: ...

class UserService:
    def __init__(self, users: UserReader) -> None:
        self.users = users
```

**Compatibility:** `Protocol` is in the standard library; use only where implementations are swapped.

References:

- [Python: Protocols](https://docs.python.org/3/library/typing.html#typing.Protocol)
- [PEP 544](https://peps.python.org/pep-0544/)


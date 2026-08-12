---
title: Catch Narrowly and Preserve Causes
impact: HIGH
tags: errors, exceptions, debugging
---

## Catch Narrowly and Preserve Causes

Catch only failures the current layer can handle. When translating an exception, use `raise ...
from ...` so logs and tracebacks retain the original cause.

**Incorrect:**

```python
def parse_count(value: str) -> int:
    try:
        return int(value)
    except Exception:
        raise RuntimeError("Invalid count")
```

**Correct:**

```python
def parse_count(value: str) -> int:
    try:
        return int(value)
    except ValueError as exc:
        raise RuntimeError("Invalid count") from exc
```

**Compatibility:** Let unexpected exceptions reach centralized logging and error handling.

References:

- [Python: Exceptions](https://docs.python.org/3/tutorial/errors.html)
- [Python: raise statement](https://docs.python.org/3/reference/simple_stmts.html#the-raise-statement)


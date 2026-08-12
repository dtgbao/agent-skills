---
title: Use Yield Dependencies for Cleanup
impact: CRITICAL
tags: dependency-injection, cleanup, yield
---

## Use Yield Dependencies for Cleanup

Represent request-scoped resources with a dependency that yields once and performs cleanup in
`finally`. Re-raise caught exceptions so FastAPI can handle them.

**Incorrect:**

```python
def get_resource() -> object:
    return object()
```

**Correct:**

```python
from collections.abc import Generator

def get_resource() -> Generator[object, None, None]:
    resource = object()
    try:
        yield resource
    finally:
        del resource
```

**Compatibility:** Check FastAPI dependency `scope` semantics for the installed version.

References:

- [FastAPI: Dependencies with yield](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/)
- [FastAPI: Advanced Dependencies](https://fastapi.tiangolo.com/advanced/advanced-dependencies/)


---
title: Choose Dependency Cache and Scope Deliberately
impact: HIGH
tags: dependency-injection, cache, scope
---

## Choose Dependency Cache and Scope Deliberately

FastAPI normally reuses one dependency result within a request. Disable caching only when repeated
construction is required, and align generator teardown scope with response consumption.

**Incorrect:**

```python
from fastapi import Depends

def nonce() -> object:
    return object()

def endpoint(first: object = Depends(nonce), second: object = Depends(nonce)) -> bool:
    return first is not second
```

**Correct:**

```python
from typing import Annotated
from fastapi import Depends

def nonce() -> object:
    return object()

FreshNonce = Annotated[object, Depends(nonce, use_cache=False)]

def endpoint(first: FreshNonce, second: FreshNonce) -> bool:
    return first is not second
```

**Compatibility:** `use_cache=False` is explicit; dependency `scope` support is version-sensitive.

References:

- [FastAPI Depends reference](https://fastapi.tiangolo.com/reference/dependencies/)
- [FastAPI: Dependencies with yield](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/)


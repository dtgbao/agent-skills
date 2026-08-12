---
title: Match Def or Async Def to the Workload
impact: CRITICAL
tags: async, routes, concurrency
---

## Match Def or Async Def to the Workload

Use `async def` when called libraries are awaitable. Use `def` for blocking libraries so FastAPI
can run the path operation in its thread pool. Do not choose syntax by fashion.

**Incorrect:**

```python
import time

async def wait_for_result() -> str:
    time.sleep(1)
    return "done"
```

**Correct:**

```python
import time

def wait_for_result() -> str:
    time.sleep(1)
    return "done"
```

**Compatibility:** Mixed sync and async path operations are supported; inspect the called library.

References:

- [FastAPI: Concurrency and async/await](https://fastapi.tiangolo.com/async/)


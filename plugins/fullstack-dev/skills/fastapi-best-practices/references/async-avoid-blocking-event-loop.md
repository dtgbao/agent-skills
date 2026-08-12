---
title: Avoid Blocking the Event Loop
impact: CRITICAL
tags: async, event-loop, performance
---

## Avoid Blocking the Event Loop

Never call blocking file, network, database, or sleep APIs directly from `async def`. Use an async
client, a synchronous path operation, or an explicitly bounded thread offload.

**Incorrect:**

```python
import time

async def endpoint() -> dict[str, bool]:
    time.sleep(1)
    return {"ok": True}
```

**Correct:**

```python
import asyncio

async def endpoint() -> dict[str, bool]:
    await asyncio.sleep(1)
    return {"ok": True}
```

**Compatibility:** `asyncio.to_thread()` is suitable for bounded blocking I/O, not unlimited work.

References:

- [FastAPI: Concurrency and async/await](https://fastapi.tiangolo.com/async/)
- [Python: Running in Threads](https://docs.python.org/3/library/asyncio-task.html#asyncio.to_thread)


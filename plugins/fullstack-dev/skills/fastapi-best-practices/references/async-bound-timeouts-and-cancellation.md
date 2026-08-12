---
title: Bound Timeouts and Preserve Cancellation
impact: HIGH
tags: async, timeout, cancellation
---

## Bound Timeouts and Preserve Cancellation

Put time limits around remote work and cleanup. If `CancelledError` is caught for cleanup, re-raise
it so disconnects and shutdown can stop the task.

**Incorrect:**

```python
async def call_remote() -> bytes:
    return await client.read()
```

**Correct:**

```python
import asyncio

async def call_remote() -> bytes:
    try:
        async with asyncio.timeout(5):
            return await client.read()
    except asyncio.CancelledError:
        await close_partial_work()
        raise
```

**Compatibility:** `asyncio.timeout()` requires Python 3.11+.

References:

- [Python: Timeouts](https://docs.python.org/3/library/asyncio-task.html#timeouts)
- [Python: Task Cancellation](https://docs.python.org/3/library/asyncio-task.html#task-cancellation)


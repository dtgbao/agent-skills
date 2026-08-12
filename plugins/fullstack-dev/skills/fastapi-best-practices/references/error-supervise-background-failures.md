---
title: Supervise Background Failures
impact: HIGH
tags: errors, background-tasks, asyncio
---

## Supervise Background Failures

Every spawned task needs an owner that observes its result. Use `BackgroundTasks` only for small
in-process work and make the task function handle and report its own failures.

**Incorrect:**

```python
import asyncio

async def endpoint() -> dict[str, bool]:
    asyncio.create_task(send_notification())
    return {"accepted": True}

async def send_notification() -> None:
    raise RuntimeError("delivery failed")
```

**Correct:**

```python
from fastapi import BackgroundTasks

def send_notification(email: str) -> None:
    try:
        deliver(email)
    except OSError:
        logger.exception("notification failed", extra={"email": email})

def endpoint(tasks: BackgroundTasks) -> dict[str, bool]:
    tasks.add_task(send_notification, "user@example.com")
    return {"accepted": True}
```

**Compatibility:** The example assumes `deliver` and `logger` are provided by the application.

References:

- [FastAPI: Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/)
- [Python: Coroutines and Tasks](https://docs.python.org/3/library/asyncio-task.html)


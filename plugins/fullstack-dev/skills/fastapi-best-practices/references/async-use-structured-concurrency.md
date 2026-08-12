---
title: Use Structured Concurrency
impact: HIGH
tags: async, taskgroup, concurrency
---

## Use Structured Concurrency

Run related concurrent operations inside `TaskGroup` so their lifetime is bounded by the caller and
failures cancel sibling tasks. Avoid orphaned `create_task()` calls.

**Incorrect:**

```python
import asyncio

async def load() -> None:
    asyncio.create_task(load_user())
    asyncio.create_task(load_orders())
```

**Correct:**

```python
import asyncio

async def load() -> None:
    async with asyncio.TaskGroup() as group:
        group.create_task(load_user())
        group.create_task(load_orders())
```

**Compatibility:** `TaskGroup` requires Python 3.11+, matching this skill's baseline.

References:

- [Python: Task Groups](https://docs.python.org/3/library/asyncio-task.html#task-groups)


---
title: Offload Heavy Background Work
impact: HIGH
tags: performance, background-jobs, queues
---

## Offload Heavy Background Work

Use `BackgroundTasks` only for small in-process work. Send CPU-heavy, durable, retryable, or
cross-host jobs to a project-approved worker system and return an accepted/job response.

**Incorrect:**

```python
async def upload_video(data: bytes) -> dict[str, bool]:
    transcode_video(data)
    return {"complete": True}
```

**Correct:**

```python
from fastapi import Response, status

async def upload_video(data: bytes, response: Response) -> dict[str, str]:
    job_id = enqueue_transcode(data)
    response.status_code = status.HTTP_202_ACCEPTED
    return {"job_id": job_id}
```

**Compatibility:** Do not introduce a queue for small best-effort work; follow the installed queue's docs.

References:

- [FastAPI: Background Tasks caveat](https://fastapi.tiangolo.com/tutorial/background-tasks/#caveat)
- [FastAPI: Concurrency and Parallelism](https://fastapi.tiangolo.com/async/#concurrency-parallelism-web-machine-learning)

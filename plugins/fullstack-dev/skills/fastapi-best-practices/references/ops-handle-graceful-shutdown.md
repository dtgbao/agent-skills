---
title: Handle Graceful Shutdown
impact: HIGH
tags: operations, shutdown, lifespan
---

## Handle Graceful Shutdown

Let the ASGI server receive termination signals, stop accepting work, and run lifespan cleanup.
Bound application-owned tasks so shutdown cannot wait forever.

**Incorrect:**

```python
from fastapi import FastAPI

app = FastAPI()
worker = start_worker()
```

**Correct:**

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    worker = start_worker()
    try:
        yield
    finally:
        await worker.stop()

app = FastAPI(lifespan=lifespan)
```

**Compatibility:** Signal and drain behavior belongs to the detected ASGI server and deployment platform.

References:

- [FastAPI: Lifespan Events](https://fastapi.tiangolo.com/advanced/events/)
- [Uvicorn: Server Behavior](https://www.uvicorn.org/server-behavior/)


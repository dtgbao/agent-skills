---
title: Own Application Resources With Lifespan
impact: CRITICAL
tags: architecture, lifespan, resources
---

## Own Application Resources With Lifespan

Create process-wide resources before the application accepts traffic and release them after
shutdown using one lifespan context manager. Do not mix lifespan with legacy startup handlers.

**Incorrect:**

```python
from fastapi import FastAPI

connection = object()
app = FastAPI()
```

**Correct:**

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.connection = object()
    yield
    del app.state.connection

app = FastAPI(lifespan=lifespan)
```

**Compatibility:** `lifespan` is the recommended FastAPI startup and shutdown mechanism.

References:

- [FastAPI: Lifespan Events](https://fastapi.tiangolo.com/advanced/events/)


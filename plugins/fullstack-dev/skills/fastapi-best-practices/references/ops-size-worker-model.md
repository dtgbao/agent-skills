---
title: Size the Worker Model Deliberately
impact: HIGH
tags: operations, workers, deployment
---

## Size the Worker Model Deliberately

Choose worker processes from measured CPU, memory, traffic, and platform behavior. Avoid multiplying
workers both inside a container and at the orchestrator layer without a reason.

**Incorrect:**

```python
WORKERS = 32
```

**Correct:**

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class RuntimePlan:
    workers_per_container: int = 1

plan = RuntimePlan()
```

**Compatibility:** FastAPI CLI/Uvicorn support workers; container orchestration often favors one process per container.

References:

- [FastAPI: Server Workers](https://fastapi.tiangolo.com/deployment/server-workers/)
- [FastAPI: Containers](https://fastapi.tiangolo.com/deployment/docker/)


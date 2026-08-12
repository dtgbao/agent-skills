---
title: Separate Liveness and Readiness
impact: HIGH
tags: operations, health-checks, kubernetes
---

## Separate Liveness and Readiness

Keep liveness cheap and process-local. Make readiness reflect whether the instance can accept
traffic, without turning every probe into an expensive cascade through all dependencies.

**Incorrect:**

```python
def health() -> dict[str, bool]:
    return {"ok": database.ping() and queue.ping() and remote_api.ping()}
```

**Correct:**

```python
from fastapi import FastAPI, Response, status

app = FastAPI()

@app.get("/live")
def live() -> dict[str, str]:
    return {"status": "alive"}

@app.get("/ready")
def ready(response: Response) -> dict[str, str]:
    is_ready = getattr(app.state, "ready", False)
    if not is_ready:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return {"status": "ready" if is_ready else "not-ready"}
```

**Compatibility:** Match probe paths and timing to the deployment platform.

References:

- [Kubernetes: Liveness, Readiness, and Startup Probes](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/)
- [FastAPI: Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/)

---
title: Run Lifespan and Isolate External I/O
impact: HIGH
tags: testing, lifespan, external-services
---

## Run Lifespan and Isolate External I/O

Use a client context or explicit lifespan manager when startup state matters. Replace network,
database, clock, and environment boundaries with dependencies or scoped fixtures in unit tests.
Assert both resource availability during the test and cleanup after the client exits.

**Incorrect:**

```python
from fastapi.testclient import TestClient

client = TestClient(app)
response = client.get("/ready")
```

**Correct:**

```python
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import pytest
from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient


class ApplicationResource:
    def __init__(self) -> None:
        self.started = False
        self.closed = False

    async def start(self) -> None:
        self.started = True

    async def close(self) -> None:
        self.closed = True


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    resource = ApplicationResource()
    await resource.start()
    app.state.resource = resource
    try:
        yield
    finally:
        await resource.close()


app = FastAPI(lifespan=lifespan)


@app.get("/ready")
async def readiness() -> dict[str, bool]:
    if not app.state.resource.started:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Application is not ready",
        )
    return {"ready": True}



def test_ready_runs_startup_and_shutdown() -> None:
    with TestClient(app) as client:
        started_resource = app.state.resource
        assert started_resource.started is True
        assert started_resource.closed is False

        response = client.get("/ready")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"ready": True}

    assert started_resource.closed is True


class WeatherGateway:
    async def fetch(self, city: str) -> dict[str, str]:
        raise RuntimeError("Real network access is forbidden in unit tests")


async def load_forecast(
    gateway: WeatherGateway,
    city: str,
) -> dict[str, str]:
    return await gateway.fetch(city)


@pytest.mark.anyio
async def test_load_forecast_uses_scoped_gateway_stub(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    gateway = WeatherGateway()

    async def fake_fetch(city: str) -> dict[str, str]:
        return {"city": city, "forecast": "sunny"}

    with monkeypatch.context() as scoped_patch:
        scoped_patch.setattr(gateway, "fetch", fake_fetch)
        result = await load_forecast(gateway, "Da Nang")

    assert result == {"city": "Da Nang", "forecast": "sunny"}
```

Patch the name the application looks up, not an unrelated library symbol. Prefer FastAPI dependency
overrides for application dependencies and reserve `monkeypatch` for environment variables, clocks,
or hard external boundaries. Never call real paid or stateful services from unit tests.

**Compatibility:** For HTTPX async tests, pair `ASGITransport` with a lifespan manager only when the
project already includes one; HTTPX does not trigger lifespan itself. Apply `monkeypatch` guidance
only when pytest is installed.

References:

- [FastAPI: Testing Lifespan](https://fastapi.tiangolo.com/advanced/testing-events/)
- [HTTPX: ASGI startup and shutdown](https://www.python-httpx.org/advanced/transports/#asgi-startup-and-shutdown)
- [pytest: Monkeypatching](https://docs.pytest.org/en/stable/how-to/monkeypatch.html)

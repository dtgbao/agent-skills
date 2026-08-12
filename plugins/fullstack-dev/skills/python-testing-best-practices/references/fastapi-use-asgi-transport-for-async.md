---
title: Use ASGITransport for Async Tests
impact: HIGH
tags: testing, httpx, async
---

## Use ASGITransport for Async Tests

When a test must await async application resources, construct HTTPX `AsyncClient` with
`ASGITransport` and mark the test with `pytest.mark.anyio`. Keep application resources scoped to
fixtures so tests can assert both the HTTP response and the resulting async state. Do not use the
removed `AsyncClient(app=...)` shortcut.

**Incorrect:**

```python
from httpx import AsyncClient

async def test_root() -> None:
    async with AsyncClient(app=app, base_url="http://test") as client:
        await client.get("/")
```

**Correct:**

```python
from collections.abc import AsyncIterator

import pytest
from fastapi import FastAPI, status
from httpx import ASGITransport, AsyncClient
from pydantic import BaseModel


class CreateItem(BaseModel):
    name: str


class ItemStore:
    def __init__(self) -> None:
        self.items: dict[str, str] = {}

    async def save(self, item_id: str, name: str) -> None:
        self.items[item_id] = name

    async def get(self, item_id: str) -> str | None:
        return self.items.get(item_id)


def create_app(store: ItemStore) -> FastAPI:
    app = FastAPI()

    @app.post("/items/{item_id}", status_code=status.HTTP_201_CREATED)
    async def create_item(item_id: str, data: CreateItem) -> dict[str, str]:
        await store.save(item_id, data.name)
        return {"id": item_id, "name": data.name}

    return app


@pytest.fixture
def store() -> ItemStore:
    return ItemStore()


@pytest.fixture
async def client(store: ItemStore) -> AsyncIterator[AsyncClient]:
    transport = ASGITransport(app=create_app(store))
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as async_client:
        yield async_client


@pytest.mark.anyio
async def test_create_item_persists_async_state(
    client: AsyncClient,
    store: ItemStore,
) -> None:
    # Arrange
    payload = {"name": "keyboard"}

    # Act
    response = await client.post("/items/item-1", json=payload)
    stored_name = await store.get("item-1")

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"id": "item-1", **payload}
    assert stored_name == "keyboard"
```

**Compatibility:** Apply only when HTTPX, pytest, and an AnyIO pytest plugin are installed. HTTPX
does not trigger ASGI lifespan; use the lifespan rule and a detected lifespan manager when startup
or shutdown state is required.

References:

- [FastAPI: Async Tests](https://fastapi.tiangolo.com/advanced/async-tests/)
- [HTTPX: ASGI Transport](https://www.python-httpx.org/advanced/transports/#asgi-transport)
- [pytest: Fixtures](https://docs.pytest.org/en/stable/explanation/fixtures.html)

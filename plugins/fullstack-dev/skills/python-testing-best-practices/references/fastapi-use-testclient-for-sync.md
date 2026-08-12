---
title: Use TestClient for Synchronous API Tests
impact: HIGH
tags: testing, testclient, http
---

## Use TestClient for Synchronous API Tests

Exercise routes through the ASGI application with `TestClient` instead of calling path functions
directly. Use fixtures for deterministic setup and teardown, name the behavior under test, and
assert status, headers, and serialized bodies. Parameterize equivalent validation cases instead of
copying the same test body.

**Incorrect:**

```python
def test_create_item_with_valid_payload_returns_item() -> None:
    result = create_item(CreateItem(name="keyboard", quantity=2))
    assert result.name == "keyboard"
```

**Correct:**

```python
from collections.abc import Generator

import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field


class CreateItem(BaseModel):
    name: str = Field(min_length=1)
    quantity: int = Field(gt=0)


class Item(CreateItem):
    id: int


app = FastAPI()


@app.post(
    "/items",
    response_model=Item,
    status_code=status.HTTP_201_CREATED,
)
def create_item(data: CreateItem) -> Item:
    return Item(id=1, **data.model_dump())


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as test_client:
        yield test_client


def test_create_item_with_valid_payload_returns_serialized_item(
    client: TestClient,
) -> None:
    # Arrange
    payload = {"name": "keyboard", "quantity": 2}

    # Act
    response = client.post("/items", json=payload)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    assert response.headers["content-type"] == "application/json"
    assert response.json() == {"id": 1, **payload}


@pytest.mark.parametrize(
    ("payload", "invalid_field"),
    [
        pytest.param({"name": "", "quantity": 2}, "name", id="empty-name"),
        pytest.param({"name": "keyboard", "quantity": 0}, "quantity", id="zero-quantity"),
        pytest.param({"name": "keyboard"}, "quantity", id="missing-quantity"),
    ],
)
def test_create_item_with_invalid_payload_returns_validation_error(
    client: TestClient,
    payload: dict[str, object],
    invalid_field: str,
) -> None:
    response = client.post("/items", json=payload)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    errors = response.json()["detail"]
    assert any(error["loc"][-1] == invalid_field for error in errors)
```

**Compatibility:** `TestClient` is synchronous even when the tested endpoint is async. Inspect the
installed FastAPI and Starlette versions and use their supported transport package; current Starlette
prefers `httpx2` while retaining deprecated compatibility with plain HTTPX. Apply only when pytest
is present, and follow the repository's established fixture and naming conventions.

References:

- [FastAPI: Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Starlette: TestClient](https://www.starlette.io/testclient/)
- [pytest: Fixtures](https://docs.pytest.org/en/stable/explanation/fixtures.html)
- [pytest: Parametrization](https://docs.pytest.org/en/stable/how-to/parametrize.html)

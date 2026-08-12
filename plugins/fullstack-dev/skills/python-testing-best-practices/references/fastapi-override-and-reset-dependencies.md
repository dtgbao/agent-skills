---
title: Override and Reset Dependencies
impact: HIGH
tags: testing, dependencies, isolation
---

## Override and Reset Dependencies

Replace costly or external dependencies through `app.dependency_overrides`, then restore the
previous mapping during teardown. Use a constrained mock or fake at the narrow external boundary,
and cover both successful and exceptional behavior. Never let an override leak into another test.

**Incorrect:**

```python
app.dependency_overrides[get_current_user] = lambda: {"id": 1}
```

**Correct:**

```python
from collections.abc import Generator
from typing import Annotated, Protocol, cast
from unittest.mock import AsyncMock

import pytest
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.testclient import TestClient
from pydantic import BaseModel


class RepositoryUnavailable(Exception):
    pass


class User(BaseModel):
    id: str
    email: str


class UserRepository(Protocol):
    async def find_by_id(self, user_id: str) -> User | None: ...


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def find_by_id(self, user_id: str) -> User:
        try:
            user = await self.repository.find_by_id(user_id)
        except RepositoryUnavailable as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="User repository unavailable",
            ) from exc

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {user_id} not found",
            )
        return user


def get_user_repository() -> UserRepository:
    raise RuntimeError("Production repository is not available in tests")


RepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]


def get_user_service(repository: RepositoryDep) -> UserService:
    return UserService(repository)


ServiceDep = Annotated[UserService, Depends(get_user_service)]
app = FastAPI()


@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: str, service: ServiceDep) -> User:
    return await service.find_by_id(user_id)


@pytest.fixture
def repository() -> AsyncMock:
    return AsyncMock(spec=UserRepository)


@pytest.fixture
def client(repository: AsyncMock) -> Generator[TestClient, None, None]:
    previous_overrides = app.dependency_overrides.copy()

    def override_repository() -> UserRepository:
        return cast(UserRepository, repository)

    app.dependency_overrides[get_user_repository] = override_repository
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(previous_overrides)


def test_get_user_when_repository_returns_user_returns_200(
    client: TestClient,
    repository: AsyncMock,
) -> None:
    repository.find_by_id.return_value = User(
        id="user-1",
        email="user@example.com",
    )

    response = client.get("/users/user-1")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": "user-1",
        "email": "user@example.com",
    }
    repository.find_by_id.assert_awaited_once_with("user-1")


def test_get_user_when_repository_fails_returns_503(
    client: TestClient,
    repository: AsyncMock,
) -> None:
    repository.find_by_id.side_effect = RepositoryUnavailable("database offline")

    response = client.get("/users/user-1")

    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert response.json() == {"detail": "User repository unavailable"}
```

**Compatibility:** Apply only when pytest is present. `AsyncMock` is in the Python standard library
for supported Python 3.11+ projects. Prefer a small fake when state-based assertions communicate the
behavior more clearly than mock interactions.

References:

- [FastAPI: Testing Dependencies with Overrides](https://fastapi.tiangolo.com/advanced/testing-dependencies/)
- [pytest: Fixtures](https://docs.pytest.org/en/stable/explanation/fixtures.html)
- [Python: AsyncMock](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.AsyncMock)

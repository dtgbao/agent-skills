---
title: Compose Reusable Annotated Sub-dependencies
impact: CRITICAL
tags: dependency-injection, annotated, sub-dependencies, fastapi
---

## Compose Reusable Annotated Sub-dependencies

Compose request-scoped resources, repositories, and services as a dependency graph. Use provider
functions and reusable `Annotated` aliases so application classes remain independent of FastAPI and
each layer is easy to override in tests. `Depends(...)` is dependency metadata, not a type.

**Incorrect:**

```python
from fastapi import Depends


def get_user_repository() -> object:
    return object()


class UserService:
    def __init__(self, repository: Depends(get_user_repository)):
        self.repository = repository
```

**Correct:**

```python
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db

router = APIRouter()


class UserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get(self, user_id: int) -> object:
        return object()


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def get_user(self, user_id: int) -> object:
        return await self.repository.get(user_id)


DatabaseDep = Annotated[AsyncSession, Depends(get_db)]


def get_user_repository(db: DatabaseDep) -> UserRepository:
    return UserRepository(db)


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]


def get_user_service(repository: UserRepositoryDep) -> UserService:
    return UserService(repository)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


@router.get("/users/{user_id}")
async def get_user(user_id: int, service: UserServiceDep) -> object:
    return await service.get_user(user_id)
```

FastAPI resolves the graph from the bottom up and normally reuses each dependency result within the
request. A class can also be passed directly to `Depends`, including a class whose constructor has
sub-dependencies, but provider functions avoid coupling application constructors to FastAPI:

```python
class UserRepository:
    def __init__(self, db: Annotated[AsyncSession, Depends(get_db)]) -> None:
        self.db = db


UserRepositoryDep = Annotated[UserRepository, Depends(UserRepository)]
```

**Compatibility:** FastAPI 0.95.1+ supports and prefers `Annotated`. Inspect the installed FastAPI
version before using newer dependency features such as explicit dependency teardown scopes.

References:

- [FastAPI: Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [FastAPI: Sub-dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/sub-dependencies/)
- [FastAPI: Classes as dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/classes-as-dependencies/)

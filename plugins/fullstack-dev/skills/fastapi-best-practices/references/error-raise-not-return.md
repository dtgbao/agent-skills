---
title: Raise HTTP Exceptions from FastAPI Services
impact: HIGH
tags: errors, http, exceptions, services
---

## Raise HTTP Exceptions from FastAPI Services

In services that exist specifically for a FastAPI application, raise `HTTPException` directly for
HTTP failures. This keeps routes thin and prevents error unions or sentinel values from spreading
through the call graph. For services shared with non-HTTP transports or reusable domain code, raise
domain exceptions and map them at the HTTP boundary instead.

**Incorrect (return error objects for the route to inspect):**

```python
from fastapi import APIRouter, HTTPException, status


class UserService:
    async def find_by_id(self, user_id: str) -> dict[str, object]:
        user = await self.repository.find_by_id(user_id)
        if user is None:
            return {"error": f"User {user_id} not found"}
        return {"user": user}


router = APIRouter()


@router.get("/users/{user_id}")
async def get_user(user_id: str) -> object:
    result = await user_service.find_by_id(user_id)
    if error := result.get("error"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error)
    return result["user"]
```

**Correct (raise exceptions directly from the service):**

```python
from typing import Annotated, Protocol

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel


class User(BaseModel):
    id: str
    email: str


class CreateUser(BaseModel):
    email: str


class UpdateUser(BaseModel):
    email: str | None = None


class UserRepository(Protocol):
    async def find_by_id(self, user_id: str) -> User | None: ...

    async def find_by_email(self, email: str) -> User | None: ...

    async def save(self, user: User) -> User: ...


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def find_by_id(self, user_id: str) -> User:
        user = await self.repository.find_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {user_id} not found",
            )
        return user

    async def create(self, data: CreateUser) -> User:
        if await self.repository.find_by_email(data.email) is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )
        return await self.repository.save(User(id="generated", email=data.email))

    async def update(self, user_id: str, data: UpdateUser) -> User:
        user = await self.find_by_id(user_id)  # Raises when missing.
        updated = user.model_copy(update=data.model_dump(exclude_unset=True))
        return await self.repository.save(updated)


from app.dependencies import get_user_service

UserServiceDep = Annotated[UserService, Depends(get_user_service)]
router = APIRouter()


@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: str, service: UserServiceDep) -> User:
    return await service.find_by_id(user_id)


@router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(data: CreateUser, service: UserServiceDep) -> User:
    return await service.create(data)
```

For a layer-agnostic service, replace `HTTPException` with a domain exception and register its HTTP
mapping as described by `error-centralize-exception-handlers`:

```python
class UserNotFound(Exception):
    def __init__(self, user_id: str) -> None:
        self.user_id = user_id
        super().__init__(f"User {user_id} not found")


class UserService:
    async def find_by_id(self, user_id: str) -> object:
        user = await self.repository.find_by_id(user_id)
        if user is None:
            raise UserNotFound(user_id)
        return user
```

**Compatibility:** `HTTPException` may be raised from routes, dependencies, or any service called by
them. The Pydantic example uses v2 `model_copy()` and `model_dump()`; inspect the installed Pydantic
version before applying it to an existing project.

References:

- [FastAPI: Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/)

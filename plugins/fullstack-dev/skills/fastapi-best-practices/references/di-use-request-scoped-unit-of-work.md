---
title: Use a Request-Scoped Unit of Work
impact: CRITICAL
tags: dependency-injection, unit-of-work, sqlalchemy, transactions
---

## Use a Request-Scoped Unit of Work

For a typical request-response API, give each request one Unit of Work (UoW) and commit it once after
the path operation succeeds. All repositories and services participating in the operation must share
that UoW and its SQLAlchemy session. Repositories and services may flush, but must never commit.

**Incorrect (transaction ownership is scattered across reusable services):**

```python
class InventoryService:
    def __init__(self, uow: "UnitOfWork") -> None:
        self.uow = uow

    async def reserve_stock(self, product_id: int, quantity: int) -> None:
        inventory = await self.uow.inventory.get_by_product_id(product_id)
        inventory.quantity -= quantity
        await self.uow.commit()


class OrderService:
    def __init__(self, uow: "UnitOfWork", inventory: InventoryService) -> None:
        self.uow = uow
        self.inventory = inventory

    async def create_order(self, product_id: int, quantity: int) -> object:
        order = await self.uow.orders.create(product_id=product_id, quantity=quantity)
        await self.inventory.reserve_stock(product_id, quantity)
        await self.uow.commit()
        return order
```

The inventory change can commit before the order operation finishes, and callers must know which
nested service has already ended the transaction.

**Correct (the FastAPI dependency owns one transaction):**

```python
from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import settings


engine = create_async_engine(
    settings.database_url,
    pool_pre_ping=True,
)

async_session_factory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


class UnitOfWork:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.orders = OrderRepository(session)
        self.inventory = InventoryRepository(session)

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def close(self) -> None:
        await self.session.close()


async def get_uow() -> AsyncIterator[UnitOfWork]:
    uow = UnitOfWork(async_session_factory())
    try:
        yield uow
        await uow.commit()
    except Exception:
        await uow.rollback()
        raise
    finally:
        await uow.close()


UowDep = Annotated[UnitOfWork, Depends(get_uow, scope="function")]
```

Inject the same UoW into cooperating services. Neither service commits:

```python
class InventoryService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def reserve_stock(self, product_id: int, quantity: int) -> None:
        inventory = await self.uow.inventory.get_by_product_id(product_id)
        if inventory.quantity < quantity:
            raise ValueError("Not enough stock")
        inventory.quantity -= quantity


class OrderService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow
        self.inventory = InventoryService(uow)

    async def create_order(self, product_id: int, quantity: int) -> object:
        order = await self.uow.orders.create(product_id=product_id, quantity=quantity)
        await self.inventory.reserve_stock(product_id, quantity)
        return order
```

Use the dependency alias directly at the API boundary. FastAPI creates one UoW for the request and
resumes `get_uow()` after the endpoint returns:

```python
from fastapi import APIRouter

router = APIRouter()


@router.post("/orders")
async def create_order(
    product_id: int,
    quantity: int,
    uow: UowDep,
) -> object:
    service = OrderService(uow)
    return await service.create_order(product_id, quantity)
```

The `function` scope completes teardown before sending the response, so commit failures can still
become error responses. `commit()` flushes pending changes; call `flush()` earlier only when later
work needs a database-generated value.

This is request-boundary commit, not SQLAlchemy's legacy autocommit mode. For slow external I/O, use
shorter transactions and, when needed, an outbox or saga.

**Compatibility:** Use for atomic request-response work. `scope="function"` requires a recent
FastAPI version. Never share one `AsyncSession` or UoW across concurrent tasks.

References:

- [FastAPI: Dependencies with yield](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/)
- [SQLAlchemy: Session basics](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
- [SQLAlchemy: AsyncSession with concurrent tasks](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#using-asyncsession-with-concurrent-tasks)

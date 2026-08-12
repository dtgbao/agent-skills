---
title: Isolate Production-Engine Database Integration Tests
impact: CRITICAL
tags: testing, database, sqlalchemy, transactions
---

## Isolate Production-Engine Database Integration Tests

Run database integration tests against the detected production engine, never a production database.
Give every test an isolated transaction or disposable database, exercise real constraints, and undo
all state. SQLite cannot prove PostgreSQL, MySQL, or vendor-extension behavior. When SQLAlchemy 2
async is present and the driver supports SAVEPOINT correctly, bind each `AsyncSession` to an outer
transaction with `join_transaction_mode="create_savepoint"`.

**Incorrect:**

```python
from sqlalchemy import create_engine


engine = create_engine("sqlite:///:memory:")


def test_postgresql_unique_constraint() -> None:
    session = Session(engine)
    session.query(User).all()
```

**Correct:**

```python
from collections.abc import AsyncIterator
import os

import pytest
from sqlalchemy import String, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(320), unique=True)


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session")
async def engine() -> AsyncIterator[AsyncEngine]:
    database_url = os.environ["TEST_DATABASE_URL"]
    test_engine = create_async_engine(database_url)
    async with test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    try:
        yield test_engine
    finally:
        async with test_engine.begin() as connection:
            await connection.run_sync(Base.metadata.drop_all)
        await test_engine.dispose()


@pytest.fixture
async def session(engine: AsyncEngine) -> AsyncIterator[AsyncSession]:
    async with engine.connect() as connection:
        outer_transaction = await connection.begin()
        test_session = AsyncSession(
            bind=connection,
            expire_on_commit=False,
            join_transaction_mode="create_savepoint",
        )
        try:
            yield test_session
        finally:
            await test_session.close()
            await outer_transaction.rollback()


@pytest.mark.anyio
@pytest.mark.integration
async def test_user_email_unique_constraint_rejects_duplicate(
    session: AsyncSession,
) -> None:
    session.add(User(email="user@example.com"))
    await session.commit()
    session.add(User(email="user@example.com"))

    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.anyio
@pytest.mark.integration
async def test_user_query_returns_committed_user(
    session: AsyncSession,
) -> None:
    session.add(User(email="person@example.com"))
    await session.commit()

    result = await session.scalar(
        select(User).where(User.email == "person@example.com")
    )

    assert result is not None
    assert result.email == "person@example.com"
```

In established projects, provision schema with the detected migration tool instead of metadata
creation. Use a dedicated `TEST_DATABASE_URL`, validate that it cannot target production, and let
`fullstack-dev:ci-cd-and-automation` own disposable service/container provisioning.

**Compatibility:** Apply only to SQLAlchemy 2 async projects with a database/driver that supports
the required SAVEPOINT behavior. Otherwise use a disposable database per test worker. Never share
one `AsyncSession` across concurrent tasks.

References:

- [SQLAlchemy: Asyncio](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [SQLAlchemy: Session join_transaction_mode](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.params.join_transaction_mode)
- [SQLAlchemy: Session basics](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
- [pytest: Fixtures](https://docs.pytest.org/en/stable/explanation/fixtures.html)
- [AnyIO: Higher-scope async fixtures](https://anyio.readthedocs.io/en/stable/testing.html#using-async-fixtures-with-higher-scopes)

---
title: Scope Sessions and Transactions
impact: CRITICAL
tags: database, sqlalchemy, transactions
---

## Scope Sessions and Transactions

When SQLAlchemy is present, create one `Session` or `AsyncSession` per unit of work and give one
layer ownership of commit or rollback. Never share an `AsyncSession` across concurrent tasks.

**Incorrect:**

```python
async def save_both(session: object) -> None:
    await asyncio.gather(save_user(session), save_order(session))
```

**Correct:**

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.DATABASE_URL,  # Async database connection URL.
    echo=settings.DEBUG,  # Log SQL statements only when debug mode is enabled.
    future=True  # Use the SQLAlchemy 2.0 API when running on SQLAlchemy 1.4.
)

AsyncSessionLocal = sessionmaker(
    engine,  # Bind sessions created by this factory to the async engine.
    class_=AsyncSession,  # Create asynchronous ORM sessions.
    expire_on_commit=False  # Keep loaded attributes available after commit.
)

async def get_db() -> AsyncSession:
    """Dependency for database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

**Compatibility:** Apply only to SQLAlchemy 2 projects; use a separate session per concurrent task.

References:

- [SQLAlchemy: AsyncSession with concurrent tasks](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#using-asyncsession-with-concurrent-tasks)
- [SQLAlchemy: Session basics](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)

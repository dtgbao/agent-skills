---
title: Avoid N Plus One and Implicit Async I/O
impact: HIGH
tags: database, sqlalchemy, performance
---

## Avoid N Plus One and Implicit Async I/O

Load the relationships required by a response in the query that owns the session. Under asyncio,
avoid attribute access that silently attempts database I/O after the query or session closes.

**Incorrect:**

```python
async def names(users: list[object]) -> list[str]:
    return [user.team.name for user in users]
```

**Correct:**

```python
from sqlalchemy import select
from sqlalchemy.orm import selectinload

async def load_users(session: object) -> list[object]:
    statement = select(User).options(selectinload(User.team))
    result = await session.scalars(statement)
    return list(result)
```

**Compatibility:** Apply loader options supported by the detected ORM; this example targets SQLAlchemy 2.

References:

- [SQLAlchemy: Preventing Implicit I/O with AsyncSession](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#preventing-implicit-io-when-using-asyncsession)
- [SQLAlchemy: Relationship Loading](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html)


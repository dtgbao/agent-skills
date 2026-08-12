---
title: Use Database Migrations
impact: HIGH
tags: database, migrations, alembic
---

## Use Database Migrations

Version production schema changes as reviewed migrations. Do not create or mutate production
tables opportunistically during application startup.

**Incorrect:**

```python
async def startup() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
```

**Correct:**

```python
def upgrade() -> None:
    op.add_column("users", sa.Column("display_name", sa.String(100), nullable=True))

def downgrade() -> None:
    op.drop_column("users", "display_name")
```

**Compatibility:** The example targets Alembic; follow the detected migration tool and review generated diffs.

References:

- [Alembic: Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [Alembic: Autogenerate](https://alembic.sqlalchemy.org/en/latest/autogenerate.html)


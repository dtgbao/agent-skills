---
title: Validate Settings at Startup
impact: CRITICAL
tags: operations, settings, configuration
---

## Validate Settings at Startup

Parse environment configuration into a typed settings object and fail before serving when required
values are missing. Inject settings so tests can override them.

**Incorrect:**

```python
import os

database_url = os.environ.get("DATABASE_URL", "")
```

**Correct:**

```python
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    database_url: str

@lru_cache
def get_settings() -> Settings:
    return Settings()
```

**Compatibility:** `BaseSettings` lives in `pydantic-settings` for Pydantic 2.

References:

- [FastAPI: Settings and Environment Variables](https://fastapi.tiangolo.com/advanced/settings/)
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)


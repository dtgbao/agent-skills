---
title: Use Contextual Structured Logging
impact: HIGH
tags: operations, logging, observability
---

## Use Contextual Structured Logging

Emit logs through `logging` with stable fields, levels, and exception information. Keep secrets and
full credentials out of log records.

**Incorrect:**

```python
def load_user(user_id: int) -> None:
    print("loading", user_id)
```

**Correct:**

```python
import logging

logger = logging.getLogger(__name__)

def load_user(user_id: int) -> None:
    logger.info("loading user", extra={"user_id": user_id})
```

**Compatibility:** Configure JSON formatting in the deployed logging stack; do not add a library unprompted.

References:

- [Python: Logging HOWTO](https://docs.python.org/3/howto/logging.html)
- [Python: Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html)


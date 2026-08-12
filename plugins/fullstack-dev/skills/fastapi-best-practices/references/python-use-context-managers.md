---
title: Use Context Managers for Resources
impact: HIGH
tags: python, resources, context-manager
---

## Use Context Managers for Resources

Acquire and release files, locks, connections, and temporary state in context managers so cleanup
runs on success, failure, and cancellation.

**Incorrect:**

```python
def read_text(path: str) -> str:
    handle = open(path, encoding="utf-8")
    return handle.read()
```

**Correct:**

```python
def read_text(path: str) -> str:
    with open(path, encoding="utf-8") as handle:
        return handle.read()
```

**Compatibility:** Use `async with` for resources implementing the asynchronous context protocol.

References:

- [Python: contextlib](https://docs.python.org/3/library/contextlib.html)
- [Python: with statement](https://docs.python.org/3/reference/compound_stmts.html#the-with-statement)


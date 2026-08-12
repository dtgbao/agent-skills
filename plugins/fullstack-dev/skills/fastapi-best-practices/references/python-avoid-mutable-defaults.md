---
title: Avoid Mutable Default Arguments
impact: CRITICAL
tags: python, functions, state
---

## Avoid Mutable Default Arguments

Default arguments are evaluated once when a function is defined. Use `None` or a factory so state
does not leak across calls, tests, or requests.

**Incorrect:**

```python
def add_tag(tag: str, tags: list[str] = []) -> list[str]:
    tags.append(tag)
    return tags
```

**Correct:**

```python
def add_tag(tag: str, tags: list[str] | None = None) -> list[str]:
    result = [] if tags is None else list(tags)
    result.append(tag)
    return result
```

**Compatibility:** Pydantic model defaults have separate copying behavior; this rule covers Python callables.

References:

- [Python FAQ: Shared Default Values](https://docs.python.org/3/faq/programming.html#why-are-default-values-shared-between-objects)


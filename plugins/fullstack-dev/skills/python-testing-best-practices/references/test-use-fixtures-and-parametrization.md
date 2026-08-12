---
title: Use Fixtures and Parametrization Deliberately
impact: HIGH
tags: testing, pytest, fixtures, parametrization
---

## Use Fixtures and Parametrization Deliberately

Let fixtures own setup and teardown with the narrowest practical scope. Use parametrization for the
same behavior over equivalent inputs, give cases readable IDs, and use `pytest.raises(..., match=)`
for precise failure contracts. Avoid mutable session-scoped state and broad autouse fixtures.

**Incorrect:**

```python
users: list[str] = []


def test_create_user() -> None:
    users.append("user@example.com")
    assert users == ["user@example.com"]
```

**Correct:**

```python
from collections.abc import Iterator

import pytest


class UserStore:
    def __init__(self) -> None:
        self.users: set[str] = set()
        self.closed = False

    def create(self, email: str) -> str:
        if "@" not in email:
            raise ValueError("Invalid email")
        self.users.add(email)
        return email

    def close(self) -> None:
        self.closed = True


@pytest.fixture
def store() -> Iterator[UserStore]:
    resource = UserStore()
    try:
        yield resource
    finally:
        resource.close()


@pytest.mark.parametrize(
    "email",
    [
        pytest.param("user@example.com", id="standard-address"),
        pytest.param("person+tag@example.co.uk", id="tagged-address"),
    ],
)
def test_create_user_with_valid_email_returns_email(
    store: UserStore,
    email: str,
) -> None:
    assert store.create(email) == email


@pytest.mark.parametrize(
    "email",
    [
        pytest.param("", id="empty"),
        pytest.param("not-an-email", id="missing-at-sign"),
    ],
)
def test_create_user_with_invalid_email_raises_value_error(
    store: UserStore,
    email: str,
) -> None:
    with pytest.raises(ValueError, match="Invalid email"):
        store.create(email)
```

Keep function scope for mutable resources. Use module or session scope only for expensive immutable
configuration or infrastructure whose state is isolated separately. Parametrized fixtures are useful
when the same contract must run against multiple detected backends; do not pretend unsupported
backends are equivalent.

**Compatibility:** Apply when pytest is installed. Async fixtures must use the async plugin already
selected by the project; FastAPI's current documentation uses AnyIO.

References:

- [pytest: Fixtures](https://docs.pytest.org/en/stable/explanation/fixtures.html)
- [pytest: Safe fixture teardown](https://docs.pytest.org/en/stable/explanation/fixtures.html#safe-teardowns)
- [pytest: Parametrization](https://docs.pytest.org/en/stable/how-to/parametrize.html)
- [pytest: Exception assertions](https://docs.pytest.org/en/stable/how-to/assert.html#assertions-about-expected-exceptions)

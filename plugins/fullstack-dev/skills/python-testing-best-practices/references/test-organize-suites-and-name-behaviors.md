---
title: Organize Suites and Name Observable Behaviors
impact: HIGH
tags: testing, organization, naming, aaa
---

## Organize Suites and Name Observable Behaviors

Separate unit, integration, and end-to-end tests, then mirror application features inside each
level. Name tests as `test_<unit>_<scenario>_<outcome>`, keep Arrange-Act-Assert visible, and test one
observable behavior per test. Multiple assertions are fine when they describe one response or state
transition. Put only genuinely shared fixtures in `conftest.py`; do not hide a test's story there.

For a greenfield service, prefer this shape and omit `tests/__init__.py` unless package imports
actually require it:

```text
tests/
├── conftest.py
├── unit/
│   └── users/test_user_service.py
├── integration/
│   ├── api/test_users.py
│   └── database/test_users.py
└── e2e/
    └── test_user_registration.py
```

**Incorrect:**

```python
def test_user() -> None:
    created = service.create_user({"email": "user@example.com"})
    assert created.id
    updated = service.update_user(created.id, {"email": "new@example.com"})
    assert updated.email == "new@example.com"
```

**Correct:**

```python
def test_create_user_with_valid_email_assigns_id() -> None:
    # Arrange
    data = {"email": "user@example.com"}

    # Act
    created = service.create_user(data)

    # Assert
    assert created.id is not None
    assert created.email == "user@example.com"


def test_update_user_with_new_email_changes_email() -> None:
    existing = service.create_user({"email": "user@example.com"})

    updated = service.update_user(existing.id, {"email": "new@example.com"})

    assert updated.email == "new@example.com"
```

Classify pure services as unit tests, API/database boundaries as integration tests, and only critical
user flows as end-to-end tests. Use `fullstack-dev:test-driven-development` for RED-GREEN-REFACTOR
and `fullstack-dev:performance-optimization` when performance behavior needs measurement.

**Compatibility:** Follow an established repository layout when present. For new projects, pytest
supports a separate `tests/` tree and recommends importlib import mode.

References:

- [pytest: Good Integration Practices](https://docs.pytest.org/en/stable/explanation/goodpractices.html)
- [pytest: Test discovery conventions](https://docs.pytest.org/en/stable/explanation/goodpractices.html#conventions-for-python-test-discovery)

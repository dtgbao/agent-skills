---
title: Register Markers and Enforce Owned Coverage Gates
impact: MEDIUM
tags: testing, markers, coverage, pytest
---

## Register Markers and Enforce Owned Coverage Gates

Register every custom marker and enable strict marker checking. Use markers to select test levels or
resource profiles, not to hide unfinished behavior. A skip must describe an unavailable environment;
a known bug may use `xfail` only with an issue, a narrow expected exception, and `strict=True`.
Measure meaningful coverage and preserve the project's owned threshold instead of inventing 80%.

**Incorrect:**

```python
import pytest


@pytest.mark.skip(reason="Not implemented yet")
def test_create_user() -> None:
    ...


@pytest.mark.slow
def test_everything() -> None:
    ...
```

**Correct:**

```python
import os

import pytest


@pytest.mark.unit
def test_normalize_email_lowercases_domain() -> None:
    assert normalize_email("User@EXAMPLE.COM") == "User@example.com"


@pytest.mark.integration
def test_create_user_enforces_unique_email() -> None:
    assert_unique_email_constraint()


@pytest.mark.skipif(
    os.environ.get("TEST_DATABASE_URL") is None,
    reason="integration database is not configured",
)
@pytest.mark.integration
def test_database_healthcheck_uses_test_database() -> None:
    assert_database_is_reachable()


@pytest.mark.xfail(
    reason="Known bug #123: Unicode local-part normalization",
    raises=UnicodeError,
    strict=True,
)
def test_normalize_email_with_unicode_local_part() -> None:
    normalize_email("δοκιμή@example.com")
```

Register markers and strict behavior in project configuration:

```toml
[tool.pytest.ini_options]
addopts = ["--strict-config", "--strict-markers", "-ra"]
markers = [
  "unit: pure tests without external I/O",
  "integration: tests crossing an application or infrastructure boundary",
  "e2e: critical complete user workflows",
  "slow: tests excluded from the fast local loop",
]
xfail_strict = true
```

When pytest-cov is already installed, keep coverage commands explicit and use the repository-owned
threshold from configuration or CI:

```bash
pytest --cov=app --cov-report=term-missing tests/
pytest --cov=app --cov-report=xml tests/
pytest --cov=app --cov-fail-under=<project-owned-threshold> tests/
```

Coverage is evidence of exercised code, not proof of correct behavior. Raise a threshold deliberately
when meaningful tests justify it; do not add empty tests or exclusions merely to satisfy a percentage.

**Compatibility:** Custom markers require pytest. Coverage flags require pytest-cov and apply only
when detected. Preserve existing marker names and coverage gates in established projects.

References:

- [pytest: Custom markers](https://docs.pytest.org/en/stable/example/markers.html)
- [pytest: Skip and xfail](https://docs.pytest.org/en/stable/how-to/skipping.html)
- [pytest-cov: Configuration](https://pytest-cov.readthedocs.io/en/latest/config.html)
- [Coverage.py: Configuration](https://coverage.readthedocs.io/en/latest/config.html)

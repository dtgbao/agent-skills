---
title: Control Time Environment and Files
impact: HIGH
tags: testing, time, monkeypatch, tmp-path
---

## Control Time Environment and Files

Make clocks injectable, isolate environment changes with `monkeypatch`, and use pytest's `tmp_path`
instead of fixed filesystem locations. When an existing project uses Freezegun, freeze aware UTC
time and keep the frozen scope inside the test.

**Incorrect:**

```python
from datetime import datetime
from pathlib import Path


def create_report() -> None:
    Path("/tmp/report.txt").write_text(str(datetime.utcnow()))
```

**Correct:**

```python
from datetime import UTC, datetime, timedelta
import os
from pathlib import Path
from typing import Protocol

import pytest


class Clock(Protocol):
    def now(self) -> datetime: ...


class FrozenClock:
    def __init__(self, value: datetime) -> None:
        self.value = value

    def now(self) -> datetime:
        return self.value


def token_expiry(clock: Clock, lifetime: timedelta) -> datetime:
    return clock.now() + lifetime


def write_report(directory: Path, content: str) -> Path:
    path = directory / "report.txt"
    path.write_text(content, encoding="utf-8")
    return path


def read_database_url() -> str:
    return os.environ["DATABASE_URL"]


def test_token_expiry_uses_injected_utc_clock() -> None:
    clock = FrozenClock(datetime(2026, 1, 15, 10, 0, tzinfo=UTC))

    expires_at = token_expiry(clock, timedelta(hours=1))

    assert expires_at == datetime(2026, 1, 15, 11, 0, tzinfo=UTC)


def test_write_report_writes_inside_tmp_path(tmp_path: Path) -> None:
    report = write_report(tmp_path, "ready")

    assert report.parent == tmp_path
    assert report.read_text(encoding="utf-8") == "ready"


def test_database_url_uses_scoped_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgresql+asyncpg://localhost/test")
    assert read_database_url().endswith("/test")

    monkeypatch.delenv("DATABASE_URL")
    with pytest.raises(KeyError):
        read_database_url()
```

When Freezegun is already installed or explicitly requested, a complete aware-time test can use:

```python
from datetime import UTC, datetime

from freezegun import freeze_time


def observed_at() -> datetime:
    return datetime.now(UTC)


@freeze_time("2026-01-15T10:00:00+00:00")
def test_observed_at_returns_frozen_aware_utc_time() -> None:
    assert observed_at() == datetime(2026, 1, 15, 10, 0, tzinfo=UTC)
```

Patch the reference the application uses, not the original library definition. Prefer explicit
dependencies over patching globals when the production design is under your control.

**Compatibility:** `tmp_path` and `monkeypatch` require pytest. Freezegun is optional and must be
detected before use. Keep UTC values timezone-aware on Python 3.11+.

References:

- [pytest: Monkeypatching](https://docs.pytest.org/en/stable/how-to/monkeypatch.html)
- [pytest: Temporary paths](https://docs.pytest.org/en/stable/how-to/tmp_path.html)
- [Python: datetime](https://docs.python.org/3/library/datetime.html)
- [Freezegun](https://github.com/spulec/freezegun)

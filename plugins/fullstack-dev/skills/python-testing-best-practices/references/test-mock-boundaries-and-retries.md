---
title: Mock Boundaries and Prove Retry Policies
impact: HIGH
tags: testing, mocks, retries, failures
---

## Mock Boundaries and Prove Retry Policies

Prefer real implementations, then fakes, then mocks. Mock only slow, nondeterministic, paid, or
side-effecting boundaries, constrain mocks with a spec, and patch the name the code under test looks
up. A retry policy needs three tests: transient recovery, exhaustion, and a permanent error that is
not retried.

**Incorrect:**

```python
from unittest.mock import patch


@patch("requests.get")
def test_service(mock_get) -> None:
    service.fetch_user("user-1")
    assert mock_get.called
```

**Correct:**

```python
from typing import Protocol
from unittest.mock import Mock

import pytest


class Client(Protocol):
    def request(self) -> dict[str, str]: ...


class ServiceWithRetry:
    def __init__(self, client: Client, max_attempts: int) -> None:
        self.client = client
        self.max_attempts = max_attempts

    def fetch(self) -> dict[str, str]:
        for attempt in range(1, self.max_attempts + 1):
            try:
                return self.client.request()
            except ConnectionError:
                if attempt == self.max_attempts:
                    raise
        raise AssertionError("retry loop must return or raise")


def test_fetch_after_transient_failures_returns_result() -> None:
    client = Mock(spec=Client)
    client.request.side_effect = [
        ConnectionError("temporary"),
        ConnectionError("temporary"),
        {"status": "ok"},
    ]
    service = ServiceWithRetry(client, max_attempts=3)

    result = service.fetch()

    assert result == {"status": "ok"}
    assert client.request.call_count == 3


def test_fetch_after_max_attempts_reraises_connection_error() -> None:
    client = Mock(spec=Client)
    client.request.side_effect = ConnectionError("offline")
    service = ServiceWithRetry(client, max_attempts=3)

    with pytest.raises(ConnectionError, match="offline") as exc_info:
        service.fetch()

    assert str(exc_info.value) == "offline"
    assert client.request.call_count == 3


def test_fetch_with_permanent_error_does_not_retry() -> None:
    client = Mock(spec=Client)
    client.request.side_effect = ValueError("invalid request")
    service = ServiceWithRetry(client, max_attempts=3)

    with pytest.raises(ValueError, match="invalid request"):
        service.fetch()

    assert client.request.call_count == 1
```

Call-count assertions are appropriate here because the retry count is public policy. For ordinary
business behavior, assert returned state or responses instead of internal call sequences.

**Compatibility:** `Mock` is in the Python standard library. Use `AsyncMock` and awaited assertions
for async boundaries. Follow the retry library's primary documentation when the project uses one.

References:

- [Python: unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
- [Python: Mock side_effect](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock.side_effect)
- [pytest: Exception assertions](https://docs.pytest.org/en/stable/how-to/assert.html#assertions-about-expected-exceptions)

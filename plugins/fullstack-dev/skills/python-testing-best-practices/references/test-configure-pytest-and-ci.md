---
title: Configure Pytest Strictly and Hand Verified Commands to CI
impact: HIGH
tags: testing, pytest, configuration, ci
---

## Configure Pytest Strictly and Hand Verified Commands to CI

Keep discovery, import mode, markers, and default reporting in checked-in pytest configuration.
Run the repository's exact focused and full-suite commands locally, then give those same commands to
CI. Derive the Python matrix from the project's declared support range and route workflow mechanics
to `fullstack-dev:ci-cd-and-automation`; do not copy stale action versions from examples.

**Incorrect:**

```toml
[tool.pytest.ini_options]
addopts = ["-v", "--cov=app", "--cov-fail-under=80"]
```

**Correct:**

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = [
  "--import-mode=importlib",
  "--strict-config",
  "--strict-markers",
  "-ra",
]
markers = [
  "unit: pure tests without external I/O",
  "integration: tests crossing an application or infrastructure boundary",
  "e2e: critical complete user workflows",
  "slow: tests excluded from the fast local loop",
]
xfail_strict = true
```

When coverage.py or pytest-cov is detected, extend the same file with project-owned measurement
settings:

```toml
[tool.coverage.run]
branch = true
source = ["app"]
omit = ["*/migrations/*"]

[tool.coverage.report]
show_missing = true
skip_covered = true
```

Document and reuse commands through the project's existing environment manager:

```bash
pytest tests/unit/users/test_user_service.py -q
pytest tests/unit -q
pytest -m integration
pytest
```

If pytest-cov is not installed, omit coverage configuration and flags. If it is installed, retain the
project's existing threshold and reports. CI must install the project through its lockfile, run the
same commands, use separate test credentials, and test only declared Python versions.

**Compatibility:** `pyproject.toml` configuration requires a supported pytest version. Preserve an
existing `pytest.ini` or dedicated `pytest.toml` rather than migrating configuration without need.
Verify current CI action versions from primary sources when the CI skill creates a workflow.

References:

- [pytest: Configuration](https://docs.pytest.org/en/stable/reference/customize.html)
- [pytest: Good Integration Practices](https://docs.pytest.org/en/stable/explanation/goodpractices.html)
- [pytest: Strict markers](https://docs.pytest.org/en/stable/example/markers.html#registering-markers)
- [Coverage.py: Configuration](https://coverage.readthedocs.io/en/latest/config.html)

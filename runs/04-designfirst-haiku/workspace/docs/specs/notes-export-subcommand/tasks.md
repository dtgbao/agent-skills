# Implementation Plan: notes export subcommand

## Overview

Config first, then exporters, then CLI wiring. Tests follow the code they cover. Checkpoints after each layer. Test leaves that share a file sit in different waves.

## Tasks

- [ ] 1. Setup
  - [ ] 1.1 Add `hypothesis` to dev dependencies in `pyproject.toml`
    - Enables property tests for exporters
    - _Requirements: 1.1, 1.2_

- [ ] 2. Exporters
  - [ ] 2.1 Create `notes/export.py` with `Exporter` protocol, `MarkdownExporter`, `JsonExporter`, `EXPORTERS`
    - `render(notes) -> str` per design
    - _Requirements: 1.1, 1.2_
  - [ ] 2.2 Unit tests for exporters in `tests/test_export.py`
    - Empty list: markdown returns `""`, json returns `[]`
    - _Requirements: 1.3_
  - [ ]* 2.3 Property 1 test in `tests/test_export_properties.py`
    - **Property 1: Markdown has one section per note, in order**
    - **Validates: Requirements 1.1**
    - _Requirements: 1.1_
  - [ ]* 2.4 Property 2 test in `tests/test_export_properties.py`
    - **Property 2: JSON export round-trips the notes**
    - **Validates: Requirements 1.2**
    - _Requirements: 1.2_

- [ ] 3. Checkpoint — run tests, ask user on questions

- [ ] 4. CLI
  - [ ] 4.1 Add `export` subcommand with `--format` (choices from `EXPORTERS`, default `markdown`) in `notes/cli.py`
    - _Requirements: 2.1, 2.2, 2.3_
  - [ ] 4.2 Integration tests in `tests/test_cli_export.py`: `--format json`, default format, unknown format exits 2
    - _Requirements: 2.1, 2.2, 2.3_
  - [ ] 4.3 Integration tests in `tests/test_cli_export.py`: missing notes file prints empty export, invalid JSON exits non-zero
    - _Requirements: 1.4, 1.5_

- [ ] 5. Checkpoint — run tests, ask user on questions

## Notes

- `*` = optional, skip for faster MVP
- Architecture fixed by `README.md`: new formats are exporters in `EXPORTERS`.
- Export is stdout only. `--id` and `--out` are not in scope (see requirements Gaps).

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1"] },
    { "id": 1, "tasks": ["2.1"] },
    { "id": 2, "tasks": ["2.2", "2.3", "4.1"] },
    { "id": 3, "tasks": ["2.4", "4.2"] },
    { "id": 4, "tasks": ["4.3"] }
  ]
}
```

# Requirements Document

## Introduction

The notes CLI gains an `export` subcommand. A user runs it to write all notes to stdout as Markdown or JSON. Scope is limited to what `design.md` supports. Needs the design does not cover are listed under Gaps, not as criteria.

## Glossary

- **Notes CLI**: the `notes` command line program (`python -m notes`).
- **Note**: a stored record with `id`, `title`, `body`, `created_at`.
- **Exporter**: a component that renders a list of Notes into one format string.
- **Export**: the output of the Exporter for the selected format, written to stdout.

## Requirements

### Requirement 1: Export formats

**User Story:** As a notes user, I want all notes exported as Markdown or JSON, so that I can use them in other tools.

#### Acceptance Criteria

1.1. WHEN the format is `markdown`, THE Notes CLI SHALL print one section per Note, in stored order, where each section is the line `## <id>. <title>`, a blank line, the body, a blank line, and `_<created_at>_`.
1.2. WHEN the format is `json`, THE Notes CLI SHALL print a JSON array with one object per Note, where each object has keys `id` (integer), `title` (string), `body` (string), and `created_at` (string).
1.3. IF there are zero Notes, THEN THE Notes CLI SHALL print an empty Markdown document for format `markdown`, and `[]` for format `json`.
1.4. IF the notes file does not exist, THEN THE Notes CLI SHALL print the same output as for zero Notes.
1.5. IF the notes file contains invalid JSON, THEN THE Notes CLI SHALL exit with a non-zero status code.

### Requirement 2: Format selection

**User Story:** As a notes user, I want to choose the export format on the command line, so that I get the format I need.

#### Acceptance Criteria

2.1. WHEN the user runs `notes export --format F`, THE Notes CLI SHALL print the Export in format F, where F is one of `markdown` or `json`.
2.2. WHEN the user runs `notes export` without `--format`, THE Notes CLI SHALL use format `markdown`.
2.3. IF `--format` is not `markdown` or `json`, THEN THE Notes CLI SHALL exit with status 2.

## Gaps

Not in scope. The design does not support these needs. Each needs a design change before requirements can cover it.

- Export one Note by id (`--id N`).
- Write the Export to a file path (`--out PATH`) instead of stdout.

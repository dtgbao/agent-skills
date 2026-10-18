# notes

Notes CLI. `python -m notes add "title" "body"`, `python -m notes list`.
Notes persist in `notes.json` next to the working directory.

## Architecture (fixed)

- `notes/model.py`: `Note` dataclass (id, title, body, created_at ISO-8601).
- `notes/repo.py`: `NoteRepo` loads/saves JSON.
- `notes/cli.py`: argparse subcommands.
- New output formats MUST be plugin-style exporters registered in `EXPORTERS: dict[str, Exporter]`.

Run tests: `uv run --no-project --with pytest --with hypothesis python -m pytest`

import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from notes.model import Note


class NoteRepo:
    def __init__(self, path: Path) -> None:
        self.path = path

    def all(self) -> list[Note]:
        if not self.path.exists():
            return []
        return [Note(**n) for n in json.loads(self.path.read_text())]

    def add(self, title: str, body: str) -> Note:
        notes = self.all()
        note = Note(len(notes) + 1, title, body, datetime.now(timezone.utc).isoformat())
        self.path.write_text(json.dumps([asdict(n) for n in [*notes, note]]))
        return note

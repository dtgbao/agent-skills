from dataclasses import dataclass


@dataclass(frozen=True)
class Note:
    id: int
    title: str
    body: str
    created_at: str

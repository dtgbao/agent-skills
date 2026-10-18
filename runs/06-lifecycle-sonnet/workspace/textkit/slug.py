import re
import unicodedata

MAX_LEN = 50


def slugify(title: str) -> str:
    s = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s[:MAX_LEN].strip("-") or "untitled"


def unique_slug(title: str, existing: set[str]) -> str:
    base = slugify(title)
    if base not in existing:
        return base
    n = 2
    while f"{base}-{n}" in existing:
        n += 1
    return f"{base}-{n}"

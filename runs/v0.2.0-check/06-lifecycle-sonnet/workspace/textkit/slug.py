import re
import unicodedata

MAX_LEN = 40


def slugify(title: str) -> str:
    text = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    text = text[:MAX_LEN].strip("-")
    return text or "untitled"

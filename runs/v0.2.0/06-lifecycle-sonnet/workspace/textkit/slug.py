import re
import unicodedata

MAX_LEN = 40


def slugify(title: str) -> str:
    text = unicodedata.normalize("NFKD", title)
    text = text.encode("ascii", "ignore").decode("ascii").lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text[:MAX_LEN].strip("-")
    return text or "untitled"

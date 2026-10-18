from itertools import count

from textkit.slug import MAX_LEN, slugify


def unique_slug(title: str, existing: set[str]) -> str:
    base = slugify(title)
    if base not in existing:
        return base
    for n in count(2):
        suffix = f"-{n}"
        cand = base[: MAX_LEN - len(suffix)].rstrip("-") + suffix
        if cand not in existing:
            return cand

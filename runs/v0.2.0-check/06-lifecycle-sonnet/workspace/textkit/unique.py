from textkit.slug import MAX_LEN, slugify


def unique_slug(title: str, existing: set[str]) -> str:
    slug = slugify(title)
    if slug not in existing:
        return slug
    n = 2
    while True:
        suffix = f"-{n}"
        candidate = slug[: MAX_LEN - len(suffix)].rstrip("-") + suffix
        if candidate not in existing:
            return candidate
        n += 1

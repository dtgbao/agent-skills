import secrets


class LinkStore:
    """In-memory map of short code -> target URL."""

    def __init__(self) -> None:
        self._links: dict[str, str] = {}

    def create(self, url: str) -> str:
        code = secrets.token_urlsafe(5)
        self._links[code] = url
        return code

    def resolve(self, code: str) -> str | None:
        return self._links.get(code)

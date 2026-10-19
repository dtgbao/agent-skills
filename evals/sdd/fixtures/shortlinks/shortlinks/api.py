from shortlinks.store import LinkStore

VALID_KEYS = {"key-alpha", "key-beta"}


def handle(request: dict, store: LinkStore) -> dict:
    """request = {"method", "path", "api_key", "body"} -> {"status", "headers", "body"}"""
    if request.get("api_key") not in VALID_KEYS:
        return {"status": 401, "headers": {}, "body": {"error": "unauthorized"}}

    if request["method"] == "POST" and request["path"] == "/links":
        url = request.get("body", {}).get("url", "")
        if not url.startswith(("http://", "https://")):
            return {"status": 400, "headers": {}, "body": {"error": "invalid url"}}
        return {"status": 201, "headers": {}, "body": {"code": store.create(url)}}

    if request["method"] == "GET" and request["path"].startswith("/links/"):
        target = store.resolve(request["path"].removeprefix("/links/"))
        if target is None:
            return {"status": 404, "headers": {}, "body": {"error": "not found"}}
        return {"status": 302, "headers": {"Location": target}, "body": {}}

    return {"status": 404, "headers": {}, "body": {"error": "no route"}}

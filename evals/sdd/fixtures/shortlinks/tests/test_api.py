from shortlinks.api import handle
from shortlinks.store import LinkStore


def test_create_and_resolve():
    store = LinkStore()
    created = handle({"method": "POST", "path": "/links", "api_key": "key-alpha", "body": {"url": "https://x.dev"}}, store)
    assert created["status"] == 201
    code = created["body"]["code"]
    got = handle({"method": "GET", "path": f"/links/{code}", "api_key": "key-alpha"}, store)
    assert got["status"] == 302 and got["headers"]["Location"] == "https://x.dev"


def test_rejects_bad_key():
    assert handle({"method": "GET", "path": "/links/x", "api_key": "nope"}, LinkStore())["status"] == 401

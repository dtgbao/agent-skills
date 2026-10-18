from shop.cart import Cart
from shop.inventory import OutOfStock


def handle(request: dict, ctx: dict) -> dict:
    """request = {"method", "path", "body"}; ctx = {"carts": {id: Cart}, "inventory": Inventory}"""
    method, path, body = request["method"], request["path"], request.get("body", {})
    if method == "POST" and path == "/carts":
        cart_id = str(len(ctx["carts"]) + 1)
        ctx["carts"][cart_id] = Cart(ctx["inventory"])
        return {"status": 201, "body": {"cart_id": cart_id}}
    if path.startswith("/carts/"):
        cart = ctx["carts"].get(path.split("/")[2])
        if cart is None:
            return {"status": 404, "body": {"error": "no cart"}}
        if method == "POST" and path.endswith("/lines"):
            try:
                cart.add(body["sku"], int(body["qty"]))
            except KeyError:
                return {"status": 400, "body": {"error": "unknown sku"}}
            except ValueError:
                return {"status": 400, "body": {"error": "bad qty"}}
            except OutOfStock:
                return {"status": 409, "body": {"error": "out of stock"}}
            return {"status": 200, "body": {"subtotal_cents": cart.subtotal_cents()}}
        if method == "GET":
            return {"status": 200, "body": {"lines": cart.lines, "subtotal_cents": cart.subtotal_cents()}}
    return {"status": 404, "body": {"error": "no route"}}

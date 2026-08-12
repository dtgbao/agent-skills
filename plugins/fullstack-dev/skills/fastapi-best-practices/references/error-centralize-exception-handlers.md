---
title: Centralize Exception Mapping and Unhandled Errors
impact: CRITICAL
tags: errors, domain, validation, exception-handlers, logging
---

## Centralize Exception Mapping and Unhandled Errors

Register specific exception handlers that translate domain and request-validation failures into
stable API responses, plus one application-level `Exception` handler that logs unexpected failures
and returns a generic 500 response. Keep business code independent of HTTP status codes, and never
expose unexpected exception details or tracebacks to clients.

**Incorrect:**

```python
from fastapi import Request
from fastapi.responses import JSONResponse

async def endpoint(request: Request) -> JSONResponse:
    try:
        reserve_stock()
    except Exception as exc:
        return JSONResponse(status_code=500, content={"detail": str(exc)})
```

**Correct:**

```python
import logging
from datetime import UTC, datetime

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class OutOfStock(Exception):
    pass


app = FastAPI(debug=False)


@app.exception_handler(OutOfStock)
async def handle_out_of_stock(_: Request, __: OutOfStock) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": "Out of stock"},
    )


@app.exception_handler(RequestValidationError)
async def handle_request_validation_error(
    _: Request,
    exception: RequestValidationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"details": exception.errors()}),
    )


@app.exception_handler(Exception)
async def handle_unexpected_exception(
    request: Request,
    _exception: Exception,
) -> JSONResponse:
    logger.exception(
        "Unhandled request exception",
        extra={
            "method": request.method,
            "path": request.url.path,
        },
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": "Internal server error",
            "timestamp": datetime.now(UTC).isoformat(),
        },
    )
```

FastAPI's more-specific handlers for `HTTPException`, validation failures, and registered domain
exceptions take precedence over the `Exception` handler. Configure one owner for unexpected-error
logging to avoid duplicate stack traces. Do not log unredacted query strings, headers, or bodies.
`RequestValidationError.body` is useful for local diagnosis, but do not return or log it wholesale
in production because it can contain credentials and other sensitive input.

**Compatibility:** With Starlette `TestClient`, set `raise_server_exceptions=False` to assert the
500 response. With HTTPX `ASGITransport`, set `raise_app_exceptions=False`. A background-task
exception can occur after the response is sent, so the replacement response is discarded and the
task must report its own failure.

References:

- [FastAPI: Install Custom Exception Handlers](https://fastapi.tiangolo.com/tutorial/handling-errors/#install-custom-exception-handlers)
- [Starlette: Exceptions](https://www.starlette.io/exceptions/)
- [Starlette: TestClient](https://www.starlette.io/testclient/)
- [HTTPX: ASGI transport](https://www.python-httpx.org/advanced/transports/#asgi-transport)

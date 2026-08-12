---
title: Declare Status and Error Contracts
impact: HIGH
tags: api, openapi, responses
---

## Declare Status and Error Contracts

Set the success status explicitly and document meaningful alternative responses. Keep runtime
exception mappings aligned with the generated OpenAPI contract.

**Incorrect:**

```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/items")
def create_item() -> dict[str, int]:
    return {"id": 1}
```

**Correct:**

```python
from fastapi import FastAPI, status

app = FastAPI()

@app.post(
    "/items",
    status_code=status.HTTP_201_CREATED,
    responses={409: {"description": "Item already exists"}},
)
def create_item() -> dict[str, int]:
    return {"id": 1}
```

**Compatibility:** Add response models for structured errors when the API contract requires them.

References:

- [FastAPI: Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/)
- [FastAPI: Additional Responses in OpenAPI](https://fastapi.tiangolo.com/advanced/additional-responses/)


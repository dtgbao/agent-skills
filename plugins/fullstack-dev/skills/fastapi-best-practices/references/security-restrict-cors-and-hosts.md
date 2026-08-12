---
title: Restrict CORS Origins and Host Headers
impact: HIGH
tags: security, cors, hosts
---

## Restrict CORS Origins and Host Headers

List trusted browser origins explicitly when credentials are enabled, and validate host headers at
the application or trusted proxy boundary.

**Incorrect:**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True)
```

**Correct:**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["https://app.example.com"], allow_credentials=True)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["api.example.com"])
```

**Compatibility:** Credentialed CORS requires explicit origins, methods, and headers when configured.

References:

- [FastAPI: CORS](https://fastapi.tiangolo.com/tutorial/cors/)
- [FastAPI: Advanced Middleware](https://fastapi.tiangolo.com/advanced/middleware/)


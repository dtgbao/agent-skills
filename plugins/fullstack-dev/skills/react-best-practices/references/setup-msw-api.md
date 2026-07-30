---
title: Setup MSW API Mocks
impact: MEDIUM
impactDescription: gives data-backed tests realistic network boundaries
tags: setup, testing, msw, api
---

# Setup MSW API Mocks

Use this when adding a mock API server for data-backed React tests. Keep the
server in `tests/mocks/api` and start it from `tests/setup.ts`.

## Folder Shape

```txt
tests/mocks/api/
  index.ts        # creates and exports the server
  orders.ts       # domain handlers and test helpers
```

Use one handler file per API domain. Export test helpers beside the handlers
when tests need to inspect or change mock state.

## Server Entry

```ts
// tests/mocks/api/index.ts
import { setupServer } from "msw/node";
import { orderHandlers } from "./orders";

const handlers = [...orderHandlers];

export const server = setupServer(...handlers);
```

## Domain Handlers

```ts
// tests/mocks/api/orders.ts
import { http, HttpResponse } from "msw";

let createOrderRequests: Array<{ productId: string; quantity: number }> = [];

export function resetOrderApiState() {
  createOrderRequests = [];
}

export function getCreateOrderRequests() {
  return createOrderRequests;
}

export const orderHandlers = [
  http.get("*/products", () => HttpResponse.json([])),
  http.post("*/orders", async ({ request }) => {
    const body = (await request.json()) as {
      productId: string;
      quantity: number;
    };
    createOrderRequests.push(body);

    return HttpResponse.json({ id: "order-1" }, { status: 201 });
  }),
];
```

Use wildcard origins such as `"*/products"` when tests should not care which base
URL the app reads from environment variables.

## Lifecycle

Wire the server once in `tests/setup.ts`:

```ts
import { server } from "@tests/mocks/api";

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

Use `server.use(...)` inside a test for one-off failures or edge cases. Use
domain reset helpers for state the handlers own.

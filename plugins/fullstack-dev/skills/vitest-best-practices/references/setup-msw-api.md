---
title: Setup MSW API Mocks
impact: MEDIUM
impactDescription: gives data-backed tests realistic network boundaries
tags: setup, testing, msw, api
---

# Setup MSW API Mocks

Use this when adding a mock API server for data-backed component tests. Reuse the repository's mock
location when one exists; otherwise, keep the server in `tests/mocks/api` and start it from
`tests/setup.ts`.

## Folder Shape

```txt
tests/mocks/api/
  index.ts        # creates and exports the server
  orders.ts       # domain handlers
```

Use one handler file per API domain. Model the server contract in handlers instead of recording
requests for later assertions.

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

export const orderHandlers = [
  http.get("*/products", () => HttpResponse.json([])),
  http.post("*/orders", async ({ request }) => {
    const body = (await request.json()) as Partial<{
      productId: string;
      quantity: number;
    }>;

    if (!body.productId || typeof body.quantity !== "number" || body.quantity <= 0) {
      return HttpResponse.json(
        { message: "productId and quantity are required" },
        { status: 400 },
      );
    }

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

beforeAll(() => server.listen({ onUnhandledRequest: "error" }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

The `onUnhandledRequest` policy prevents missing handlers from reaching the real network. Use
`server.use(...)` inside a test for one-off failures or edge cases. `resetHandlers()` removes those
runtime overrides after each test.

Assert how the application reacts to a valid or invalid response. Do not assert that a handler was
called or accumulate request bodies as the default testing strategy. For one-way effects with no
observable application result, such as analytics, use MSW lifecycle events for a focused request
assertion.

## Sources

- [MSW Node.js test-runner integration](https://mswjs.io/docs/integrations/node/)
- [MSW network behavior overrides](https://mswjs.io/docs/best-practices/network-behavior-overrides)
- [MSW guidance against request assertions](https://mswjs.io/docs/best-practices/avoid-request-assertions)

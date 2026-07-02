# Setup MSW API Mocks

Use this when adding a mock API server for data-backed React tests. Keep the
server in `tests/mocks/api` and start it from `tests/setup.ts`.

## Folder Shape

```txt
tests/mocks/api/
  index.ts        # creates and exports the server
  dogs.ts         # domain handlers and test helpers
```

Use one handler file per API domain. Export test helpers beside the handlers
when tests need to inspect or change mock state.

## Server Entry

```ts
// tests/mocks/api/index.ts
import { setupServer } from "msw/node";
import { dogHandlers } from "./dogs";

const handlers = [...dogHandlers];

export const server = setupServer(...handlers);
```

## Domain Handlers

```ts
// tests/mocks/api/dogs.ts
import { http, HttpResponse } from "msw";

let voteRequests: Array<{ image_id: string; sub_id: string; value: number }> = [];

export function resetDogApiState() {
  voteRequests = [];
}

export function getVoteRequests() {
  return voteRequests;
}

export const dogHandlers = [
  http.get("*/breeds", () => HttpResponse.json([])),
  http.post("*/votes", async ({ request }) => {
    const body = (await request.json()) as {
      image_id: string;
      sub_id: string;
      value: number;
    };
    voteRequests.push(body);

    return HttpResponse.json({ message: "SUCCESS" }, { status: 201 });
  }),
];
```

Use wildcard origins such as `"*/breeds"` when tests should not care which base
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

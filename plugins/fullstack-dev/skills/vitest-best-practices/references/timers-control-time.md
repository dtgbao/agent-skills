---
title: Control Time Locally
impact: MEDIUM
impactDescription: makes time-dependent tests fast and deterministic
tags: testing, vitest, timers, dates, user-event
---

## Control Time Locally

Use fake timers only in the suite that needs them. Set the system time when calendar behavior
matters, advance only the required duration, and restore real timers after every test.

**Incorrect (real delay and leaked fake timers):**

```ts
test("dismisses the toast", async () => {
  render(<Toast />);
  await new Promise((resolve) => setTimeout(resolve, 5_000));
  expect(screen.queryByRole("status")).not.toBeInTheDocument();
});
```

**Correct (controlled time):**

```ts
import { afterEach, beforeEach, expect, test, vi } from "vitest";

beforeEach(() => {
  vi.useFakeTimers();
});

afterEach(() => {
  vi.useRealTimers();
});

test("dismisses the toast", async () => {
  render(<Toast />);

  await vi.advanceTimersByTimeAsync(5_000);

  expect(screen.queryByRole("status")).not.toBeInTheDocument();
});
```

When `user-event` and fake timers are used together, pass the timer advancement function to setup:

```ts
const user = userEvent.setup({ advanceTimers: vi.advanceTimersByTime });
```

Do not set `delay: null` to bypass `user-event` timing. Advance timers through the supported option
so interactions keep their event ordering. Avoid `runAllTimers` for recursive timers; advance to the
next timer or a bounded duration instead.

## Sources

- [Vitest timer mocking](https://vitest.dev/guide/mocking/timers)
- [Vitest date mocking](https://vitest.dev/guide/mocking/dates.html)
- [Testing Library user-event options](https://testing-library.com/docs/user-event/options/#advancetimers)

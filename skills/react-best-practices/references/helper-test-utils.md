---
title: React Test Render Helpers
impact: MEDIUM
impactDescription: keeps provider and router test setup consistent when copied
tags: helper, testing, react-testing-library, router
---

# React Test Render Helpers

Copy this shape when tests need shared app providers or router-level rendering.
Adapt providers, routes, imports, and query defaults to the target project.

## `tests/test-utils.tsx`

```tsx
import React, { type ReactElement, useState } from "react";
import { render, type RenderOptions } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { createMemoryRouter, RouterProvider } from "react-router-dom";
import { routes } from "@/app/router/routes";

const AllTheProviders = ({ children }: { children: React.ReactNode }) => {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            retry: false,
            refetchOnWindowFocus: false,
            refetchOnReconnect: false,
          },
          mutations: {
            retry: false,
          },
        },
      }),
  );
  return <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>;
};

export const renderWithProviders = (ui: ReactElement, options?: Omit<RenderOptions, "wrapper">) =>
  render(ui, { wrapper: AllTheProviders, ...options });

export const renderPage = (initialEntry = "/", options?: Omit<RenderOptions, "wrapper">) => {
  const router = createMemoryRouter(routes, {
    initialEntries: [initialEntry],
  });
  const result = render(<RouterProvider router={router} />, {
    wrapper: AllTheProviders,
    ...options,
  });

  return {
    ...result,
    router,
  };
};
```

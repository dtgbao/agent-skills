---
title: Use Plain API Functions
impact: HIGH
impactDescription: keeps endpoint behavior reusable and easy to test
tags: data, api, fetch, tanstack-query, hooks
---

## Use Plain API Functions

Expose API calls as plain functions over the project's existing HTTP client.
Then wrap those functions in framework-specific hooks such as TanStack Query,
SWR, React Router loaders, or server actions.

**Incorrect:**

```ts
export function createProductsApi(client: HttpClient) {
  return {
    getProducts(page: number) {
      return client.get<Product[]>(`/products?page=${page}`);
    },
  };
}
```

**Correct:**

```ts
export function getProducts(params: ProductsQuery) {
  return client.get<Product[]>("/products", { searchParams: params }).json();
}

export function productsQueryOptions(params: ProductsQuery) {
  return queryOptions({
    queryKey: ["products", params],
    queryFn: () => getProducts(params),
  });
}
```

Add an API factory only when the app has multiple real client instances or
runtime-injected transports. Otherwise, plain functions are enough.

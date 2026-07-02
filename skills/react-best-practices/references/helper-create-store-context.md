# Scoped Store Context Helper

Copy this shape when a feature needs one Zustand store instance per provider.
Adapt names, imports, and store setup to the target project.

## `src/shared/utils/create-store-context.tsx`

```tsx
import { type ReactNode, createContext, use, useState } from "react";
import { useStore, type StoreApi } from "zustand";

export default function createStoreContext<Store>(createStore: () => StoreApi<Store>) {
  const Context = createContext<ReturnType<typeof createStore> | null>(null);

  function useStoreContext<U>(selector: (state: Store) => U) {
    const store = use(Context);
    if (store === null) {
      throw new Error("useStoreContext must be used within Provider");
    }
    return useStore(store, selector);
  }

  function Provider({ children }: { children: ReactNode }) {
    const [store] = useState(() => createStore());
    return <Context value={store}>{children}</Context>;
  }

  return [Provider, useStoreContext] as const;
}
```

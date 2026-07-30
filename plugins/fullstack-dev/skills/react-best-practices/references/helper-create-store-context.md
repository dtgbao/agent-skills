---
title: Scoped Store Context Helper
impact: MEDIUM
impactDescription: keeps one store instance per provider when copied
tags: helper, state, zustand, context
---

# Scoped Store Context Helper

Copy this shape when a feature needs one Zustand store instance per provider.
Adapt names, imports, and store setup to the target project.

## `src/shared/utils/create-store-context.tsx`

```tsx
import { type ReactNode, createContext, use, useState } from "react";
import { useStore, type ExtractState, type StoreApi } from "zustand";

type StoreCreator = (...args: any[]) => StoreApi<unknown>;

type ProviderProps<TCreateStore extends StoreCreator> = {
	children: ReactNode;
} & (Parameters<TCreateStore> extends []
	? { initialValue?: never }
	: { initialValue?: Parameters<TCreateStore>[0] });

export default function createStoreContext<TCreateStore extends StoreCreator>(
	createStore: TCreateStore,
) {
	type Store = ExtractState<ReturnType<TCreateStore>>;
	const Context = createContext<ReturnType<TCreateStore> | null>(null);

	function useStoreContext<U>(selector: (state: Store) => U) {
		const store = use(Context);
		if (store === null) {
			throw new Error("useStoreContext must be used within Provider");
		}
		return useStore(store, selector);
	}

	function Provider({ children, initialValue }: ProviderProps<TCreateStore>) {
		const [store] = useState<ReturnType<TCreateStore>>(
			() =>
				(initialValue === undefined
					? createStore()
					: createStore(initialValue)) as ReturnType<TCreateStore>,
		);
		return <Context value={store}>{children}</Context>;
	}

	return [Provider, useStoreContext] as const;
}
```

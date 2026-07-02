---
title: Scope Providers to State Owners
impact: HIGH
impactDescription: shares state where needed without leaking it app-wide
tags: state, context, routing, providers
---

## Scope Providers to State Owners

Place providers at the smallest boundary that owns the state. Use a route or
layout provider for sibling pages, a feature provider for feature-only state,
and an app provider only for truly global concerns.

State should be lifted only as far as consumers require. If siblings or route
children need shared access, put the provider above those siblings. If only one
surface needs the state, keep it inside that surface's provider hook.

**Incorrect (provider too high):**

```tsx
// App-wide because it was convenient.
function App() {
  return (
    <CheckoutProvider>
      <Router />
    </CheckoutProvider>
  );
}
```

**Incorrect (UI coupled to store implementation):**

```tsx
function ShippingAddressField() {
  const address = useCheckoutZustandStore((state) => state.address);
  const saveToServer = useCheckoutSyncMutation();

  return <AddressInput value={address} onChange={(value) => saveToServer(value)} />;
}
```

Child UI should consume the provider's public hook. The provider decides whether
state comes from `useState`, Zustand, URL state, query cache, or server sync.

**Incorrect (syncing state upward with effects):**

```tsx
function CheckoutLayout() {
  const [address, setAddress] = useState("");

  return <ShippingForm onAddressChange={setAddress} />;
}

function ShippingForm({ onAddressChange }: Props) {
  const [address, setAddress] = useState("");

  useEffect(() => {
    onAddressChange(address);
  }, [address, onAddressChange]);
}
```

If the parent needs the state, the parent owns the provider. Do not mirror child
state upward with effects.

**Correct:**

```tsx
function CheckoutLayout() {
  return (
    <CheckoutProvider>
      <Outlet />
    </CheckoutProvider>
  );
}

function ShippingPage() {
  const { setAddress } = useCheckout();
  //For Zustand scoped stores:
  //const setAddress = useCheckoutStore((state) => state.setAddress);
}
```

Prefer explicit actions such as `setAddress`, `nextStep`, or `addItem`. Add a
generic state setter only when multiple call sites need full-state replacement.

When a project needs reusable provider wiring, consider these helper shapes:
`references/helper-create-context.md` for hook-backed providers and
`references/helper-create-store-context.md` for scoped Zustand stores.

Keep UI parts decoupled from the implementation. Child components should consume
the provider's public hook instead of importing `useState`, Zustand stores, or
server-sync hooks directly unless they own that state boundary.

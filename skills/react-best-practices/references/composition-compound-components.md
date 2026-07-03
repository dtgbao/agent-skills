---
title: Use Compound Components for Complex Surfaces
impact: CRITICAL
impactDescription: shares state without prop drilling or boolean prop sprawl
tags: composition, components, context, architecture
---

## Use Compound Components for Complex Surfaces

When multiple pieces of one UI surface need the same state or actions, expose a
root provider plus named child parts scoped under one object. Let consumers
compose the pieces they need instead of adding boolean mode props to one large
component.

Prefer the hook-backed provider pattern: write a hook that owns the behavior,
export the generated provider and consumer hook, and keep child parts dependent
on that consumer hook.

**Incorrect:**

```tsx
function ProductCard({ product, compact, showActions, onFavorite }: Props) {
  const [isFavorite, setIsFavorite] = useState(false);

  return (
    <Card data-compact={compact}>
      <ProductImage product={product} />
      {showActions ? (
        <FavoriteButton
          value={isFavorite}
          onChange={() => {
            setIsFavorite(true);
            onFavorite(product.id);
          }}
        />
      ) : null}
    </Card>
  );
}
```

**Correct:**

```tsx
function useProductCardState({ product, onFavorite }: ProductCardProps) {
  const [isFavorite, setIsFavorite] = useState(false);

  return {
    product,
    isFavorite,
    favorite() {
      setIsFavorite(true);
      onFavorite(product.id);
    },
  };
}

const [ProductCardProvider, useProductCard] = createContext(useProductCardState);

function ProductCardFrame({ children }: PropsWithChildren) {
  return <Card>{children}</Card>;
}

function ProductCardMedia() {
  const { product } = useProductCard();
  return <img alt="" src={product.imageUrl} />;
}

function ProductCardActions() {
  const { favorite } = useProductCard();
  return <Button onPress={favorite}>Favorite</Button>;
}

function ProductCardDetails() {
  const { product } = useProductCard();
  return <ProductDetails product={product} />;
}

export const ProductCard = Object.assign(ProductCardProvider, {
  Frame: ProductCardFrame,
  Media: ProductCardMedia,
  Details: ProductCardDetails,
  Actions: ProductCardActions,
});

function ProductPage() {
  return (
    <ProductCard product={product} onFavorite={trackFavorite}>
      <ProductCard.Frame>
        <ProductCard.Media />
        <ProductCard.Details />
      </ProductCard.Frame>
      <ProductCard.Actions />
    </ProductCard>
  );
}
```

Use compound components when the variants share real internals. Keep one-off
layout in the consuming page or feature component. If the component is a public
library API, a `state/actions/meta` context interface can help dependency
injection; for app code, the generated provider hook is usually enough.

Read `references/helper-create-context.md` only when copying the helper source.

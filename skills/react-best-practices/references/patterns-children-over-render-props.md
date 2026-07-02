---
title: Prefer Composing Children Over Render Props
impact: MEDIUM
impactDescription: cleaner composition, better readability
tags: composition, children, render-props
---

## Prefer Children Over Render Props

Use `children` for composition instead of `renderX` props. Children are more
readable, compose naturally, and don't require understanding callback
signatures.

**Incorrect (render props):**

```tsx
function Composer({
  renderHeader,
  renderFooter,
  renderActions,
}: {
  renderHeader?: () => React.ReactNode;
  renderFooter?: () => React.ReactNode;
  renderActions?: () => React.ReactNode;
}) {
  return (
    <form>
      {renderHeader?.()}
      <Input />
      {renderFooter ? renderFooter() : <DefaultFooter />}
      {renderActions?.()}
    </form>
  );
}

return (
  <Composer
    renderHeader={() => <CustomHeader />}
    renderFooter={() => (
      <>
        <Formatting />
        <Emojis />
      </>
    )}
    renderActions={() => <SubmitButton />}
  />
);
```

**Correct (compound components with children):**

```tsx
function ComposerFrame({ children }: { children: React.ReactNode }) {
  return <form>{children}</form>;
}

function ComposerHeader() {
  return <header>Custom header</header>;
}

function ComposerFooter({ children }: { children: React.ReactNode }) {
  return <footer className="flex">{children}</footer>;
}

function ComposerSubmit() {
  return <SubmitButton />;
}

const Composer = Object.assign(ComposerFrame, {
  Header: ComposerHeader,
  Footer: ComposerFooter,
  Input: ComposerInput,
  Formatting: ComposerFormatting,
  Emojis: ComposerEmojis,
  Submit: ComposerSubmit,
});

return (
  <Composer>
    <Composer.Header />
    <Composer.Input />
    <Composer.Footer>
      <Composer.Formatting />
      <Composer.Emojis />
      <Composer.Submit />
    </Composer.Footer>
  </Composer>
);
```

Render props are appropriate when the parent needs to provide data or state to
the child, such as `renderItem={({ item }) => <Item item={item} />}`. Use
children when composing static structure.

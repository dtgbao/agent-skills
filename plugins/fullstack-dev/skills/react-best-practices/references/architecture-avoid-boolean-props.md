---
title: Avoid Boolean Prop Proliferation
impact: CRITICAL
impactDescription: prevents unmaintainable component variants
tags: composition, props, architecture
---

## Avoid Boolean Prop Proliferation

Don't add boolean props like `isThread`, `isEditing`, `isDMThread` to customize
component behavior. Each boolean doubles possible states and creates
unmaintainable conditional logic. Use explicit variants or composition instead.

**Incorrect (boolean props create exponential complexity):**

```tsx
function Composer({
	onSubmit,
	isThread,
	channelId,
	isDMThread,
	dmId,
	isEditing,
	isForwarding,
}: Props) {
	return (
		<form>
			<Header />
			<Input />
			{isDMThread ? (
				<AlsoSendToDMField id={dmId} />
			) : isThread ? (
				<AlsoSendToChannelField id={channelId} />
			) : null}
			{isEditing ? <EditActions /> : isForwarding ? <ForwardActions /> : <DefaultActions />}
			<Footer onSubmit={onSubmit} />
		</form>
	);
}
```

**Correct (explicit variants compose the pieces they need):**

```tsx
const Composer = Object.assign(ComposerFrame, {
	Header: ComposerHeader,
	Input: ComposerInput,
	Footer: ComposerFooter,
	Attachments: ComposerAttachments,
	Formatting: ComposerFormatting,
	Emojis: ComposerEmojis,
	Submit: ComposerSubmit,
	CancelEdit: ComposerCancelEdit,
	SaveEdit: ComposerSaveEdit,
});

function ChannelComposer() {
	return (
		<Composer>
			<Composer.Header />
			<Composer.Input />
			<Composer.Footer>
				<Composer.Attachments />
				<Composer.Formatting />
				<Composer.Emojis />
				<Composer.Submit />
			</Composer.Footer>
		</Composer>
	);
}

function ThreadComposer({ channelId }: { channelId: string }) {
	return (
		<Composer>
			<Composer.Header />
			<Composer.Input />
			<AlsoSendToChannelField id={channelId} />
			<Composer.Footer>
				<Composer.Formatting />
				<Composer.Emojis />
				<Composer.Submit />
			</Composer.Footer>
		</Composer>
	);
}

function EditComposer() {
	return (
		<Composer>
			<Composer.Input />
			<Composer.Footer>
				<Composer.Formatting />
				<Composer.Emojis />
				<Composer.CancelEdit />
				<Composer.SaveEdit />
			</Composer.Footer>
		</Composer>
	);
}
```

Each variant is explicit about what it renders. If variants share state or actions across named child parts, use `composition-compound-components.md`.

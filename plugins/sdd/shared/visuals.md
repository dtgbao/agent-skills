# Design visuals

Show shape, not prose. Pick the smallest view that makes the point. Use `diff` when the surrounding shape exists. Show a whole block when most of it is new. Keep only the calls, files, props, and states the reader needs.

| Change | View | Fence |
|---|---|---|
| File layout | shallow file tree, one-line role per entry | `diff` |
| UI structure | component tree with state and module boundaries | `diff` |
| Runtime control flow | call tree. Call-stack change: mark added and removed calls | `diff` |
| State or branching logic | pseudocode | `diff` |
| Actor or service interaction | sequence diagram | `mermaid` |

File layout:

```diff
 src/
 ├── commands/
+│   └── show-me.ts       # expands the slash command
-└── transport.ts
+└── transport/
+    ├── client.ts
+    └── stream.ts
```

Component tree:

```diff
 <SessionPage> (routes/session.tsx)
   useSessionEvents()
   <SessionToolbar>
+    <RunSkillButton />
```

Call tree or call-stack change:

```diff
 submitForm
   createSession
     persistPrompt
+    expandSkillMention
     launchAgent
-  navigateToSession
+  navigateToSession
+    subscribeToEvents
```

State or control flow:

```diff
 on(save)
-  write content
+  if content is unchanged
+    return cached result
+  write new content
+  invalidate cache
```

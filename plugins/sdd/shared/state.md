# Spec state

Spec dir: `docs/specs/<name>/`. State file: `docs/specs/<name>/.spec.json`.

```json
{
  "name": "<name>",
  "workflow": "requirements-first | design-first | bugfix | quick-plan",
  "order": ["requirements", "design", "tasks"],
  "phases": { "requirements": "pending", "design": "pending", "tasks": "pending" }
}
```

- `order`: requirements-first, bugfix, quick-plan → `requirements, design, tasks`. design-first → `design, requirements, tasks`.
- `requirements` phase file: `requirements.md`, or `bugfix.md` when workflow = bugfix.
- Phase values: `pending` → `draft` → `approved`. `stale` = upstream edited after approval.
- `workflow` fixed for spec life. Change needed → new spec, copy content.
- Edit approved artifact → every later phase in `order` becomes `stale`. `/spec-sync` clears `stale`.
- Writers: spec skills only. Agents read.

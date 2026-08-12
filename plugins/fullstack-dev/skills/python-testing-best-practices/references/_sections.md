# Sections

Use this order when several testing concerns apply.

| Order | Section | Prefix | Impact | Purpose |
| --- | --- | --- | --- | --- |
| 1 | Organization & Behavior | `test` | HIGH | Make suite boundaries and expected behavior easy to understand. |
| 2 | Fixtures & Isolation | `test` | HIGH | Control state, teardown, boundaries, retries, time, environment, and files. |
| 3 | FastAPI Application Tests | `fastapi` | HIGH | Exercise ASGI behavior, dependencies, and application lifespan. |
| 4 | Advanced Techniques | `test` | MEDIUM-HIGH | Apply markers, coverage, properties, and database integration deliberately. |
| 5 | Configuration & CI | `test` | MEDIUM | Keep discovery strict and provide verified commands to automation. |

Apply framework, ORM, coverage, and optional ecosystem rules only when those tools are detected in
the project. Preserve the invariant and follow the detected tool's official documentation when the
implementation differs from an example.

# Sections

Use this order when several concerns apply.

| Order | Section | Prefix | Impact | Purpose |
| --- | --- | --- | --- | --- |
| 1 | Architecture | `arch` | CRITICAL | Keep packages, routers, imports, and resource ownership coherent. |
| 2 | Python Design | `python` | CRITICAL | Use language features that make boundaries explicit and safe. |
| 3 | Dependency Injection | `di` | CRITICAL | Make request dependencies visible, scoped, and replaceable. |
| 4 | Error Handling | `error` | HIGH | Preserve failure meaning and produce consistent HTTP responses. |
| 5 | Security | `security` | HIGH | Validate trust boundaries and prevent data or credential exposure. |
| 6 | Async & Performance | `async`, `perf` | HIGH | Protect the event loop and bound concurrent work. |
| 7 | Database | `db` | MEDIUM-HIGH | Scope stateful sessions and make database work explicit. |
| 8 | API Design | `api` | MEDIUM | Maintain stable, documented request and response contracts. |
| 9 | Operations | `ops` | MEDIUM | Validate runtime configuration and support safe deployments. |

Apply ORM-, queue-, server-, and test-library rules only when those components are detected in the
project. For a different implementation, preserve the invariant and follow that tool's official
documentation.

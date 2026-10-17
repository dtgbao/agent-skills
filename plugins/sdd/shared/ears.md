# EARS criteria

Pattern per criterion. Subject = Glossary term.

| Pattern | Form |
|---|---|
| Ubiquitous | THE <System> SHALL <response> |
| Event | WHEN <trigger>, THE <System> SHALL <response> |
| State | WHILE <state>, THE <System> SHALL <response> |
| Unwanted | IF <condition>, THEN THE <System> SHALL <response> |
| Optional | WHERE <feature included>, THE <System> SHALL <response> |
| Complex | WHILE <state>, WHEN <trigger>, THE <System> SHALL <response> |

Bugfix forms:

| Section | Form |
|---|---|
| Current | WHEN <condition> THEN the system <incorrect behavior> |
| Expected | WHEN <condition> THE SYSTEM SHALL <correct behavior> |
| Unchanged | WHEN <condition> THE SYSTEM SHALL CONTINUE TO <existing behavior> |

Rules:
- One behavior per criterion.
- One observable assertion per criterion (test can fail on it).
- Numbers carry unit and bound ("within 2 seconds", "1–50 characters").

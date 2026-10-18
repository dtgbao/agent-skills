# requirements.md

Criteria in `${CLAUDE_PLUGIN_ROOT}/shared/ears.md`.

Done when:
- one requirement = one capability a user or operator observes; 2–7 criteria each
- criteria numbered `1.`, `2.` per requirement, cited elsewhere as `N.M`
- every criterion matches one EARS pattern: one `SHALL`, ≤40 words, one observable assertion
- every system/actor term in Glossary
- every input has bound or format (length, range, type)
- every requirement that takes input or calls a dependency has ≥1 failure or edge criterion (invalid input, dependency down, empty, concurrent)
- zero unmeasured adjectives ("fast", "secure", "user-friendly")

Skeleton:

```markdown
# Requirements Document

## Introduction

<what feature does, who uses it, 1 paragraph>

## Glossary

- **<Term>**: <definition>

## Requirements

### Requirement 1: <title>

**User Story:** As a <role>, I want <capability>, so that <benefit>.

#### Acceptance Criteria

1. WHEN <trigger>, THE <System> SHALL <response>.
2. IF <condition>, THEN THE <System> SHALL <response>.

## Open Questions

- <F-id> (<type>, <severity>, deferred): <issue>
```

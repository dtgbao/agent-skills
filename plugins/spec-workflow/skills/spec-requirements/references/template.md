# requirements.md template and EARS rules

Shared by both modes (fresh Requirements-First start and Design-First
derivation) — read whichever mode file applies first, then this one for
the exact structure.

## Build the Glossary first

Before drafting requirements, identify the domain nouns the requirements
will need to reference precisely, and define them:

- The system/application itself (e.g. `Application`), and any major
  subsystem the requirements will call out by name (e.g. `Middleware`,
  `Rate_Limiter`, `Auth_Guard`) — these become the subject of "THE ... SHALL"
  statements instead of a generic "the system." When deriving from a design
  (Design-First mode), reuse the component names design.md already
  defined.
- Actors/roles referenced in user stories (e.g. `Client`, `User`, `Admin`).
- Key domain concepts with a precise meaning in this feature (e.g.
  `Protected_Route`, `Time_Window`, `Session`).

Name each term in `Title_Case_With_Underscores` for multi-word terms so it
reads unambiguously inside a sentence, and give each a one-sentence
definition. This glossary is what acceptance criteria quote from — don't
introduce a capitalized term in the requirements that isn't defined here,
and don't define a term here that no acceptance criterion uses.

## Structure

```markdown
# Requirements Document

## Introduction
<1-2 sentence summary of the feature and why it's needed>

## Glossary

- **Term**: One-sentence definition.
- **Another_Term**: One-sentence definition.

---

## Requirements

### Requirement 1: <short title>
**User Story:** As a <role>, I want <capability>, so that <benefit>.

#### Acceptance Criteria

1. WHEN <event/condition>, THE <Glossary Term> SHALL <expected behavior>
2. IF <precondition>, THEN THE <Glossary Term> SHALL <expected behavior>
3. WHILE <ongoing condition>, THE <Glossary Term> SHALL <expected behavior>

---

### Requirement 2: <short title>
...

---
```

## EARS rules

Use EARS (Easy Approach to Requirements Syntax) for every acceptance
criterion, and always name the specific glossary term responsible for the
behavior rather than a generic "the system":

- `WHEN <event> THE <Term> SHALL <response>` — for triggered behavior
- `IF <condition> THEN THE <Term> SHALL <response>` — for conditional behavior
- `WHILE <state> THE <Term> SHALL <response>` — for behavior during a state
- `WHERE <feature/context> THE <Term> SHALL <response>` — for context-dependent
  behavior
- A criterion with no trigger at all is stated flatly: `THE <Term> SHALL
  <behavior>` (used for standing constraints, e.g. "THE Application SHALL
  include `<package>` as a production dependency").

Cover the happy path, edge cases, error conditions, and any explicit
non-functional requirements the user mentioned (performance, security,
accessibility). Don't invent requirements the user didn't ask for and
wouldn't want — when in doubt, list it as an open question instead of
assuming.

Separate the Introduction, Glossary, and each numbered Requirement with a
`---` horizontal rule, matching the structure above.

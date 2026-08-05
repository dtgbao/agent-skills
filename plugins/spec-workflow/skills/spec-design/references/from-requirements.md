# Mode A: derive design from approved requirements

Read `.claude/specs/<slug>/requirements.md` in full, including its
Glossary — reuse those exact terms in the design; don't rename `Auth_Guard`
to "the guard middleware" partway through.

Every non-trivial design decision should trace back to a requirement —
reference requirement numbers (e.g. "satisfies Requirement 2") where it
clarifies why something exists. If a requirement turns out ambiguous or
under-specified once you try to design against it, flag it explicitly
rather than silently resolving it your own way.

Draft design.md following `feature-template.md`.

On approval, the next phase is `spec-tasks`.

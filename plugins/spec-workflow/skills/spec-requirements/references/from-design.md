# Mode: derive requirements from an approved design (Design-First phase 2)

Read `.claude/specs/<slug>/design.md` in full first. Every requirement you
write must be something the design actually supports — that's the whole
point of Design-First: requirements are guaranteed technically feasible
because they're derived from validated architecture, not the other way
around. Don't introduce a requirement the design has no component for; if
the user's `$ARGUMENTS` asks for something the design can't do, flag the
mismatch rather than silently inventing new architecture to cover it.

Build the glossary (per `template.md`) using the component and data-model
names already established in design.md, so terminology stays consistent
across both files.

On approval, the next phase is `spec-tasks` (design is already done), not
`spec-design`.

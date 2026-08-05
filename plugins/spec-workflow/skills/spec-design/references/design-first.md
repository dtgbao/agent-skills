# Mode B: Design-First entry

There's no requirements.md to read yet; the design comes first and
requirements will be derived from it afterward in a separate
`spec-requirements` run. Since there are no requirement numbers to cite
yet, justify decisions against the user's stated goals in `$ARGUMENTS`
instead.

**First, determine the detail level.** If `$ARGUMENTS` already signals one
(mentions "high level", "architecture diagram", "for the team", or
conversely "pseudocode", "low level", "quick feasibility check", "just
validate this works"), use that. Otherwise ask a single question:

> Should this be a **High Level Design** (architecture diagram, component
> interactions, tech stack — best for complex systems or team
> collaboration) or a **Low Level Design** (algorithmic pseudocode,
> interface contracts, key data structures — best for rapid prototyping or
> a quick feasibility check)?

Then draft design.md following `feature-template.md`, weighting emphasis by
level:

- **High Level:** spend the most space on the Architecture diagram and
  Components and Interfaces sections; Data Models and pseudocode-level
  detail can stay lighter.
- **Low Level:** spend the most space on concrete interface signatures,
  pseudocode, and Data Models; the Architecture section can be a brief
  diagram plus a short walkthrough rather than a full component catalog.

Both levels still cover non-functional properties (performance, security,
scalability) if the user mentioned any — that's expected at either level.

On approval, the next phase is `spec-requirements` (to derive requirements
from this now-validated design), **not** `spec-tasks`.

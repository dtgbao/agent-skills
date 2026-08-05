# Feature spec: task citations and property tests

Tie every implementation subtask back to the requirement(s) it satisfies
via a `_Requirements: X.Y_` line.

**If design.md has a `## Correctness Properties` section**, add one
optional subtask per property, formatted distinctly from normal tasks:

```markdown
- [ ]* 2.3 Write property test for <name> in `<test file path>`
  - **Property N: <title>**
  - Use `<library>` `<generator>` to generate <inputs>; assert <the
    property's guarantee, restated as a concrete check>
  - Run a minimum of 100 iterations
  - Tag: `// Feature: <feature-slug>, Property N: <title>`
  - **Validates: Requirements X.Y**
```

Note the property test's closing line is `**Validates: Requirements X.Y**`
(bold), not the `_Requirements:_` (italic) line used elsewhere — this
distinguishes "implements requirement X" from "formally verifies
requirement X across all inputs."

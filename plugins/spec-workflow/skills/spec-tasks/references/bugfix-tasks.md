# Bugfix spec: task citations and required property tests

There's no requirements.md, so implementation subtasks cite bugfix.md
directly: `_Addresses: bugfix.md — Expected Behavior_` (or `— Unchanged
Behavior` for a subtask specifically about preserving existing behavior).

**Always include three property-test subtasks**, one per property defined
in design.md's `## Properties to Test` section (bugfix designs always have
exactly these three: bug is reproducible, bug is fixed, no regressions).
Format each like a feature property test, but validate against bugfix.md
instead of a requirement number:

```markdown
- [ ]* 2.1 Write property test for bug reproduction in `<test file path>`
  - **Property 1: Bug is reproducible**
  - Use `<library>` `<generator>` to generate <inputs matching the defect
    condition>; assert the pre-fix code exhibits the Current Behavior
  - Run a minimum of 100 iterations
  - Tag: `// Bugfix: <bugfix-slug>, Property 1: Bug is reproducible`
  - **Validates: bugfix.md — Current Behavior**
```

Repeat the pattern for Property 2 (bug is fixed — assert the *fixed* code
now exhibits Expected Behavior) and Property 3 (no regressions — assert
Unchanged Behavior scenarios still pass). These three are marked `[ ]*` for
consistency with the rest of the plugin's optional-task convention, but
they're not optional in spirit — a bugfix isn't done until all three pass.

Also include a plain (non-test) implementation subtask for the actual code
change described in design.md's Fix Approach, citing `_Addresses:
bugfix.md — Expected Behavior_`.

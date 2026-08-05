# Mode C: bugfix design (self-contained — does not use feature-template.md)

Read `docs/specs/<slug>/bugfix.md` in full — it defines the Current
(Defect), Expected (Correct), and Unchanged (Regression Prevention)
behavior this design must resolve.

**Investigate before writing anything.** Don't draft root cause from the
bug report alone: find the relevant code path, check recent history if
useful (`git log` / `git blame` on the suspect file), and confirm your
theory against what the code actually does. If you can't pin down a root
cause with reasonable confidence, say so explicitly rather than presenting
a guess as settled fact.

## Structure

```markdown
# Bugfix Design: <Short Title>

## Root Cause Analysis
<The specific code/logic responsible, with file/function references. If
unconfirmed, say so and describe your leading hypothesis plus what would
confirm it.>

## Affected Areas
<Other code paths that touch the same function/state/data and could be
impacted by a fix>

## Fix Approach
<The specific, minimal change proposed, and why it's minimal rather than a
broader refactor>

## Properties to Test

*Each property below becomes a property-based test in the tasks phase.*

### Property 1: Bug is reproducible
*For any* <input matching the defect condition in bugfix.md>, the current
(pre-fix) implementation SHALL exhibit the Current Behavior described in
bugfix.md.

**Validates: bugfix.md — Current Behavior**

### Property 2: Bug is fixed
*For any* <same input>, the fixed implementation SHALL exhibit the Expected
Behavior described in bugfix.md.

**Validates: bugfix.md — Expected Behavior**

### Property 3: No regressions
*For any* <input covering the Unchanged Behavior scenarios in bugfix.md>,
the fixed implementation SHALL CONTINUE TO exhibit that behavior unchanged.

**Validates: bugfix.md — Unchanged Behavior**
```

Fill in the `<...>` parts concretely — these three properties always exist
for a bugfix design (they're what makes it "surgical": prove the bug was
real, prove it's fixed, prove nothing else broke), but their input
descriptions and exact wording should reflect this specific bug.

On approval, the next phase is `spec-tasks`.

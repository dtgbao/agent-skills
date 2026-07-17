# Task Planning

Use this reference before writing or revising `tasks.md`. Translate the approved design into short executable leaves without restating its architecture.

## Contents

- [Build Capability Groups](#build-capability-groups)
- [Pair Test and Implementation Leaves](#pair-test-and-implementation-leaves)
- [Keep Leaves Concise](#keep-leaves-concise)
- [Model Dependencies Once](#model-dependencies-once)
- [Use Checkpoints and Exceptions](#use-checkpoints-and-exceptions)
- [Review the Plan](#review-the-plan)

## Build Capability Groups

Use numbered top-level checkboxes as capability groups. Give every independently executable behavior a numbered child such as `1.1`, `1.2`, and `1.3`. Keep parent groups free of implementation prose; required child completion determines parent completion.

Use a top-level checkpoint when it is itself executable and needs no artificial child. Keep identifiers sequential within the document.

Complete decomposition when every large capability has child leaves and every executable item has one observable outcome.

## Pair Test and Implementation Leaves

Represent each behavior as an adjacent one-to-one pair:

```markdown
  - [ ] 1.1 Prove <behavior>
    - **RED:** <Focused test, setup, and assertion>.
    - **Verify RED:** Run `<command>`; expect <failure caused by missing behavior>.
    - _Requirements: <identifiers>_
  - [ ] 1.2 Implement <behavior>
    - **GREEN:** <Smallest implementation boundary, paths, and symbols>.
    - **Verify GREEN:** Run `<focused and related commands>`; expect success.
    - **REFACTOR:** <Cleanup or explicit no-cleanup decision>, then rerun `<command>`.
    - _Requirements: <same identifiers>_
```

Give the implementation leaf a direct dependency on its test leaf. Preserve the same upstream identifiers on both leaves. Read [test-driven development](test-driven-development.md) for failure evidence, test quality, and exception rules.

Complete a pair when RED proves the test detects absence and GREEN/refactor proves the approved behavior through the designed public contract.

## Keep Leaves Concise

Use only the accepted labeled bullets for a leaf. Make each label one focused instruction. Name exact paths or symbols and commands, but refer to the relevant `design.md` contract instead of repeating schemas, algorithms, component trees, or full interfaces.

Split a leaf when it spans independently reviewable outcomes, crosses unrelated subsystems, needs another RED/GREEN proof, or cannot be described within its accepted labels.

## Model Dependencies Once

Use one JSON dependency graph after the task list. Each wave contains executable task objects with string `id` and `dependsOn` fields. Include child leaves plus executable top-level checkpoints or exceptions; exclude parent capability groups.

Every dependency must appear in an earlier wave. Tasks in one wave must have no dependency on each other and must be safe to run concurrently without shared files, mutable state, or unresolved interfaces. Include every executable task exactly once.

## Use Checkpoints and Exceptions

Use checkpoints after integrated vertical slices:

```markdown
- [ ] 2. Checkpoint — <integrated outcome>
  - **Check:** Run `<integration command>`.
  - **Expected:** <Observable success and warning expectations>.
  - _Requirements: <identifiers>_
```

Use `[TDD Exception]` only after explicit user approval for generated output, configuration-only work, throwaway exploration, or another recorded case. Include Reason, Approval, and Check entries. Optional behavior still uses a complete RED/GREEN pair.

## Review the Plan

Before approval, resolve every finding:

1. **Coverage:** Every required upstream identifier appears in a required RED/GREEN pair or checkpoint.
2. **Pairing:** Every test has exactly one adjacent implementation with identical traceability.
3. **Concision:** Every leaf has one outcome and only its accepted labels.
4. **Design boundary:** Tasks name where to work without duplicating design details.
5. **Graph:** Executable identifiers and dependencies exactly match the checklist and are acyclic.
6. **Checkpoints:** Each completed vertical slice has observable integration evidence.
7. **Completion state:** A parent is checked only when every required child is checked.
8. **Completion:** No placeholder, vague instruction, or unresolved choice remains.

Run the validator and request approval only after every check passes.

---
name: spec-writer
description: "Write or update one section of an sdd spec.md (Requirements, or Design + Plan). Dispatched by spec-new and spec-sync."
tools: Read, Write, Edit, Glob, Grep, Bash
model: sonnet
---

The caller gives you: the spec dir, the task (`requirements`, `design` or `update`), the input text, and the paths of `spec-format.md` and `spec.py`.

## Steps

1. Read `spec-format.md`. Read `spec.md` if it exists.
2. Read the code that the input touches: the files that it names, the modules, the tests, the manifest and the README. Use Bash only for commands that read.
3. Write the task:
   - `requirements`: create `spec.md` with the header lines and `## Requirements`, from the input. Put each value that the input does not give in Open questions, with your recommended answer.
   - `design`: first apply the answers in the input to the Requirements: write each answer into its criteria, and set Open questions to `- none`. Change nothing else in the Requirements. Then add `## Design` and `## Plan`. If another requirement must change, write it under KEY.
   - `update`: apply the changes in the input (changes from the user, or changed criteria). Change only what the input needs. For a changed criterion, update its cases and the Properties and Decisions that use it. For each `OLD VALUE … criterion N.M` line, update that criterion too, so that the criteria agree.
4. Run `python3 <spec.py> check <dir>` (add `requirements` for the requirements task). Fix each `FAIL` line and run it again.
5. Reply with this report only, 12 lines or fewer:

```
WROTE: <section(s)>
COUNTS: <n> requirements, <n> criteria | <n> lanes, <n> slices, <n> cases, <n> properties
OPEN: none | one line for each open question: Q<n> <question> (recommended: <answer>)
KEY: up to 4 lines, the decisions or assumptions that the user must know
CHECK: PASS | FAIL <first failing line>
```

Do not write code or tests. Do not run tests.

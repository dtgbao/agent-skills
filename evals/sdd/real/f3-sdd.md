## Script (f3, sdd plugin)

Feature text: the content of `f3-feature.md` in this folder, word for word.

Commands:
1. `/sdd:spec-new <feature text>`
2. `/sdd:spec-run <name> <RUN ARGS>` (RUN ARGS come from your first message)

Answers:
- Gate 1: for each open question, first write the question in `eval/notes.md`, then read `f3-answers.md` in this folder and answer from it. If no line fits, use the recommended answer. Then Approve.
- Gate 2: Approve.
- spec-run: retries as the skill says; after 2 attempts, Skip lane. Counterexample: Fix code.

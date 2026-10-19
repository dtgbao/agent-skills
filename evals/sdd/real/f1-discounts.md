## Script (f1-discounts, sdd plugin)

Feature text: the content of `f1-feature.md` in this folder, word for word.

Commands:
1. `/sdd:spec-new <feature text>`
2. `/sdd:spec-run <name> <RUN ARGS>` — RUN ARGS come from your first message.
3. Hand edit, as a human: in `spec.md`, in the Requirements section only, change the percent range 1–90 to 1–50. Text only. Touch no other file and no other section.
4. `/sdd:spec-sync <name>`
5. `/sdd:spec-run <name> <RUN ARGS>`

Answers:
- Gate 1: Approve, with the recommended answer for each open question.
- Gate 2: Approve.
- spec-run: retries as the skill says; after 2 attempts, Skip lane. Counterexample: Fix code.
- spec-sync: Approve.

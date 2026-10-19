## Script (f1-tdd baseline, no plugin)

The same feature and change as `f1-discounts.md`, done with the `tdd` skill only. Use it to compare time, tokens and quality with the sdd plugin.

Feature text: the content of `f1-feature.md` in this folder, word for word.

Commands:
1. Invoke the `tdd` skill and build the feature text.
2. Change request, with the `tdd` skill: the percent range is now 1–50, not 1–90. A percent above 50 gives status 400.

Answers:
- Any question to the user: pick the most conservative concrete option, and log it in `eval/QA.md`.

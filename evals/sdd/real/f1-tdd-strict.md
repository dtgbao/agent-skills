## Script (f1-tdd-strict baseline, no plugin)

The same as `f1-tdd.md`, but follow the `tdd` skill exactly: vertical slices. One test, then the code that makes it pass, then the next test. Never write the next test before the current test is green. Run the test after you write it (it must fail for the right reason) and after you write the code.

Feature text: the content of `f1-feature.md` in this folder, word for word.

Commands:
1. Invoke the `tdd` skill and build the feature text, one test at a time.
2. Change request, with the `tdd` skill, one test at a time: the percent range is now 1–50, not 1–90. A percent above 50 gives status 400.

Answers:
- Any question to the user: pick the most conservative concrete option, and log it in `eval/notes.md`.

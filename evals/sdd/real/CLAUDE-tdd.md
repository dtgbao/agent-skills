# Eval mode: tdd baseline

This project is an automated baseline test. No human answers questions.

1. **Script.** Your first message names the Script file. Read it yourself. Run its commands in order. Use only the `tdd` skill (Skill tool, `skill: "tdd"`). Use no plugin and no other skill. Write no spec files.
2. **Scripted user.** Never call AskUserQuestion. When the skill says to ask, take the answer from the Script, and log it in `eval/notes.md`.
3. **Logs.** Keep them minimal: in `eval/notes.md`, one line for each command with its start and end time (`date +%T`). Write nothing else under `eval/`.
4. Tests: `uv run --no-project --with pytest --with hypothesis python -m pytest -q`. Do not commit.

End with one line: `DONE: <commands run> · <final test result line>`.

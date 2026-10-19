---
name: spec-brainstorm
description: "Clarify a vague feature idea with the user before a spec. Writes no files."
argument-hint: "[idea]"
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Bash, AskUserQuestion, Agent, Task
---

Input: $ARGUMENTS. If `spec-new` started this skill, the input is the input of `spec-new`. At the end, go back to the next step of `spec-new`. The terms in this file have the meanings in `${CLAUDE_PLUGIN_ROOT}/shared/glossary.md`.

Goal: the user and you agree on what to build and why, before `requirements.md` exists. The result is a playback that the user confirms in chat. Do not write files or code. The playback stays in the conversation only.

## Brief

The brief is the test for clarity. It has this form:

`<who> needs <what> so that <why>. Done when <observable success>. Out: <one non-goal>.`

Fill each slot from the input and from the code. If you must guess a slot, write `?` in it. The `Out:` slot is optional: if the input gives no non-goal, write your guess and mark it `(guess)`. A guessed `Out:` does not make the input vague. A why that follows directly from the what counts as filled. Example: "tag notes and filter by tag" gives "so that the user finds related notes".

- The input is vague if one or more slots have `?`.
- The input is ambiguous if one of its words has two meanings that give different products.
- The input is a defect report if it names a wrong behavior that existing code shows now: a call that fails, or a result that is different from the expected result. A wrong behavior that the user reports counts, also when the code cannot show it. The spec-writer tests it when it writes the `## Bug` section. "It feels broken", with no observed behavior, is not a defect report. Test it as a feature.

## Steps

1. Test the input.
   1. Read the files that the input names. Search the code for the nouns in the input.
   2. If the input is a defect report, do not make a brief and do not ask questions. If `spec-new` started this skill, go back to it; the spec-writer gets the facts from the code. If the user started this skill, tell the user to type `/sdd:spec-new Bugfix: <input>`. Then stop.
   3. If not, fill the brief.
   4. If the brief is clear and `spec-new` started this skill, show the brief in one line and go back. The input stays the source for `spec-new`. The brief only confirms it.
   5. If the brief is clear and the user started this skill, go to step 4.
   6. If the input is vague or ambiguous, write one line with the open slots and "Say skip to start now". Send this line and the first question of step 2 in one message.
   - Done when: you know the result: defect, clear, vague or ambiguous.
2. Describe.
   - Ask one open question in each message. Do not give a list of options.
   - Connect each question to a real event. Example: "Tell me about the last time this caused a problem."
   - Use the words of the user.
   - If you can make a guess that the user can correct, give the guess. A guess is better than a question.
   - Find the facts yourself: read the code, the docs and `git log`. Use Bash only for commands that read. Ask the user only about intent and decisions.
   - Learn about these topics, but do not read them to the user as a list: why now, the users, success, non-goals, anti-goals (it works, but it is still a failure), examples that exist, the current state, fixed choices (stack, libraries, interfaces).
   - Done when: no slot has `?`.
3. Ask about decisions.
   1. Make a decision tree of the open decisions. Find the frontier.
   2. In each round, ask with AskUserQuestion. Ask 4 frontier questions or fewer. Put your recommended answer first and mark it `(Recommended)`.
   3. The surface (CLI, library, UI or API) is a frontier question, unless the input or the code sets it already.
   4. After each answer, find the frontier again.
   5. Ask only about intent: what, why, and which choices are fixed. EARS criteria, edge cases and failure cases come later, in the requirements draft and its open questions.
   - Done when: the frontier is empty, and you told the user each assumption.
4. Play back. Write 300 words or fewer, in this form:
   ```
   Brief: <brief>
   Why: <reason of the user>
   Code facts: <what the code shows that changes the scope>
   Surface: <what calls it: CLI, library, UI, API>
   Goals: …  Non-goals: …  Anti-goals: …
   Fixed: <choices that the user made>
   Open for design: <choices for the agent>
   Split: <independent parts, one spec for each>   (only when there is more than one part)
   Workflow: feature | bugfix, because <reason>
   ```
   Mark each guess `(guess)`. Write the words of the user as their words. Ask the user what is wrong or missing. If the user gives a correction, fix the playback and show it again.
   - Done when: the user confirms the playback.
5. Hand off.
   - The confirmed playback replaces the input for `spec-new` and for the requirements draft.
   - If the playback has a Split line, the user chooses the first part. Make one spec for each part.
   - If the user started this skill, tell the user to type `/sdd:spec-new`. With an empty input, `spec-new` uses the playback.

If the user says "skip" at any step, write your guess for each `?` slot in one line. Then go to step 5.

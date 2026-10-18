---
name: spec-brainstorm
description: "Clarify a vague feature idea with the user before a spec. Writes no files."
argument-hint: "[idea]"
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Bash, AskUserQuestion, Agent, Task
---

Input: $ARGUMENTS. Called from `spec-new` → input = its input; at the end, go back to its next step.

Goal: user and agent share one picture of what to build and why, before `requirements.md` exists. Output = a playback the user confirms in chat. Write no files and no code; the playback lives in the conversation only.

## Brief

The brief is the clarity test: `<who> needs <what> so that <why>. Done when <observable success>. Out: <one non-goal>.` Fill each slot from the input and the code. A slot you guess → `?`. A why that follows from the what counts as filled.

- Vague = one or more slots `?`.
- Ambiguous = a word in the input has two readings that build different things.
- Defect report = the input names a wrong behavior that existing code shows now: a failing call, or actual vs expected. "Feels broken" with no observed behavior → not a defect report; test it as a feature.

## Steps

1. Test. Read files the input names. Grep the code for its nouns.
   - Defect report → no brief, no question. Called from `spec-new` → go back; the Bugfix workflow Facts step gets the facts. Standalone → tell user: `/sdd:spec-new Bugfix: <input>`. Stop.
   - Else fill the brief.
   - Clear, called from `spec-new` → show the brief in one line, go back. The input stays the source for `spec-new`; the brief only confirms it.
   - Clear, standalone → step 4.
   - Vague or ambiguous → one line: which slots are open, and "say skip to start now". Send it in one message with the first step 2 question.
   - Done when: verdict known (defect, clear, vague or ambiguous).
2. Describe. One open question per message, no option list. Anchor it on a real moment ("Walk me through the last time this hurt."). Use the user's words. A guess the user can correct beats a question. Facts are your job: read code, docs, `git log` (Bash for read-only commands only); ask the user only for intent and decisions. Ground to cover, never read out as a list: why now · users · success · non-goals · anti-goals (works, but still a failure) · prior art · current state · fixed choices (stack, libraries, interfaces).
   - Done when: no slot `?`.
3. Grill. Map the open decisions as a design tree. Frontier = decisions whose prerequisites are settled. Each round: AskUserQuestion, ≤4 frontier questions, your recommendation first, marked `(Recommended)`. Recompute the frontier after each answer. Stay at intent: what, why, which choices are fixed. EARS criteria, edge and failure cases go to the requirements draft and `/sdd:spec-analyze`.
   - Done when: frontier empty, no assumption left unspoken.
4. Play back. ≤300 words, this shape:
   ```
   Brief: <brief>
   Why: <user's reason>
   Code facts: <what the code shows that changes scope>
   Goals: …  Non-goals: …  Anti-goals: …
   Fixed: <choices the user made>
   Open for design: <choices left to the agent>
   Split: <independent parts, one spec each>   (only when >1)
   Workflow: <spec-new workflow option>, because <signal>
   ```
   Mark each guess `(guess)`. User words go in as theirs. Ask what is wrong or missing. Correction → fix, play back again.
   - Done when: user confirms the playback.
5. Hand off. The confirmed playback replaces the input for `spec-new` and for the workflow Context step. Split → user picks the first part; one spec per part. Standalone → tell user: `/sdd:spec-new` (empty input picks up the playback).

User says skip at any step → state each `?` slot as your guess in one line, then step 5.

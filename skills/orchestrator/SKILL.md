---
name: orchestrator
description: Use when work is multi-step, ambiguous, cross-cutting, or has independent pieces to plan, coordinate, split, or supervise.
---

# Orchestrator

Use subagents for bounded workstreams only after the user approves the plan.

## Model Choice

Choose the subagent model and reasoning while planning. Allowed choices:

- GPT-5.4 Low/Medium/High
- GPT-5.5 Low/Medium

Use the cheapest choice that can do the work under review. Intelligence is how hard a problem can be handed off unsupervised. Taste covers UI/UX, code quality, API design, and copy. Raise reasoning for ambiguity, risk, broad search, or weak review signals; choose GPT-5.5 when taste matters.

## Loop

1. Build the plan first: identify workstreams, dependencies, merge criteria, the smallest verification that proves the work, and the subagent model/reasoning for each delegated piece. Complete this step when every delegated piece has a clear boundary and the user has approved the plan.
2. Delegate clean subtasks: start a subagent with the chosen model/reasoning for each independent, bounded, checkable piece. Complete this step when every brief passes the Delegation Gate.
3. Run independent pieces in parallel. Keep serial or judgment-heavy work local until its prerequisites are clear. Complete this step when every active subtask has returned or is explicitly blocked.
4. Review every return before merging it. Check claims against source, diffs, logs, tests, or artifacts. Complete this step when every accepted result has evidence you verified.
5. If a return is wrong or under-scoped, rewrite the brief and run another subagent. Patch it yourself only when the fix is trivial. Complete this step when each rejected result is retried, fixed locally, or excluded.
6. Integrate reviewed results, run the smallest relevant verification, and report what was delegated, accepted, retried, or kept local.

## Delegation Gate

Delegate only when the subtask has:

- One outcome.
- Small enough context to brief cleanly.
- No hidden dependency on another active subtask.
- A result you can review without trusting the subagent.

Keep the work local when it is trivial, requires continuous judgment, touches live systems, or the plan is not stable enough to brief.

## Subagent Brief

Give each subagent:

- Goal: the concrete outcome.
- Context: relevant files, commands, constraints, and user intent.
- Boundaries: what not to change, decide, or assume.
- Return: the exact artifact to bring back, such as findings, a patch, command output, or a recommendation.
- Stop condition: when to ask back instead of guessing.

---
name: orchestrator
description: Use when work is multi-step, ambiguous, cross-cutting, or has independent pieces to plan, coordinate, split, or supervise.
---

# Orchestrator

Use the strongest available reasoning model for broad, high-risk, architecture-heavy, or shallow-plan-sensitive work.

## Worker Gate

Before planning, check for `.codex/agents/worker.toml` in the active workspace. If it is missing, stop and ask the user to create it from `skills/orchestrator/assets/template-work-subagent.md`; ask which `model` and `model_reasoning_effort` they want. Complete this gate only when the file exists.

Use the configured `worker` subagent for delegation. Do not hard-code its model or reasoning effort in briefs; `.codex/agents/worker.toml` owns that choice.

## Loop

1. Build the plan first: identify workstreams, dependencies, merge criteria, and the smallest verification that proves the work. Complete this step when every delegated piece has a clear boundary.
2. Delegate clean subtasks: start a `worker` subagent for each independent, bounded, checkable piece. Complete this step when every brief passes the Delegation Gate.
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

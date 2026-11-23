---
name: refine-prompt
description: Refine a draft prompt with the eight prompt components and a base framework, asking the user for missing parts.
disable-model-invocation: true
argument-hint: "Paste the draft prompt, or give a file path"
---

The user wants a draft prompt **refined**. You make it complete and minimal. Each of the eight components gets a decision, and each decision gets a reason.

One rule decides every component:

```
for each component:
    if the model would guess WRONG without it  → include it
    else                                        → leave it out
```

Apply it with the **otherwise test**: you can finish "…otherwise the model will ___" with a concrete failure. If you cannot finish the sentence, the component is out. A prompt that has extra parts is not better. Extra parts cost tokens and pull attention from the task.

## The eight components

| Component | Removes the guess about | Usually included when |
|---|---|---|
| `role` | voice, expertise, depth | domain tone matters. Goes in the system prompt. |
| `context` | why the task exists, stakes, what "good" means | trade-offs exist that the model cannot infer |
| `audience` | reading level, jargon, length | a **person** reads the output. Code readers have no audience. |
| `instructions` | the task itself | always |
| `examples` | edge cases, exact style | labels are ambiguous, or style is hard to describe |
| `constraints` | what the output may **say**: limits, allowed values, forbidden content | hard limits exist |
| `format` | what **shape** the output has | code parses it, or readers scan it |
| `input` | the data | the task has data. Use a `{{variable}}` when it changes per run. |

Constraints and format are often mixed up. Constraints control content ("only these five labels"). Format controls shape ("return only JSON").

## Frameworks

A framework is a pre-chosen set of components. Use it as the starting checklist, then compose with the rule.

| Framework | Slots | Lacks | Base for |
|---|---|---|---|
| RTF | Role, Task, Format | context, audience, constraints, examples | output read by code; short tasks |
| CO-STAR | Context, Objective, Style, Tone, Audience, Response | constraints, examples, input | text people read, where voice matters |
| RISEN | Role, Instructions, Steps, End goal, Narrowing | audience, format, examples | multi-step procedures, agents |
| CRISPE | Capacity/Role, Insight, Statement, Personality, Experiment | format, constraints | the user wants several variants |

Style is the writing manner. Tone is the attitude. Narrowing is constraints. End goal is the success test.

Select the base by asking two questions. **Who reads the output?** Code → RTF. A person → is it a **procedure**? Yes → RISEN. Is **voice** critical? Yes → CO-STAR. Otherwise → RTF. Use one base. Take single slots from other frameworks when they pass the otherwise test, and merge duplicate slots (Role = Capacity, Narrowing = constraints).

## Steps

### 1. Read the draft

Take the draft from the argument, a file path, or the conversation. Name the task in one line. Answer the two selection questions: who reads the output, and is it a procedure? When the draft does not show who reads the output, include that in the step 4 questions.

### 2. Map the draft

Sort every sentence of the draft into one of the eight components. Mark each component as **present**, **missing**, or **vague**. Vague means that it exists but still leaves a guess (for example, "be concise" with no limit).

### 3. Decide each component

Run the otherwise test on all eight components. Each one gets **include** or **leave out**, with a one-line reason. Then select the base framework and write the composition:

```
SELECT  <framework> because <who reads the output / task type>
KEEP    <slot> because <otherwise the model will ___>
ADD     <component> because <otherwise the model will ___>
DROP    <slot> because <it removes no guess for this task>
```

Done when all eight components have a decision and every decision has a "because".

### 4. Ask for what is missing

For every included component that is missing or vague, decide if you can fill it from the draft or the conversation. Fill it when you can. Ask only for the rest. Never ask about a component you decided to leave out.

Use the `AskUserQuestion` tool:

- One question for each component. Put at most 4 questions in each call. Ask in order of impact: instructions, input, format, constraints, examples, audience, context, role. Call it again if more remain.
- Give 2–4 options. Each option is a **concrete draft** of that component's text, written for this task, not a category name. Put the full text in the option's `preview` when it is longer than the label.
- Put your recommended option first, and add "(Recommended)" to its label. In its description, give the otherwise-test reason.
- Use the component name as the `header` (for example, `format`).

The user can choose "Other" and write their own text. Use the answer as given.

Done when every included component has final text.

### 5. Assemble and report

Build the refined prompt:

- Split it into **system** and **user** parts when the prompt runs through an API or an app. The system part holds role and standing constraints. The user part holds the per-run parts.
- Wrap each component in an XML tag with the component's name.
- Put long `input` first, and put `instructions` and `format` after it.

Reply with three blocks:

1. **Refined prompt**, in one code block, ready to copy.
2. **Decisions**: a table with columns component, decision, because. It has all eight rows.
3. **Composition**: the SELECT / KEEP / ADD / DROP lines from step 3.

Show the user's original draft only when they ask for a comparison.

For a full worked example (a ticket classifier), read [`references/example.md`](references/example.md).

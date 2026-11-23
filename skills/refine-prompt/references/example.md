# Worked example: ticket classifier

## Draft

```
Classify this support ticket. Be accurate.
```

## Step 1–2: read and map

Task: label support tickets for an automated router. **Code reads the output.** It is not a procedure.

| Component | Draft status |
|---|---|
| instructions | vague: "classify" with no label set |
| input | missing ("this ticket" has no slot) |
| all others | missing |

## Step 3: decide

| Component | Decision | Because |
|---|---|---|
| role | leave out | voice does not change a label |
| context | leave out | the label set already carries what matters |
| audience | leave out | code reads the output, not a person |
| instructions | include | otherwise the model invents its own label set |
| examples | include | otherwise "app crashes when I pay" goes to billing, not bug |
| constraints | include | otherwise the model returns labels the router cannot route |
| format | include | otherwise the shape varies and the parser breaks |
| input | include | otherwise there is nothing to classify |

```
SELECT  RTF because code reads the output
KEEP    Task (instructions), Format
ADD     examples, constraints, input
DROP    Role because voice does not change a label
```

## Step 4: questions asked

Only `instructions` (the label set) could not be inferred. `format` was drafted from the router's needs. The question was:

- header `instructions`, options: "billing, bug, account, feature_request, other (Recommended)" · "billing, technical, other" · "Use our Jira components"

## Step 5: result

```
SYSTEM:
<constraints>
Use only these labels: billing, bug, account, feature_request, other.
If no label fits, use other.
</constraints>

USER:
<input>
{{ticket_text}}
</input>

<instructions>
Classify the ticket in <input> into exactly one label.
</instructions>

<examples>
Ticket: I was charged twice → billing
Ticket: The app crashes when I pay → bug (the fault is in the software, not the charge)
</examples>

<format>
Return only JSON: {"label": "<label>"}
</format>
```

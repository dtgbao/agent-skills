# The wiki schema (AGENTS.md)

`<root>/AGENTS.md` is the per-wiki schema. `init` writes it once and never overwrites it.
The user and you change it together over time. Many agent hosts also load `AGENTS.md`
on their own when they work in that folder.

## Read it before every operation

Read it in full before each ingest, query, lint or sync. Its rules win over this skill.
A local convention may not show in any existing page. For example, a rule can apply
only to question pages, and no question page exists yet. So follow the text of the
schema, not the pattern of the files.

## Sections

| Section | Content |
|---|---|
| Layers | raw, wiki, schema rules |
| Domains | domain path rules, one domain per page |
| Page kinds | generic kinds, preset kinds, the extra-kinds marker |
| Frontmatter | the field template |
| Workflows | the short ingest, query, lint and sync steps |
| Local conventions | one bullet per user convention, with the date |

## Add a convention

When the user states a convention ("from now on", "always", "never", "in this wiki"):

1. Add a bullet under `## Local conventions`. Replace "None yet." on the first one.

   ```markdown
   - 2026-11-23: Every decision page has a "Reversal cost" section (low, medium, high).
   ```

2. For a new page kind, also edit the marker. Lint reads it:

   ```markdown
   <!-- llm-wiki:extra-kinds: runbook, incident, postmortem -->
   ```

3. Log it:

   ```bash
   python3 <skill-dir>/scripts/llm_wiki.py log schema "Decision pages get a Reversal cost section"
   ```

4. Apply the convention now, to the current task.

Do not add a convention that the user did not state. If you think one would help,
suggest it and wait for a yes.

## Presets

`init --preset NAME` adds domain kinds to the marker and short guidance:

| Preset | Extra kinds |
|---|---|
| `research` | paper, claim, dataset, method |
| `engineering` | system, runbook, incident, api |
| `book` | character, place, theme, chapter |
| `team` | meeting, person, project, customer |

A preset changes only the schema text. Kinds can be added later by editing the marker.

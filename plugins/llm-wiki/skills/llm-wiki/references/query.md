# Query

## Find

```bash
python3 <skill-dir>/scripts/llm_wiki.py search "permission boundary resource policy" --json
python3 <skill-dir>/scripts/llm_wiki.py search "boundary" --domain aws --kind concept --json
```

Search ranks title matches highest, then summary and tags, then body text.
Run 2–3 searches with different terms. Read `wiki/index.md` and the domain index too.
Then read the top pages in full. Open raw files when a page is thin or a claim needs a check.

## Answer

- Cite every claim with a relative link to a wiki page or raw file.
- Say clearly what the wiki does not cover. Mark any knowledge from outside the wiki.
- Pick the form that fits: a short answer, a table, a comparison, a list of steps.

## File the answer back

File it as a `question` page when the answer combines two or more pages, makes a
comparison or analysis, or the user asks to keep it. Skip it for trivial lookups,
or when the user says not to.

Put the page under the domain of its main subject. Name the file after the question.
Start with the scaffold, then write it to this shape:

```bash
python3 <skill-dir>/scripts/llm_wiki.py new question --domain aws/iam \
  --title "Do permission boundaries limit resource-based policies?" --json
```

```markdown
---
title: Do permission boundaries limit resource-based policies?
kind: question
domain: aws/iam
summary: No for same-account resource policies that name the user; yes for role sessions.
tags: [security]
sources: [raw/aws/iam/policy-eval-guide.md]
created: 2026-11-23
updated: 2026-11-23
---

# Do permission boundaries limit resource-based policies?

## Answer

Short answer first, then detail, each claim cited ([evaluation](policy-evaluation.md)).

## Evidence

- [Policy evaluation](policy-evaluation.md): ...
- [Guide](iam-policy-evaluation-guide.md): ...

## Open points

- What the wiki does not know yet.
```

Then link the question page from the main page it cites, and close:

```bash
python3 <skill-dir>/scripts/llm_wiki.py index
python3 <skill-dir>/scripts/llm_wiki.py lint
python3 <skill-dir>/scripts/llm_wiki.py log query "Do permission boundaries limit resource-based policies?" \
  --page wiki/aws/iam/do-permission-boundaries-limit-resource-based-policies.md
```

Check `AGENTS.md` first. A local convention can change the question page format,
its domain, or whether to file at all.

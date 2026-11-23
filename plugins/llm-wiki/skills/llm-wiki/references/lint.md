# Lint

Lint has two passes: mechanical (the CLI) and semantic (you).

## Mechanical pass

```bash
python3 <skill-dir>/scripts/llm_wiki.py lint --json
```

Exit 1 means errors. `--strict` also fails on warnings.

| Code | Level | Fix |
|---|---|---|
| `placeholder` | error | Replace the `TODO(llm-wiki)` text with real content |
| `frontmatter-missing`, `frontmatter-invalid` | error | Add or fix the YAML block |
| `field-missing` | error | Add the field (title, kind, domain, summary, updated) |
| `summary-too-long` | error | Rewrite the summary in 160 characters or fewer |
| `kind-unknown` | error | Use a known kind, or add it to the AGENTS.md extra-kinds marker |
| `domain-mismatch`, `domain-invalid`, `page-outside-domain` | error | Move the page or fix `domain:` |
| `date-invalid` | error | Use `YYYY-MM-DD` |
| `source-missing` | error | Fix the `raw/...` path in `sources:`. Never recreate raw files by hand. |
| `link-broken` | error | Fix or remove the link. Only links inside `wiki/` are checked. |
| `log-missing`, `log-heading-invalid`, `log-op-unknown` | error | Tell the user. Do not rewrite log history yourself. |
| `orphan` | warning | Link the page from a related page or the overview |
| `ingest-log-missing` | warning | Run `log ingest "<title>" --page <path>` |
| `raw-unreferenced` | warning | Ingest the raw file, or add it to a page's `sources:` |
| `index-stale` | warning | Run `index` |
| `summary-markup`, `date-order`, `log-order` | warning | Clean up the field |

## Semantic pass

Read the indexes, then the pages in the scope (a domain, or the whole wiki). Look for:

1. **Contradictions** between pages. Record them on both pages with citations.
2. **Stale claims** that a newer source supersedes. Update them and cite the newer source.
3. **Missing pages:** entities or concepts that appear on 2+ pages but have no page.
4. **Missing cross-links** between pages that discuss the same thing.
5. **Gaps:** questions the wiki cannot answer yet, and sources that would fill them.
   This is the main input for follow-ups.
6. **Local conventions** in `AGENTS.md` that pages do not follow yet.

Fix what is safe: links, summaries, small updates with citations. Ask before you delete
content, merge pages or change a decision.

## Log the pass

Every lint pass ends with one `lint` log entry. Put each suggested question and source
in a `--follow-up` item. Prefix each item with `Question:` or `Source:`.

```bash
python3 <skill-dir>/scripts/llm_wiki.py log lint "Health check: aws" \
  --body "- Fixed 2 broken links and 1 orphan.
- Contradiction: boundary scope (policy-types vs guide), noted on both pages." \
  --follow-up "Question: How do SCPs interact with resource control policies?" \
  --follow-up "Source: AWS IAM user guide, section 'Policy evaluation logic'"
```

The entry gets a `### Follow-ups` section. Report the same list to the user.

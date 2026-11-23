# Ingest

## Contents

- Order of work
- Choose the domain
- The approval gate
- Write the pages
- Close the ingest

## Order of work

```text
read source ─┬─> scan wiki ─> PROPOSAL ─> (user approves) ─> ingest scaffold ─> write pages ─> index ─> lint ─> log ingest
             └─> research workers (background) ──── findings ─────────────────────┘ (merged while writing)
```

The user waits only for your own scan. Research never blocks the proposal.

## Choose the domain

- A domain is a path of lowercase kebab-case segments: `aws/iam`, `ml/transformers`,
  `team/payments/incidents`. Two or three segments are typical.
- Reuse an existing domain when one fits. Check `wiki/index.md` and `wiki status`.
- Choose the domain of the source's main subject, not of its author or publisher.
- A page lives under exactly one domain. For secondary domains, add a tag such as
  `aws/organizations` and link to pages there.
- Raw files and the source page use the same domain: `raw/<domain>/` and `wiki/<domain>/`.

## The approval gate

Send this before any write. Keep it short. Then stop and wait for the reply.

```markdown
**Proposed domain:** `aws/iam`
Alternatives: `aws/security` (if you group all AWS security), `security/access-control` (vendor-neutral)

**Key takeaways**
1. An explicit deny in any policy overrides every allow.
2. SCPs limit the maximum permissions of an account; they grant nothing.
3. Permission boundaries cap identity policies, not resource policies.

**Related pages:** [IAM policy types](wiki/aws/iam/policy-types.md) (update), [SCP](wiki/aws/organizations/scp.md) (link)
**Contradictions:** [policy-types.md](wiki/aws/iam/policy-types.md) says boundaries also cap resource policies. This source says they do not.
**Planned pages:** new source page; new concept `policy-evaluation`; update `policy-types`.
**Research:** 2 background checks running (AWS docs on boundaries, a recent re:Invent talk).

What should I emphasize? Reply "ok" to use this plan, or change the domain or focus.
```

Rules:

- Give exactly one primary domain and 1–3 alternatives, each with a short reason.
- Give 3–5 takeaways. Each is one specific claim from the source, not a topic label.
- Name related pages from your scan. Write "None found" when there are none.
- Name every contradiction with an existing page. Write "None found" when there are none.
- Ask what to emphasize.
- Skip the gate only when the user approved this domain for this source in advance,
  for example "ingest this into aws/iam, no need to confirm". Then still report the
  takeaways in your final message.

## Write the pages

After approval, run the scaffold:

```bash
python3 <skill-dir>/scripts/llm_wiki.py ingest "https://example.com/post" --domain aws/iam --snapshot --json
python3 <skill-dir>/scripts/llm_wiki.py ingest ~/Downloads/meeting.txt --domain team/payments --title "Payments sync 2026-11-20" --json
python3 <skill-dir>/scripts/llm_wiki.py ingest talk.md --domain ml/rl --asset slide-3.png --json
```

- A URL with `--snapshot` saves the original bytes (for example `.html`) and, for HTML,
  an extracted `.md` text file next to it. Read the `.md`; cite both in `sources`.
- A local file is copied into `raw/<domain>/`. The original stays where it was.
  A file already under `raw/` is used in place.
- Identical content is reused. Different content under the same name is refused.
  Pass `--name <new-slug>`.

Then do the judgment work:

1. **Source page** (the scaffold). Replace every `TODO(llm-wiki)` placeholder. Write the
   `summary:` field as one plain sentence of 160 characters or fewer.
2. **Entity and concept pages.** For each important entity or concept, update its page
   or create one. Add the new facts with a citation to the source page. Start a new
   page with `new KIND --domain D --title T` (see [page-format.md](page-format.md)).
3. **Decision and practice pages** when the source records a choice or a how-to.
4. **Overview** of the domain: update the synthesis when the source changes the picture.
5. **Contradictions.** Write them on both pages, with both citations. Do not silently
   pick a winner. Prefer the newer or more authoritative source only when you say why.
6. **Cross-links.** Link every new page from at least one related page.
7. **Research findings.** Merge findings that have arrived. Mark them as web findings
   with their URL. If a finding conflicts with the source, record it as a contradiction.
8. Set `updated:` to today on every page you change. Add the source to its `sources:`.

## Close the ingest

```bash
python3 <skill-dir>/scripts/llm_wiki.py index
python3 <skill-dir>/scripts/llm_wiki.py lint
python3 <skill-dir>/scripts/llm_wiki.py log ingest "IAM policy evaluation guide" \
  --page wiki/aws/iam/iam-policy-evaluation-guide.md --page wiki/aws/iam/policy-types.md
```

Lint must end with zero errors. The ingest log entry must name the source page,
because lint warns about source pages without one.

In the final message, list the pages created and updated, the contradictions and
the open questions. Offer to sync; do not sync unasked.

---
name: web-search
description: Research current technical guidance on the web. Use for version-specific documentation or setup, implementation practices that may have changed, comparisons of official recommendations, or concise source-backed technical summaries.
---

# Web Search

Produce a current, version-aligned technical answer whose material factual claims are traceable to opened sources.

## Defaults

- Cite at most 5 unique source URLs unless the user sets another limit. Inspect additional pages when needed; the limit applies to sources cited in the answer.
- Prefer primary, official sources. Use secondary and community sources for discovery or explicitly requested perspective, then trace technical claims to primary evidence.
- Include minimal code for implementation requests when the relevant APIs can be verified.
- Use Markdown unless the user requests another format; match the requested shape, depth, and source constraints.

## 1. Frame the research target

Extract or infer:

- the question or decision to resolve
- the technology, version, runtime, and platform in scope
- the freshness target, especially for “latest,” “current,” or migration requests
- requested sources, source limit, code preference, and output format

Use the clearest reasonable interpretation. When plausible interpretations would change the recommendation, cover the meaningful alternatives or state the assumption before answering.

**Complete this step when:** the question, version scope, freshness target, and output constraints are explicit in the working notes or planned answer.

## 2. Build the source map

Split the question into material claim groups such as setup, API behavior, compatibility, migration, performance, or known limitations. Search each group through this source ladder:

1. Current official documentation, API reference, specification, or vendor guidance
2. Official release notes, migration guides, changelogs, and maintainer repositories
3. Upstream source, tests, commits, pull requests, issues, or maintainer discussions for behavior absent from published docs
4. Original standards, research, benchmarks, or datasets when the claim type requires them

Start with focused queries containing the product, task, and version. Expand only for unresolved claim groups. Open the relevant pages and treat search snippets as discovery signals rather than evidence.

**Complete this step when:** every material claim group has the strongest reasonably available evidence, or an authoritative-source gap is recorded.

## 3. Verify the evidence

Check each source against the claim it will support:

- Confirm the page states the claim directly or provides the primary data needed to infer it.
- Confirm version, runtime, platform, and release status match the request.
- Prefer the canonical URL for the requested version and language. Treat development-version paths, localized mirrors, and alternate copies as version or provenance mismatches until verified.
- Capture a concrete freshness signal when recency affects the answer: documentation version, release tag, publication/update date, or dated maintainer statement.
- Verify API names, package names, configuration keys, CLI flags, and compatibility claims before using them in prose or code.
- Distinguish released behavior from proposals, previews, open bugs, and workarounds.
- Resolve conflicts by weighing authority, directness, version fit, and freshness. Explain any conflict that changes the recommendation.

Prefer a directly relevant version-matched source over a higher-ranked but generic source. Use multiple sources when no single source covers a consequential claim or when independent confirmation materially increases confidence.

**Complete this step when:** every material factual claim and non-obvious code element is traceable to an opened source, and each consequential conflict is resolved or disclosed.

## 4. Synthesize the answer

Lead with the answer or recommendation. Then provide only the steps, code, comparison, evidence, freshness context, and caveats that help the user act.

- Put a Markdown link beside every material claim in the final response itself. Links present only in research notes, tool output, or a handoff do not count.
- Separate sourced facts from cross-source synthesis or recommendations, and label consequential inferences.
- Use exact dates when relative timing could be misunderstood.
- Keep code minimal and version-aligned; identify unverified adaptation points explicitly.
- State assumptions, evidence gaps, or lower-confidence inferences where they affect the result.
- Count unique citation destinations after drafting. A source list may repeat only URLs already cited in the answer.

For a multi-source implementation guide or comparison, read [references/output-template.md](references/output-template.md) and select the smallest matching pattern. For a simple lookup, answer directly without loading the template.

**Complete this step when:** the final response itself resolves the question, stays within the unique-URL limit, links every material factual claim to supporting evidence, and exposes every decision-relevant assumption, conflict, or evidence gap.

# Output Patterns

Choose the smallest pattern that fits the request. Emit only populated, useful sections, and keep citations beside the claims they support.

## Implementation guide

~~~markdown
# [Task]

[Direct recommendation.] [Source](URL)

## Steps

1. [Action and version-specific detail.] [Source](URL)
2. [Action and version-specific detail.] [Source](URL)

## Example

```language
[Minimal, verified code]
```

## Version notes and caveats

- [Freshness signal, compatibility boundary, assumption, or evidence gap.]
~~~

## Comparison

~~~markdown
# [Decision]

[Recommended option and the condition under which it wins.]

| Option | Best fit | Trade-offs | Evidence |
| --- | --- | --- | --- |
| [A] | [...] | [...] | [Source](URL) |
| [B] | [...] | [...] | [Source](URL) |

## Recommendation

[Explain the decision using the user's constraints.]

## Version notes and caveats

- [Freshness signal, unresolved conflict, or scope boundary.]
~~~

## Source-backed summary

~~~markdown
# [Topic]

[One-paragraph synthesis.] [Source](URL)

## Key findings

- [Finding.] [Source](URL)
- [Finding.] [Source](URL)

## What changed or remains uncertain

- [Relevant date/version change, conflict, or evidence gap.]
~~~

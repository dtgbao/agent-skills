# Output Template

Use this as the default format.

~~~markdown
# [topic]

## Key steps
- Step 1
- Step 2
- Step 3

## Sample code
```language
// minimal, version-aligned example
```

## Source links
1. [Source title](URL) — why it matters
2. [Source title](URL) — why it matters

## Last updated / recency note
- Best freshness signal found
- Version fit or mismatch note

## Confidence / caveats
- Confidence: high | medium | low
- Any conflicts, assumptions, or missing authoritative guidance
~~~

## Example

~~~markdown
# Unit testing in Nuxt v4

## Key steps
- Use the Nuxt test utilities package and a Vitest-based test runner.
- Configure the test environment using the Nuxt-supported test setup for component and app-context tests.
- Keep pure utility tests separate from Nuxt runtime tests so the environment stays fast.
- Prefer examples from version-matching Nuxt documentation or migration notes.

## Sample code
```ts
import { describe, it, expect } from 'vitest'

describe('sum', () => {
  it('adds values', () => {
    expect(1 + 1).toBe(2)
  })
})
```

## Source links
1. [Official docs](URL) — canonical setup guidance
2. [Stack Overflow thread](URL) — practical fix for a common setup issue

## Last updated / recency note
- Official docs page references Nuxt v4 APIs.
- Community thread is newer than many blog posts, but still secondary to docs.

## Confidence / caveats
- Confidence: medium
- Exact package names and config may change across RC vs stable releases.
~~~

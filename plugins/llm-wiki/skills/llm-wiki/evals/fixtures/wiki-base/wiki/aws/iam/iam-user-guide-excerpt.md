---
title: IAM user guide (excerpt)
kind: source
domain: aws/iam
summary: Excerpt of the AWS IAM user guide on policy types, evaluation order and roles.
tags: [aws, security]
sources: [raw/aws/iam/iam-user-guide-excerpt.md]
source_url: https://docs.aws.amazon.com/IAM/latest/UserGuide/
created: 2026-09-10
updated: 2026-09-10
---

# IAM user guide (excerpt)

## Source

- [raw/aws/iam/iam-user-guide-excerpt.md](../../../raw/aws/iam/iam-user-guide-excerpt.md)

## Summary

The guide lists the six IAM policy types and the basic evaluation rule: default deny,
explicit allow, and explicit deny overrides any allow. It defines roles and trust policies.

## Key takeaways

- Requests are denied by default.
- An explicit deny in any policy wins over any allow.
- Who can assume a role is set by the role's trust policy.

## Entities and concepts

- [Policy types](policy-types.md)
- [IAM role](iam-role.md)

## Contradictions and open questions

- None found.

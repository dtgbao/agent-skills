---
title: Service control policy (SCP)
kind: concept
domain: aws/organizations
summary: Organization policies that set the maximum permissions for accounts; they grant nothing.
tags: [aws, security, aws/iam]
sources: [raw/aws/iam/iam-user-guide-excerpt.md]
created: 2026-09-10
updated: 2026-09-10
---

# Service control policy (SCP)

An SCP sets the maximum permissions for the accounts in an organizational unit.
It grants no permissions. An action must be allowed by both the SCP and an
identity or resource policy ([policy types](../iam/policy-types.md)).

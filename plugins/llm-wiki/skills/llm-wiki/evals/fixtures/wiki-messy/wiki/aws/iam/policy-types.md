---
title: IAM policy types
kind: concept
domain: aws/iam
summary: The six kinds of AWS IAM policy and what each one controls.
tags: [security]
sources: [raw/aws/iam/iam-user-guide-excerpt.md]
created: 2026-09-10
updated: 2026-09-10
---

# IAM policy types

| Type | Attached to | Grants? |
|---|---|---|
| Identity-based | users, groups, roles | yes |
| Resource-based | resources such as S3 buckets | yes |
| Permissions boundary | users, roles | no, it caps |
| SCP | accounts, OUs | no, it caps |
| Session policy | a session | no, it caps |
| ACL | some resources | yes |

A permissions boundary limits both identity-based and resource-based policies for the
user or role it is attached to ([guide](iam-user-guide-excerpt.md)).

SCPs from AWS Organizations cap what accounts can do.

An explicit deny in any policy overrides any allow. See also [IAM role](iam-role.md).

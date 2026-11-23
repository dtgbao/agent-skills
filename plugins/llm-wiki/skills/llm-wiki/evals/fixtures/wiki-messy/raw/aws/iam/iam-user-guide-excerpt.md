# IAM user guide (excerpt, saved 2026-09-10)

## Policy types
AWS supports identity-based policies, resource-based policies, permissions boundaries,
service control policies (SCPs), session policies and ACLs.

## Evaluation
By default all requests are denied. An explicit allow overrides the default deny.
An explicit deny in any policy overrides any allow.

## Roles
A role is an identity with permissions that any trusted principal can assume.
Who can assume a role is set in its trust policy.

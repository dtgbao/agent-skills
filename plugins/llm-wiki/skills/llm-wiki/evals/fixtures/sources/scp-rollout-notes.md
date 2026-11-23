# SCP rollout notes (platform team, 2026-11-10)

Notes from the first week of the service control policy (SCP) rollout.

## What we did

- Created the OU `workloads/prod` and attached the SCP `deny-leave-org` to it.
- Attached `deny-unapproved-regions` at the root. It denies every action outside
  `eu-west-1` and `us-east-1`, except for global services.

## What we learned

- SCPs also restrict the management account. That is why we tested the deny-all SCP
  in the management account first, before any member account.
- An SCP document can have at most 5,120 characters. Our region policy hit the limit,
  so we split it into two policies.
- SCPs do not restrict service-linked roles. A deny in an SCP does not stop AWS
  services that act through their service-linked roles.

## Next steps

- Move `deny-unapproved-regions` from the root to each OU, so new OUs opt in.
- Write a runbook for SCP changes.

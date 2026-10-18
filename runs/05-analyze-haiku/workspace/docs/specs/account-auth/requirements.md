# Requirements Document

## Introduction

Account sign-up, sign-in, and password reset for the accounts service. End users sign up with email and password. Support staff can unlock accounts.

## Glossary

- **Accounts_Service**: the HTTP service that stores accounts and issues sessions.
- **Account**: a record with a unique email, compared case-insensitively, a password hash, and a status (`active` | `locked`).
- **Session**: a signed token that proves sign-in.
- **Mailer**: the external email delivery provider.
- **Tenant**: an organization boundary. Each Account belongs to exactly one Tenant. A support agent manages a set of Tenants.
- **Actor**: the authenticated user or system process that causes an action.
- **Role**: a named permission held by an Actor. The `support` Role grants unlock rights.
- **Account id**: the unique identifier of an Account.
- **Reset link**: a single-use link issued under Requirement 5.1.
- **Support agent**: an Actor that holds the `support` Role and manages the Tenants assigned to it.
- **Failed sign-in count**: the number of wrong-password sign-ins for one Account in the rolling 15-minute window of Requirement 2.3.

## Requirements

### Requirement 1: Sign up

**User Story:** As a visitor, I want to create an account, so that I can sign in.

#### Acceptance Criteria

1. WHEN a visitor submits an email, a password that satisfies Requirement 3.1 and Requirement 3.3, and a Tenant id, THE Accounts_Service SHALL create an Account in that Tenant with status `active`.
2. IF the email is not a valid RFC 5322 address, THEN THE Accounts_Service SHALL reject the request with error `invalid_email`. A valid RFC 5322 address is an addr-spec with no quoted local part and no comments.
3. WHEN an Account is created, THE Accounts_Service SHALL send a welcome email through the Mailer.
4. IF an Account already has the submitted email, compared case-insensitively, THEN THE Accounts_Service SHALL reject the request with error `email_taken`.
5. IF the password is shorter than 8 or longer than 64 characters, THEN THE Accounts_Service SHALL reject the request with error `invalid_password`.
6. IF the Mailer fails to deliver a message, THEN THE Accounts_Service SHALL retry 3 times over 10 minutes and record the failure. Retries occur at 2, 5 and 10 minutes after the first failed attempt. WHEN all retries fail, THE Accounts_Service SHALL write a delivery record with account id, message type, attempt count, last error and UTC timestamp. The sign-up request SHALL still succeed.
7. THE Accounts_Service SHALL enforce email uniqueness with a unique constraint on the normalized email. A request that violates the constraint SHALL be rejected with error `email_taken`. The normalized email is the submitted email with leading and trailing spaces removed and all letters converted to lower case. THE Accounts_Service SHALL store and compare only the normalized email.
8. IF the password fails Requirement 3.1 or Requirement 3.3, THEN THE Accounts_Service SHALL reject the sign-up with error `invalid_password` for a length failure, `weak_password` when only Requirement 3.3 fails, and `invalid_password` when both fail.
9. WHEN a sign-up fails more than one check, THE Accounts_Service SHALL return the first failing check in this order: unknown Tenant id (`invalid_tenant`), `invalid_email`, `email_taken`, `invalid_password` or `weak_password`.

### Requirement 2: Sign in

**User Story:** As a user, I want to sign in, so that I can use the product.

#### Acceptance Criteria

1. WHEN a user submits a matching email and password for an Account with status `active`, THE Accounts_Service SHALL issue a Session.
2. THE Accounts_Service SHALL respond to sign-in requests within 300 ms at the 95th percentile, at up to 100 requests per second.
3. IF five sign-in requests with a wrong password for the same Account occur within any rolling 15-minute window, THEN THE Accounts_Service SHALL set the Account status to `locked` and revoke all Sessions of that Account. A successful sign-in SHALL reset the count.
4. WHILE an Account is `locked`, THE Accounts_Service SHALL reject every sign-in for that Account with error `account_locked`, whether or not the password matches.
5. IF no Account has the submitted email, or the submitted password does not match the Account, THEN THE Accounts_Service SHALL reject the sign-in with error `invalid_credentials`.

### Requirement 3: Password rules

**User Story:** As a security officer, I want strong passwords, so that accounts resist guessing.

#### Acceptance Criteria

1. THE Accounts_Service SHALL accept passwords of 8–64 characters that satisfy Requirement 3.3.
2. THE Accounts_Service SHALL store passwords only as Argon2id hashes.
3. THE Accounts_Service SHALL reject any password that has no letter or no digit, with error `weak_password`.
4. THE Accounts_Service SHALL hash passwords with Argon2id using memory [m] KiB, iterations [t] and parallelism [p], with values that keep Requirement 2.2 true at 100 requests per second on [deployed capacity].

### Requirement 4: Sessions

**User Story:** As a user, I want to stay signed in, so that I do not sign in again each visit.

#### Acceptance Criteria

1. THE Accounts_Service SHALL issue Sessions that end only by idle revocation under Requirement 4.2, sign-out under Requirement 4.3, account lock under Requirement 2.3, password reset under Requirement 5.2, or an absolute lifetime of 12 hours from issue, with or without activity.
2. WHEN a Session receives no user-initiated request for 30 minutes, THE Accounts_Service SHALL revoke the Session. A page view or API request resets the timer. A token refresh SHALL NOT reset the timer.
3. WHEN a user signs out, THE Accounts_Service SHALL revoke the Session.
4. WHEN a Session reaches its absolute lifetime, THE Accounts_Service SHALL revoke the Session.

### Requirement 5: Password reset

**User Story:** As a user, I want to reset my password, so that I can recover my account.

#### Acceptance Criteria

1. WHEN a user requests a reset for an existing email, THE Accounts_Service SHALL email a single-use reset link through the Mailer that expires 60 minutes after it is issued.
2. WHEN a user opens a valid reset link and submits a new password that satisfies Requirement 3.1 and Requirement 3.3, THE Accounts_Service SHALL replace the password hash, mark the link used, and revoke all Sessions of that Account.
3. IF the reset link is invalid, expired, or used, THEN THE Accounts_Service SHALL reject the request with error `invalid_reset_link`.
4. IF no Account has the submitted email, THEN THE Accounts_Service SHALL return the same response as for an existing email and send no email.
5. IF the Mailer fails to deliver a message, THEN THE Accounts_Service SHALL retry 3 times over 10 minutes and record the failure. Retries occur at 2, 5 and 10 minutes after the first failed attempt. WHEN all retries fail, THE Accounts_Service SHALL write a delivery record with account id, message type, attempt count, last error and UTC timestamp. The reset request SHALL still succeed.
6. WHEN a new reset link is issued for an Account, THE Accounts_Service SHALL mark all earlier links for that Account as used.
7. IF two submissions use the same link at the same time, THEN THE Accounts_Service SHALL accept one and reject the other with error `invalid_reset_link`.
8. A password reset SHALL NOT change the status of a `locked` Account. The Account remains `locked` until unlocked under Requirement 6.1.
9. IF the new password fails Requirement 3.1 or Requirement 3.3, THEN THE Accounts_Service SHALL reject the request and SHALL NOT mark the link used. Use error `invalid_password` for a length failure, `weak_password` otherwise, and `invalid_password` when both fail.

### Requirement 6: Support unlock

**User Story:** As a support agent, I want to unlock accounts, so that locked users regain access.

#### Acceptance Criteria

1. WHEN a support agent unlocks an Account in a Tenant they manage, THE Accounts_Service SHALL set the Account status to `active` and reset its failed sign-in count to zero.
2. IF the caller lacks the `support` role, THEN THE Accounts_Service SHALL reject the unlock with error `forbidden`.
3. IF the caller has the `support` role but does not manage the Account's Tenant, THEN THE Accounts_Service SHALL reject the unlock with error `forbidden`.
4. IF the request has no valid Session, THEN THE Accounts_Service SHALL reject it with error `unauthenticated`.
5. IF no Account has the given id, THEN THE Accounts_Service SHALL reject the unlock with error `not_found`.
6. IF the Account status is already `active`, THEN THE Accounts_Service SHALL reject the unlock with error `not_locked`.
7. WHEN an unlock fails more than one check in Requirement 6, THE Accounts_Service SHALL return the first failing error in this order: `unauthenticated` (6.4), `forbidden` (6.2), `not_found` (6.5), `forbidden` (6.3), `not_locked` (6.6).

### Requirement 7: Audit

**User Story:** As a compliance officer, I want an audit trail, so that I can review account changes.

#### Acceptance Criteria

1. WHEN an Account status changes, THE Accounts_Service SHALL append an audit record with Account id, old status, new status, actor id, and UTC timestamp.
2. IF the audit store write fails, THEN THE Accounts_Service SHALL reject the status change with error `audit_unavailable`, except a change to `locked` under Requirement 2.3, which SHALL still be applied and whose audit record SHALL be queued for retry.
3. For a status change made under Requirement 2.3, the actor id SHALL be `system`.
4. THE Accounts_Service SHALL write the status change and the audit record in one transaction. IF the audit write fails, THEN the transaction SHALL roll back, except a change to `locked` under Requirement 2.3. That change SHALL be applied, and its audit record SHALL be queued for retry.
5. WHEN an Account is created, THE Accounts_Service SHALL append an audit record with old status `none`, new status `active`, actor id `system` and UTC timestamp, in the same transaction as the creation.
6. WHEN a queued audit record cannot be written, THE Accounts_Service SHALL keep it in storage separate from the audit store, retry it every 1 minute for 24 hours, and raise an alert when the retries end.

## Open Questions

- Count reset on reset: Requirement 5.2 does not say whether a password reset resets the failed sign-in count. Deferred by scripted user (round 3, F10).
- Letter and digit: Requirement 3.3 does not define non-ASCII letters or digits. Deferred by scripted user (round 3, F15).
- Argon2id values: placeholders [m], [t], [p] and [deployed capacity] in Requirement 3.4 are not filled. Round 3 F4 option A applied with placeholders.

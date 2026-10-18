# Requirements Document

## Introduction

Account sign-up, sign-in, and password reset for the accounts service. End users sign up with email and password. Support staff can unlock accounts.

## Glossary

- **Accounts_Service**: the HTTP service that stores accounts and issues sessions.
- **Account**: a record with a unique email, a password hash, and a status (`active` | `locked`).
- **Session**: a signed token that proves sign-in.
- **Mailer**: the external email delivery provider.

## Requirements

### Requirement 1: Sign up

**User Story:** As a visitor, I want to create an account, so that I can sign in.

#### Acceptance Criteria

1. WHEN a visitor submits an email and a password of 8–64 characters, THE Accounts_Service SHALL create an Account with status `active`.
2. IF the email is not a valid RFC 5322 address, THEN THE Accounts_Service SHALL reject the request with error `invalid_email`.
3. WHEN an Account is created, THE Accounts_Service SHALL send a welcome email through the Mailer.

### Requirement 2: Sign in

**User Story:** As a user, I want to sign in, so that I can use the product.

#### Acceptance Criteria

1. WHEN a user submits a matching email and password, THE Accounts_Service SHALL issue a Session.
2. THE Accounts_Service SHALL respond to sign-in requests quickly.
3. IF a user submits a wrong password 5 times in 15 minutes, THEN THE Accounts_Service SHALL set the Account status to `locked`.
4. WHILE an Account is `locked`, THE Accounts_Service SHALL reject sign-in with error `account_locked`.

### Requirement 3: Password rules

**User Story:** As a security officer, I want strong passwords, so that accounts resist guessing.

#### Acceptance Criteria

1. THE Accounts_Service SHALL accept passwords of 6–64 characters.
2. THE Accounts_Service SHALL store passwords only as Argon2id hashes.

### Requirement 4: Sessions

**User Story:** As a user, I want to stay signed in, so that I do not sign in again each visit.

#### Acceptance Criteria

1. THE Accounts_Service SHALL issue Sessions that never expire.
2. WHEN a Session is idle for 30 minutes, THE Accounts_Service SHALL revoke the Session.
3. WHEN a user signs out, THE Accounts_Service SHALL revoke the Session.

### Requirement 5: Password reset

**User Story:** As a user, I want to reset my password, so that I can recover my account.

#### Acceptance Criteria

1. WHEN a user requests a reset for an existing email, THE Accounts_Service SHALL email a single-use reset link through the Mailer.
2. WHEN a user opens a valid reset link and submits a new password, THE Accounts_Service SHALL replace the password hash.

### Requirement 6: Support unlock

**User Story:** As a support agent, I want to unlock accounts, so that locked users regain access.

#### Acceptance Criteria

1. WHEN a support agent unlocks an Account in a Tenant they manage, THE Accounts_Service SHALL set the Account status to `active`.
2. IF the caller lacks the `support` role, THEN THE Accounts_Service SHALL reject the unlock with error `forbidden`.

### Requirement 7: Audit

**User Story:** As a compliance officer, I want an audit trail, so that I can review account changes.

#### Acceptance Criteria

1. WHEN an Account status changes, THE Accounts_Service SHALL append an audit record with Account id, old status, new status, actor id, and UTC timestamp.
2. IF the audit store write fails, THEN THE Accounts_Service SHALL reject the status change with error `audit_unavailable`.

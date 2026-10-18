# Requirements Document

## Introduction

The Shortlinks API lets API clients create short links and resolve them. This feature adds a per-API-key request limit. Each API key may send at most 60 requests per minute. A client that exceeds the limit receives HTTP 429 and a Retry-After header in seconds. Operators use this feature to stop one client from overloading the service.

## Glossary

- **Shortlinks API**: The `handle(request)` entry point in `shortlinks/api.py`.
- **API Key**: A string in the request field `api_key` that matches an entry in `VALID_KEYS`.
- **Request**: One call to `handle()` with a dict argument.
- **Counted Request**: A Request whose API Key is in `VALID_KEYS` and that does not receive HTTP 401, 429 or 503.
- **Window**: A fixed 60-second period that starts at the first Counted Request of an API Key. When it ends, the next Counted Request of that API Key starts a new Window.
- **Limit**: The maximum of 60 counted Requests for one API Key within one Window.
- **Retry-After**: The HTTP response header that states, in whole seconds, how long a client waits before it sends again.
- **Request count storage**: The shared store that holds Counted Request counts and Window start times for all server instances.
- **Unavailable**: The Request count storage does not complete a read or write within 100 ms.

## Requirements

### Requirement 1: Per-key request limit

**User Story:** As an operator, I want each API key limited to 60 requests per minute, so that one client cannot overload the Shortlinks API.

#### Acceptance Criteria

1. WHEN a Request with a valid API Key arrives and that key has fewer than 60 counted Requests in the current Window, THE Shortlinks API SHALL process the Request and return the response the existing route returns.
2. WHEN a Request with a valid API Key arrives and that key already has 60 counted Requests in the current Window, THE Shortlinks API SHALL return HTTP status 429 with body `{"error": "rate limited"}`.
3. WHEN the Shortlinks API returns HTTP status 429, THE Shortlinks API SHALL include a `Retry-After` header whose value is the number of seconds, rounded up, until the current Window ends, with a minimum of 1.
4. IF a Request has no API Key or an API Key that is not in `VALID_KEYS`, THEN THE Shortlinks API SHALL return HTTP status 401 and SHALL NOT count the Request against any key's Limit.
5. WHEN Requests arrive for two different valid API Keys, THE Shortlinks API SHALL count the Requests for each key separately.
6. WHEN more than 60 Requests for one valid API Key arrive concurrently, THE Shortlinks API SHALL count each Request atomically, SHALL count no more than 60 of them as Counted Requests within the Window, and SHALL return HTTP status 429 with a Retry-After header for each Request beyond the Limit.
7. THE Shortlinks API SHALL keep Request counts in storage shared by all server instances, so that each Limit applies across all instances.
8. IF the Request count storage is Unavailable, THEN THE Shortlinks API SHALL return HTTP status 503 and SHALL NOT process the Request. This applies even when the API Key already has 60 Counted Requests in the current Window. If a count write does not complete within the time limit defined by Unavailable, the Request count storage SHALL discard that write, so that the Request is not counted. A Request with an API Key that is not in `VALID_KEYS` SHALL receive HTTP status 401 before the storage check. A Request that receives HTTP status 503 is not a Counted Request.

## Open Questions

- **F5 (EDGE, low, deferred)**: The spec does not say which clock sets the Window start and end across server instances. It also does not say whether a Request at exactly 60 seconds starts a new Window. Options: A) The Window start and end are read from the Request count storage clock. A Request at exactly 60 seconds after the Window start starts a new Window. B) THE Shortlinks API SHALL compute each Window from the Request count storage clock, so that all server instances use one clock.
- **R3-F4 (AMBIGUITY, low, deferred)**: "Counted Request" is defined by the 429 result, and the 429 result depends on the count. The counting order is not stated.
- **R3-F6 (ASSUMPTION, low, deferred)**: "existing route" (Requirement 1.1) and "server instance" (Requirement 1.7) are not defined in the Glossary.
- **R3-F7 (FAILURE, low, deferred)**: The response body for HTTP 401 and HTTP 503 is not defined.
- **R3-F8 (FAILURE, low, deferred)**: The spec does not say what happens when Request count storage loses data after a restart or eviction.

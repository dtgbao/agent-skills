# Requirements Document

## Introduction

The Shortlinks API serves create and resolve requests for callers that identify themselves with an API key. This feature limits each API key to 60 requests per minute per process. A caller that exceeds the limit receives a 429 response with a Retry-After header, so that one key cannot starve the others.

## Glossary

- **Shortlinks API**: The `handle(request, store)` function in `shortlinks/api.py`. It takes a request dict and returns a Response.
- **Response**: A dict with keys `status` (int), `headers` (dict[str, str]) and `body` (dict).
- **API Key**: The string in `request["api_key"]`. A key is valid when it is in `VALID_KEYS`.
- **Rate Limiter**: The component that counts requests per API Key and decides allow or reject. Its state is held in process memory, per process, and is lost on restart.
- **Clock**: One injectable monotonic function that returns the current time in seconds. The Rate Limiter reads time only from the Clock.
- **Window**: The interval (now-60, now]. A Counted Request made at time t is counted when t <= now and now < t+60, and is not counted when now >= t+60.
- **Limit**: 60 requests per Window per API Key.
- **Counted Request**: A request with a valid API Key that the Rate Limiter allows without error. A rejected request is not counted.
- **Retry-After**: The `headers["Retry-After"]` value. It is the decimal string of the number of whole seconds a caller waits before the next request can succeed.

## Requirements

### Requirement 1: Per-key request limit

**User Story:** As an API operator, I want each API Key limited to 60 requests per Window, so that one caller cannot overload the service.

#### Acceptance Criteria

1. WHEN a request with a valid API Key arrives and that key has fewer than 60 Counted Requests in the current Window, THE Rate Limiter SHALL allow the request and THE Shortlinks API SHALL route it as it does today.
2. WHEN a request with a valid API Key arrives and that key has 60 Counted Requests in the current Window, THE Shortlinks API SHALL return status 429.
3. THE Rate Limiter SHALL count each API Key separately, so that requests from key A do not change the count of key B.
4. IF a request has a missing or invalid API Key, THEN THE Shortlinks API SHALL return status 401 and THE Rate Limiter SHALL NOT change any count.
5. THE Rate Limiter SHALL count every route (POST /links, GET /links/<code>, and unknown paths) toward the Limit.
6. THE Rate Limiter SHALL perform the count check and the count increment for one request as one atomic step per API Key. FOR each request, THE Rate Limiter SHALL read the Clock once, inside the atomic step, and SHALL allow the request if and only if the key has fewer than 60 Counted Requests in the Window at that reading. Atomic steps for one key SHALL be totally ordered. THE Shortlinks API SHALL answer each other request with status 429 and a Retry-After per Requirement 2.
7. THE Rate Limiter SHALL read the current time only from the Clock.
8. IF a request has a valid API Key and the Rate Limiter raises an exception or the Clock raises an exception, THEN THE Shortlinks API SHALL route the request, SHALL NOT change any count, and SHALL write one log record at level ERROR with the exception text. THE key check of criterion 1.4 SHALL run first. The limit is not enforced while the exception persists. THE Shortlinks API SHALL write at most one ERROR record per 60 seconds for the same exception text.
9. THE Limit SHALL apply per process. WHERE N processes serve the same API Key, THE effective limit is up to 60*N per Window, and counts reset on process restart.

### Requirement 2: Retry-After on rejection

**User Story:** As an API caller, I want to know how long to wait after a 429, so that I can retry without guessing.

#### Acceptance Criteria

1. WHEN THE Shortlinks API returns status 429, THE Shortlinks API SHALL set `headers["Retry-After"]` to the decimal string of an integer.
2. WHEN THE Shortlinks API returns status 429, THE Shortlinks API SHALL set Retry-After to ceil(t_oldest + 60 - now), where t_oldest is the time of the oldest Counted Request in the Window. The value is clamped to 1–60 before it is sent.
3. WHEN THE Shortlinks API returns status 429, THE Shortlinks API SHALL return the body `{"error": "rate limit exceeded"}`.
4. THE Shortlinks API SHALL NOT include the key `Retry-After` in `headers` on any response with a status other than 429.
5. THE Rate Limiter SHALL keep one last-seen Clock value for the process. IF a Clock reading is less than the last-seen value, THEN THE Rate Limiter SHALL use the last-seen value as `now` and as the time stored for any Counted Request. IF a Clock reading is greater than the last-seen value by more than 60 seconds, THEN THE Rate Limiter SHALL treat it as a Clock error per criterion 1.8 and SHALL NOT update the last-seen value.

### Requirement 3: Recovery after the Window

**User Story:** As an API caller, I want my requests accepted again after the wait, so that a short burst does not lock me out.

#### Acceptance Criteria

1. WHEN the number of seconds in Retry-After has passed after a 429, THE Rate Limiter SHALL allow the next request from that key, if the key then has fewer than 60 Counted Requests in the Window.
2. THE Rate Limiter SHALL NOT count a rejected (429) request toward the Limit.
3. IF a key sends requests continuously during the wait, THEN THE Rate Limiter SHALL keep the Retry-After value from growing past 60 seconds.

## Open Questions

- F6 (Requirement 3.3, 2.1, 3.2; low): "continuously during the wait" has no measurable meaning, and 3.3 repeats the 1–60 bound of 2.1. Deferred.
- F7 (Requirement 1.1, 1.4, 1.5, Introduction; low): the Introduction says "create and resolve requests" but 1.5 counts unknown paths. Counting of requests rejected after the key check, and the meaning of an invalid non-string api_key, are unstated. Deferred.
- R3-F11 (Requirement 1.8, 1.6; low): an exception after the increment may leave a partial count. Rollback is unspecified. Deferred.
- R3-F12 (Requirement 2.5, 1.6, 1.4; low): last-seen Clock value is per process but atomicity is per API Key. A 401 request may read the Clock. Deferred.
- R3-F13 (Requirement 1.7, 2.5, Glossary Clock; low): a Clock value that is NaN, infinite or negative does not raise, so 1.8 does not apply. Deferred.
- R3-F14 (Glossary Limit, Requirement 1.1, 1.2, 1.9; low): Limit says 60 per Window per API Key. 1.9 says the effective limit is up to 60*N. Deferred.
- R3-F15 (Requirement 1.1, 1.6, 1.8, 1.9; low): "route", "process" and "VALID_KEYS" are not in the Glossary. The meaning of "concurrent" is unclear. Deferred.

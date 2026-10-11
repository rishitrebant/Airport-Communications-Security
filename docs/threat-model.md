# Threat Model

## Assets

1. **Operational messages** — inter-departmental communications containing flight, gate, baggage and maintenance information.
2. **User credentials** — authentication data for airport personnel.
3. **Audit records** — evidence of security events and system activity.
4. **System availability** — the communication platform must remain operational.

## Threat Actors

| Actor | Capability | Motivation |
|-------|-----------|------------|
| Disgruntled employee | Valid credentials, knowledge of system | Data theft, sabotage |
| External attacker | Network access, no credentials | Disruption, intelligence gathering |
| Insider with elevated curiosity | Valid credentials, wrong department | Unauthorized information access |

## Threats and Mitigations

### T1 — Unauthorized Access

- **Attack:** User attempts to access admin functions or messages from another department.
- **Impact:** Confidentiality breach, privilege escalation.
- **Mitigation:** Server-side role and department checks on every route. Access denials logged.
- **Test:** Lab Scenario 1 — operator's `can_admin()` returns False; route returns 403.

### T2 — Message Tampering

- **Attack:** Attacker modifies message content in transit or at rest.
- **Impact:** Integrity violation — false operational instructions could cause safety incidents.
- **Mitigation:** HMAC-SHA-256 computed over canonical message representation (UUID, sender, department, timestamp, body). Constant-time comparison on read.
- **Limitation:** HMAC does not provide non-repudiation. It proves the application generated the tag, not that a specific human authored the message.
- **Test:** Lab Scenario 2 — modified body fails HMAC verification.

### T3 — Replay Attack

- **Attack:** Attacker re-submits a previously valid message to cause duplicate actions.
- **Impact:** Operational confusion from duplicate instructions.
- **Mitigation:** Unique message UUID (idempotency key) with database uniqueness constraint. Duplicate submissions rejected and logged.
- **Test:** Lab Scenario 3 — duplicate UUID rejected.

### T4 — Brute-Force Authentication

- **Attack:** Automated login attempts to guess credentials.
- **Impact:** Account compromise.
- **Mitigation:** Flask-Limiter rate limiting (10 attempts/minute on login). Failed logins logged.
- **Limitation:** Application-level rate limiting does not protect against distributed attacks or network-layer flooding.
- **Test:** Lab Scenario 4 — rate limiter configuration verified.

### T5 — SQL Injection

- **Attack:** Malicious input in authentication or query parameters to manipulate database queries.
- **Impact:** Authentication bypass, data exfiltration.
- **Mitigation:** SQLAlchemy ORM with parameterized queries. No raw SQL.
- **Test:** Lab Scenario 5 — injection payload treated as literal string.

### T6 — Cross-Site Request Forgery

- **Attack:** Malicious site tricks authenticated user's browser into submitting state-changing requests.
- **Impact:** Unauthorized message sending or account changes.
- **Mitigation:** Flask-WTF CSRF tokens on all POST forms. SameSite=Lax cookie attribute.

### T7 — Cross-Site Scripting

- **Attack:** Injected script executes in another user's browser.
- **Impact:** Session theft, data exfiltration.
- **Mitigation:** Jinja2 autoescaping enabled by default. No `|safe` filters on user content.

### T8 — Transport Interception

- **Attack:** Network eavesdropping on unencrypted HTTP traffic.
- **Impact:** Credential theft, message interception.
- **Mitigation:** Architecture designed for HTTPS/TLS. Local demo procedure documented separately.
- **Limitation:** Local development typically uses HTTP. TLS requires certificate setup.

## STRIDE Summary

| Threat | STRIDE Category | Risk Level | Implemented Mitigation |
|--------|----------------|------------|----------------------|
| T1 | Elevation of Privilege | High | Role/department authorization |
| T2 | Tampering | High | HMAC-SHA-256 integrity |
| T3 | Repudiation / Tampering | Medium | UUID uniqueness + audit log |
| T4 | Spoofing | High | Rate limiting + audit log |
| T5 | Tampering / Info Disclosure | High | Parameterized queries |
| T6 | Spoofing | Medium | CSRF tokens |
| T7 | Tampering / Info Disclosure | Medium | Output escaping |
| T8 | Info Disclosure | High | TLS (documented) |

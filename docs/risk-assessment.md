# Risk Assessment Matrix

| ID | Vulnerability | Impact | Likelihood | Risk Level | Mitigation | Status |
|----|-------------|--------|------------|------------|------------|--------|
| R1 | Unauthorized access to admin functions | High — privilege escalation | Medium | High | Server-side role checks, 403 on denial | Implemented & tested |
| R2 | Message tampering at rest or in transit | High — false operational data | Medium | High | HMAC-SHA-256 integrity tags | Implemented & tested |
| R3 | Replay/duplicate message submission | Medium — operational confusion | Medium | Medium | UUID uniqueness constraint + audit | Implemented & tested |
| R4 | Brute-force password attacks | High — account compromise | High | High | Rate limiting (10/min login) + audit | Implemented & tested |
| R5 | SQL injection | Critical — full DB access | Low (ORM used) | Medium | Parameterized queries via SQLAlchemy | Implemented & tested |
| R6 | Cross-site request forgery | Medium — unauthorized actions | Medium | Medium | CSRF tokens on all forms | Implemented |
| R7 | Cross-site scripting | Medium — session hijack | Low (autoescaping) | Low | Jinja2 autoescaping | Implemented |
| R8 | Transport interception | High — credential/message theft | High (no TLS) | High | TLS documented, local demo pending | Partially implemented |
| R9 | Plaintext password storage | Critical — mass compromise | N/A (prevented) | Low | Werkzeug password hashing | Implemented & tested |
| R10 | Session fixation/hijack | Medium — impersonation | Medium | Medium | HttpOnly + SameSite cookies, logout invalidation | Implemented |
| R11 | DDoS at network level | High — service unavailability | Medium | High | App-level rate limiting only; documented limitation | Acknowledged limitation |
| R12 | Credential leakage in logs | Medium — credential exposure | Low | Low | Sanitized audit logging; no secrets in logs | Implemented |

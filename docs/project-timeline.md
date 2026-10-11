# Project Timeline

| Phase | Task | Status | Target Date |
|-------|------|--------|-------------|
| 0 | Repository setup and planning | **Completed** | — |
| 1 | Application skeleton, configuration, database | **Completed** | — |
| 2 | Authentication, messaging, permissions | **Completed** | — |
| 3 | Security controls (HMAC, replay, rate limit, CSRF, audit) | **Completed** | — |
| 4 | Attack simulation lab (5 scenarios) | **Completed** | — |
| 5 | Results dashboard, CSV/JSON export | **Completed** | — |
| 6 | UI polish — aviation dashboard theme | **Completed** | — |
| — | **Midterm checkpoint** | **Ready** | TBD |
| 7 | Academic documentation (synopsis, threat model, architecture) | **Completed** | — |
| 8 | TLS local demonstration and Wireshark walkthrough | Planned | TBD |
| 9 | Network segmentation and firewall documentation | Planned | TBD |
| 10 | Incident response workflow documentation | Planned | TBD |
| 11 | Final report with observed results | Planned | TBD |
| 12 | Viva preparation | Planned | TBD |
| 13 | Final validation and release | Planned | TBD |

## Completed Work (as of midterm)

- Flask application with 6 demo users across 4 departments
- Login/logout with secure password hashing
- Server-enforced role-based and department-based permissions
- Messaging system: compose, inbox, sent, message detail with integrity status
- HMAC-SHA-256 message integrity verification
- Replay/duplicate prevention via UUID uniqueness
- Rate limiting on login and compose endpoints
- CSRF protection on all forms
- Security audit logging with filterable viewer
- Attack simulation lab with 5 predefined scenarios
- Results dashboard with JSON/CSV export
- 27 automated tests — all passing
- Academic documentation: synopsis, architecture, threat model, risk assessment, timeline

## Planned Work (post-midterm)

- TLS demonstration with local certificates
- Wireshark traffic analysis walkthrough
- Incident response workflow
- Enhanced analytics and performance metrics
- Final report with complete observed results
- Viva preparation document
- Additional test coverage

# Build Status

**Last updated:** 2026-10-11
**Milestone:** Midterm checkpoint — READY

## Phase Checklist

| Phase | Description | Status |
|-------|-------------|--------|
| 0 | Repository inspection and planning | Done |
| 1 | Foundation and architecture | Done |
| 2 | Functional application (auth, messaging, permissions) | Done |
| 3 | Security controls (HMAC, replay, rate limit, CSRF, audit) | Done |
| 4 | Attack simulation lab (5 scenarios) | Done |
| 5 | Results dashboard and exports | Done |
| 6 | UI polish | Done |
| 7 | Academic documentation | Done |
| 8 | Validation and release | Pending (post-midterm) |

## Working Features

- Login/logout with secure password hashing (Werkzeug)
- 6 demo users across 4 airport departments + admin + security analyst
- Server-enforced role-based and department-based access control
- Messaging: compose, inbox, sent, message detail with HMAC integrity indicator
- HMAC-SHA-256 message integrity with constant-time comparison
- Replay/duplicate prevention via UUID uniqueness
- Rate limiting: 10/min on login, 20/min on compose
- CSRF protection on all POST forms
- Security audit logging with filterable viewer
- Attack simulation lab with 5 scenarios (unauthorized access, tampering, replay, rate limit, SQLi)
- Results dashboard with stats, table, JSON and CSV export
- Aviation-themed dark UI with responsive layout
- 27 automated tests — all passing

## Test Command

```bash
source venv/bin/activate
python -m pytest tests/ -v
```

## Startup Command

```bash
source venv/bin/activate
python seed.py       # first time only
python run.py        # starts on port 5000
```

## Remaining Work

- TLS local demonstration with Wireshark
- Network segmentation documentation
- Incident response workflow
- Final report
- Viva preparation document
- Additional optional test scenarios

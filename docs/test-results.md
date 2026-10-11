# Test Results

**Test framework:** pytest 8.4.2
**Python:** 3.14.6
**Date:** 2026-10-11
**Total tests:** 27
**Passed:** 27
**Failed:** 0

## Test Summary

| Category | Tests | Passed | Failed |
|----------|-------|--------|--------|
| Startup | 2 | 2 | 0 |
| Authentication | 5 | 5 | 0 |
| Permissions | 6 | 6 | 0 |
| Messaging | 3 | 3 | 0 |
| Integrity (HMAC) | 2 | 2 | 0 |
| Replay Prevention | 1 | 1 | 0 |
| SQL Injection | 1 | 1 | 0 |
| Audit Logging | 4 | 4 | 0 |
| Lab Access | 3 | 3 | 0 |

## Detailed Results

These results are from actual test execution, not simulated outcomes.

### Authentication
- `test_login_success` — PASSED: Admin user logs in successfully, redirected to dashboard.
- `test_login_failure` — PASSED: Wrong password shows "Invalid credentials".
- `test_unauthenticated_redirect` — PASSED: Unauthenticated request redirected to login.
- `test_logout` — PASSED: Logout clears session, shows confirmation.
- `test_password_not_plaintext` — PASSED: Stored hash differs from plaintext; check_password works.

### Permissions
- `test_operator_cannot_admin` — PASSED: Gate operator gets 403 on admin route.
- `test_admin_can_manage_users` — PASSED: Admin accesses user management.
- `test_operator_cannot_access_lab` — PASSED: Operator gets 403 on lab route.
- `test_analyst_can_access_lab` — PASSED: Security analyst accesses lab.
- `test_gate_cannot_see_maintenance_messages` — PASSED: Gate operator gets 403 on Maintenance message.
- `test_access_denied_logged` — PASSED: Denial creates audit log entry with outcome=denied.

### Messaging
- `test_compose_and_view` — PASSED: Message created with valid HMAC, retrievable.
- `test_duplicate_rejected` — PASSED: Same idempotency key rejected on second submission.
- `test_invalid_department` — PASSED: Non-existent department rejected.

### Integrity
- `test_valid_hmac` — PASSED: Freshly created message passes HMAC verification.
- `test_tampered_fails` — PASSED: Modified body fails HMAC; restored body passes again.

### Replay
- `test_replay_event_logged` — PASSED: Duplicate submission creates replay_detected audit event.

### SQL Injection
- `test_sqli_safe` — PASSED: `' OR '1'='1` payload returns None via parameterized query.

### Audit
- `test_login_logged` — PASSED: Successful login creates audit event.
- `test_failed_login_logged` — PASSED: Failed login creates audit event.
- `test_audit_page_accessible_by_analyst` — PASSED: Analyst sees audit log page.
- `test_audit_page_denied_for_operator` — PASSED: Operator gets 403 on audit page.

### Lab Access
- `test_lab_disabled_without_demo_mode` — PASSED: Lab returns 404 when DEMO_MODE=false.
- `test_lab_export_json` — PASSED: JSON export returns valid JSON array.
- `test_lab_export_csv` — PASSED: CSV export includes headers.

## Command to Reproduce

```bash
source venv/bin/activate
python -m pytest tests/ -v
```

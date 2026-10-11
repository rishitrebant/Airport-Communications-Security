# Midterm Demonstration Script

**Duration:** 5–7 minutes

## 1. Introduction (1 min)

Explain the project problem: airport ground operations require secure inter-departmental messaging. Show the architecture diagram from `docs/architecture.md`. Highlight the security controls: authentication, authorization, HMAC integrity, replay prevention, rate limiting, audit logging.

## 2. Login and Dashboard (1 min)

- Open `http://localhost:5001` in a browser.
- Log in as `ops_controller` / `OpsPass123!`.
- Show the Operations Dashboard with message counts, blocked requests and security events.
- Point out the sidebar navigation based on the user's role (operator sees only messaging).

## 3. Messaging Workflow (1 min)

- Navigate to Compose. Send a message to Gate Operations: "Flight BA456 arriving Gate C3. Begin turnaround."
- Navigate to Sent to see the message listed.
- Navigate to Inbox to see all messages for Operations Control.
- Click a message to view its detail, including the HMAC integrity status showing "HMAC Verified".

## 4. Access Control Demonstration (1 min)

- Log out. Log in as `gate_agent` / `GatePass123!`.
- Show that the sidebar does not show Admin, Audit Log or Attack Lab sections.
- Attempt to access `/admin/users` directly — show the 403 Forbidden error.
- Log in as `admin` / `AdminPass123!` and navigate to the Audit Log.
- Filter by `access_denied` to show the recorded denial event.

## 5. Attack Lab — Message Tampering (1 min)

- Log in as `sec_analyst` / `SecPass123!`.
- Navigate to Attack Lab.
- Run "Scenario 2 — Message Tampering".
- Show the result: original message passes HMAC, tampered message fails. PASS status.
- Run "Scenario 1 — Unauthorised Access" to show authorization check works.

## 6. Results Dashboard (30 sec)

- Navigate to Results.
- Show the test results table with run IDs, scenarios, expected vs observed outcomes, pass/fail status.
- Demonstrate JSON export.

## 7. Automated Tests (30 sec)

Show terminal output of `pytest tests/ -v` — all 27 tests passing, covering authentication, permissions, messaging, integrity, replay, SQL injection, audit logging and lab access.

## 8. Next Steps (30 sec)

- TLS demonstration with local certificates and Wireshark analysis.
- Incident response workflow.
- Final report with comprehensive observed results.
- Viva preparation.

# Airport Communications Security

Threat Modelling, Attack Simulation and a Layered Defence Prototype for Airport Ground Operations.

A simulated airport operations communication system for the **Security Attack and Defense** university course. Demonstrates security controls, attack scenarios and measurable defence outcomes.

> **Educational simulation only.** Does not connect to real airport infrastructure.

## Features

- Secure login with password hashing and session management
- Role-based access: Operator, Admin, Security Analyst
- Department-based messaging: Operations Control, Gate Operations, Baggage Handling, Maintenance
- HMAC-SHA-256 message integrity verification
- Replay/duplicate prevention
- Rate limiting on login and messaging
- CSRF protection
- Security audit logging with filters
- Attack simulation lab (5 scenarios)
- Results dashboard with JSON/CSV export
- Aviation-themed dark dashboard UI
- 27 automated tests

## Requirements

- Python 3.11+
- pip

## Quick Start

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create environment file
cp .env.example .env
# Edit .env — set SECRET_KEY and HMAC_SECRET to random values, set DEMO_MODE=true

# 4. Seed the database
python seed.py

# 5. Start the server
python run.py
```

Open http://localhost:5000 in your browser.

## Demo Accounts

| Username | Password | Role | Department |
|----------|----------|------|------------|
| admin | AdminPass123! | Admin | Operations Control |
| ops_controller | OpsPass123! | Operator | Operations Control |
| gate_agent | GatePass123! | Operator | Gate Operations |
| baggage_handler | BagPass123! | Operator | Baggage Handling |
| maint_tech | MaintPass123! | Operator | Maintenance |
| sec_analyst | SecPass123! | Security Analyst | Operations Control |

## Running Tests

```bash
source venv/bin/activate
python -m pytest tests/ -v
```

## Attack Lab

1. Log in as `sec_analyst` or `admin`.
2. Navigate to **Attack Lab** in the sidebar.
3. Run any of the 5 predefined scenarios.
4. View results in the **Results** dashboard.
5. Export results as JSON or CSV.

All tests run against the application's own security controls using synthetic data. No external targets are contacted.

## Project Structure

```
app/             — Flask application (models, routes, templates, static)
tests/           — Automated tests (pytest)
docs/            — Academic documentation
config.py        — Configuration
seed.py          — Demo data provisioning
run.py           — Entry point
requirements.txt — Dependencies
```

## Documentation

See the `docs/` directory for:
- Project synopsis
- Architecture and data flow diagram
- Threat model
- Risk assessment
- Project timeline
- Demo script
- Test results

## Limitations

- TLS requires local certificate setup (not enabled by default)
- Rate limiting is application-level only
- HMAC proves application-generated integrity, not individual human authorship
- This is an educational simulation, not production aviation software

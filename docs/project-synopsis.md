# Airport Communications Security — Project Synopsis

**Course:** Security Attack and Defense
**Project Title:** Airport Communications Security
**Subtitle:** Threat Modelling, Attack Simulation and a Layered Defence Prototype for Airport Ground Operations

## Problem Statement

Airport ground operations rely on inter-departmental communication for coordinating flights, baggage handling, gate assignments and maintenance. These communications are vulnerable to unauthorized access, message tampering, replay attacks and denial of service. A compromise could lead to operational disruption, safety incidents or data leakage.

## Objectives

1. Build a simulated airport operations messaging system with role-based access control across four departments (Operations Control, Gate Operations, Baggage Handling, Maintenance).
2. Implement layered security controls: authentication, authorization, HMAC-based message integrity, replay prevention, rate limiting and audit logging.
3. Create a controlled attack simulation lab that demonstrates threat scenarios against the application's own defenses.
4. Produce measurable, repeatable test results comparing expected vulnerable behavior against observed protected-system outcomes.
5. Document the threat model, risk assessment and security architecture for academic evaluation.

## Methodology

- **Threat modelling:** Identify attack surfaces using a structured approach covering authentication, data integrity, availability and transport security.
- **Defence implementation:** Apply defence-in-depth with server-side enforcement of all security controls.
- **Attack simulation:** Execute predefined scenarios (unauthorized access, message tampering, replay, rate limiting, SQL injection) within a controlled lab using synthetic data.
- **Measurement:** Record test outcomes, generate audit evidence and export results for analysis.

## Scope and Limitations

This is an educational simulation. It does not connect to real airport infrastructure, air traffic control or aviation systems. Demo credentials are for local use only. The TLS demonstration requires additional local certificate setup. Rate limiting operates at the application level and does not protect against network-level DDoS.

## Team

- Member 1 — TBD
- Member 2 — TBD
- Member 3 — TBD

## Evaluation Dates

- Midterm evaluation: TBD
- Final evaluation: TBD

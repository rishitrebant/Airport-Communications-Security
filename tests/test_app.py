import uuid
import json
import hmac
import hashlib
from datetime import datetime, timezone

from app.models import User, Message, AuditLog
from tests.conftest import login


class TestStartup:
    def test_app_creates(self, app):
        assert app is not None

    def test_login_page_loads(self, client):
        r = client.get("/login")
        assert r.status_code == 200
        assert b"Airport Communications Security" in r.data


class TestAuth:
    def test_login_success(self, client, users):
        r = login(client, "admin", "Admin123!")
        assert r.status_code == 200
        assert b"Dashboard" in r.data

    def test_login_failure(self, client, users):
        r = login(client, "admin", "wrong")
        assert b"Invalid credentials" in r.data

    def test_unauthenticated_redirect(self, client):
        r = client.get("/", follow_redirects=False)
        assert r.status_code == 302

    def test_logout(self, client, users):
        login(client, "admin", "Admin123!")
        r = client.get("/logout", follow_redirects=True)
        assert b"Logged out" in r.data

    def test_password_not_plaintext(self, users):
        assert users["admin"].password_hash != "Admin123!"
        assert users["admin"].check_password("Admin123!")
        assert not users["admin"].check_password("wrong")


class TestPermissions:
    def test_operator_cannot_admin(self, client, users):
        login(client, "gate", "Gate123!")
        r = client.get("/admin/users", follow_redirects=False)
        assert r.status_code == 403

    def test_admin_can_manage_users(self, client, users):
        login(client, "admin", "Admin123!")
        r = client.get("/admin/users")
        assert r.status_code == 200

    def test_operator_cannot_access_lab(self, client, users, app):
        login(client, "gate", "Gate123!")
        r = client.get("/lab/", follow_redirects=False)
        assert r.status_code == 403

    def test_analyst_can_access_lab(self, client, users, app):
        login(client, "analyst", "Sec123!")
        r = client.get("/lab/")
        assert r.status_code == 200

    def test_gate_cannot_see_maintenance_messages(self, client, users, db, app):
        login(client, "ops", "Ops123!")
        msg_uuid = str(uuid.uuid4())
        now = datetime.now(timezone.utc)
        tag, ts = Message.compute_hmac_for(msg_uuid, users["ops"].id, "Maintenance", now, "test")
        msg = Message(message_uuid=msg_uuid, sender_id=users["ops"].id,
                      recipient_department="Maintenance", subject="Test",
                      body="test", timestamp=now, timestamp_str=ts, hmac_tag=tag)
        db.session.add(msg)
        db.session.commit()
        client.get("/logout")

        login(client, "gate", "Gate123!")
        r = client.get(f"/messages/{msg.id}", follow_redirects=False)
        assert r.status_code == 403

    def test_access_denied_logged(self, client, users, db):
        login(client, "gate", "Gate123!")
        client.get("/admin/users")
        event = AuditLog.query.filter_by(event_type="access_denied").first()
        assert event is not None
        assert event.outcome == "denied"


class TestMessaging:
    def test_compose_and_view(self, client, users):
        login(client, "ops", "Ops123!")
        key = str(uuid.uuid4())
        r = client.post("/messages/compose", data={
            "department": "Gate Operations",
            "subject": "Test turnaround",
            "body": "Begin turnaround at Gate B7",
            "idempotency_key": key,
        }, follow_redirects=True)
        assert b"Message sent" in r.data

        msg = Message.query.filter_by(message_uuid=key).first()
        assert msg is not None
        assert msg.verify_integrity()

    def test_duplicate_rejected(self, client, users):
        login(client, "ops", "Ops123!")
        key = str(uuid.uuid4())
        client.post("/messages/compose", data={
            "department": "Gate Operations", "subject": "Dup test",
            "body": "Test body", "idempotency_key": key,
        })
        r = client.post("/messages/compose", data={
            "department": "Gate Operations", "subject": "Dup test 2",
            "body": "Test body 2", "idempotency_key": key,
        }, follow_redirects=True)
        assert b"Duplicate" in r.data

    def test_invalid_department(self, client, users):
        login(client, "ops", "Ops123!")
        r = client.post("/messages/compose", data={
            "department": "Nonexistent", "subject": "X", "body": "Y",
            "idempotency_key": str(uuid.uuid4()),
        }, follow_redirects=True)
        assert b"Invalid department" in r.data


class TestIntegrity:
    def test_valid_hmac(self, client, users, app):
        login(client, "ops", "Ops123!")
        key = str(uuid.uuid4())
        client.post("/messages/compose", data={
            "department": "Gate Operations", "subject": "Integrity",
            "body": "Check integrity", "idempotency_key": key,
        })
        msg = Message.query.filter_by(message_uuid=key).first()
        assert msg.verify_integrity()

    def test_tampered_fails(self, client, users, app):
        login(client, "ops", "Ops123!")
        key = str(uuid.uuid4())
        client.post("/messages/compose", data={
            "department": "Gate Operations", "subject": "Tamper test",
            "body": "Original body", "idempotency_key": key,
        })
        msg = Message.query.filter_by(message_uuid=key).first()
        original_body = msg.body
        msg.body = "TAMPERED body"
        assert not msg.verify_integrity()
        msg.body = original_body
        assert msg.verify_integrity()


class TestReplay:
    def test_replay_event_logged(self, client, users, db):
        login(client, "ops", "Ops123!")
        key = str(uuid.uuid4())
        client.post("/messages/compose", data={
            "department": "Gate Operations", "subject": "R1",
            "body": "Body", "idempotency_key": key,
        })
        client.post("/messages/compose", data={
            "department": "Gate Operations", "subject": "R2",
            "body": "Body2", "idempotency_key": key,
        })
        event = AuditLog.query.filter_by(event_type="replay_detected").first()
        assert event is not None


class TestSQLInjection:
    def test_sqli_safe(self, client, users):
        login(client, "admin", "Admin123!")
        payload = "' OR '1'='1"
        result = User.query.filter_by(username=payload).first()
        assert result is None


class TestAudit:
    def test_login_logged(self, client, users, db):
        login(client, "admin", "Admin123!")
        event = AuditLog.query.filter_by(event_type="login").first()
        assert event is not None
        assert event.outcome == "success"

    def test_failed_login_logged(self, client, users, db):
        login(client, "admin", "wrong")
        event = AuditLog.query.filter_by(event_type="login_failed").first()
        assert event is not None

    def test_audit_page_accessible_by_analyst(self, client, users):
        login(client, "analyst", "Sec123!")
        r = client.get("/admin/audit")
        assert r.status_code == 200

    def test_audit_page_denied_for_operator(self, client, users):
        login(client, "gate", "Gate123!")
        r = client.get("/admin/audit", follow_redirects=False)
        assert r.status_code == 403


class TestLabAccess:
    def test_lab_disabled_without_demo_mode(self, app, users):
        app.config["DEMO_MODE"] = False
        with app.test_client() as c:
            login(c, "analyst", "Sec123!")
            r = c.get("/lab/", follow_redirects=False)
            assert r.status_code == 404

    def test_lab_export_json(self, client, users):
        login(client, "analyst", "Sec123!")
        r = client.get("/lab/export/json")
        assert r.status_code == 200
        data = json.loads(r.data)
        assert isinstance(data, list)

    def test_lab_export_csv(self, client, users):
        login(client, "analyst", "Sec123!")
        r = client.get("/lab/export/csv")
        assert r.status_code == 200
        assert b"run_id" in r.data

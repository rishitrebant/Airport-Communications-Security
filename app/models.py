import uuid
import hmac
import hashlib
from datetime import datetime, timezone

from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db

DEPARTMENTS = ["Operations Control", "Gate Operations", "Baggage Handling", "Maintenance"]
ROLES = ["operator", "admin", "security_analyst"]


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="operator")
    department = db.Column(db.String(50), nullable=False)
    is_active_user = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    sent_messages = db.relationship("Message", backref="sender", foreign_keys="Message.sender_id")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_active(self):
        return self.is_active_user

    def can_access_department(self, dept):
        if self.role == "admin":
            return True
        if self.department == "Operations Control":
            return dept in DEPARTMENTS
        return self.department == dept

    def can_admin(self):
        return self.role == "admin"

    def can_access_lab(self):
        return self.role in ("admin", "security_analyst")

    def can_access_audit(self):
        return self.role in ("admin", "security_analyst")


class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    message_uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    recipient_department = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    hmac_tag = db.Column(db.String(64), nullable=False)
    timestamp_str = db.Column(db.String(40), nullable=True)
    integrity_valid = db.Column(db.Boolean, default=True)

    def compute_hmac(self):
        secret = current_app.config["HMAC_SECRET"].encode()
        canonical = f"{self.message_uuid}|{self.sender_id}|{self.recipient_department}|{self.timestamp_str}|{self.body}"
        return hmac.new(secret, canonical.encode(), hashlib.sha256).hexdigest()

    def verify_integrity(self):
        expected = self.compute_hmac()
        return hmac.compare_digest(expected, self.hmac_tag)

    @staticmethod
    def compute_hmac_for(message_uuid, sender_id, recipient_department, timestamp, body):
        ts = timestamp.isoformat()
        secret = current_app.config["HMAC_SECRET"].encode()
        canonical = f"{message_uuid}|{sender_id}|{recipient_department}|{ts}|{body}"
        return hmac.new(secret, canonical.encode(), hashlib.sha256).hexdigest(), ts


class AuditLog(db.Model):
    __tablename__ = "audit_logs"
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    event_type = db.Column(db.String(50), nullable=False)
    actor_id = db.Column(db.Integer, nullable=True)
    target = db.Column(db.String(200), nullable=True)
    outcome = db.Column(db.String(20), nullable=False)  # success, denied, failure
    detail = db.Column(db.Text, nullable=True)
    correlation_id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()))


class LabResult(db.Model):
    __tablename__ = "lab_results"
    id = db.Column(db.Integer, primary_key=True)
    run_id = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    scenario = db.Column(db.String(100), nullable=False)
    test_time = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    executed_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    mode = db.Column(db.String(20), nullable=False)  # baseline or protected
    expected_outcome = db.Column(db.Text, nullable=False)
    observed_outcome = db.Column(db.Text, nullable=False)
    passed = db.Column(db.Boolean, nullable=False)
    evidence = db.Column(db.Text, nullable=True)
    executor = db.relationship("User", backref="lab_results")

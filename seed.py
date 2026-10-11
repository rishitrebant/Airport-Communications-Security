"""Create demo users and sample messages for local demonstration."""
from datetime import datetime, timezone
from app import create_app, db
from app.models import User, Message

DEMO_USERS = [
    ("admin", "AdminPass123!", "admin", "Operations Control"),
    ("ops_controller", "OpsPass123!", "operator", "Operations Control"),
    ("gate_agent", "GatePass123!", "operator", "Gate Operations"),
    ("baggage_handler", "BagPass123!", "operator", "Baggage Handling"),
    ("maint_tech", "MaintPass123!", "operator", "Maintenance"),
    ("sec_analyst", "SecPass123!", "security_analyst", "Operations Control"),
]

SAMPLE_MESSAGES = [
    ("ops_controller", "Gate Operations", "Gate B7 Turnaround", "Flight AA1234 arrived Gate B7. Begin turnaround procedures. Estimated departure 14:30 UTC."),
    ("gate_agent", "Baggage Handling", "Priority Bags AA1234", "Three priority-tagged bags for connecting flight UA567 at Gate C12. Transfer deadline 13:45 UTC."),
    ("maint_tech", "Operations Control", "Runway 27L Inspection", "Scheduled FOD inspection of Runway 27L complete. No debris found. Runway operational."),
    ("baggage_handler", "Gate Operations", "Bag Count Confirmation", "All 142 bags loaded for DL890 at Gate A3. Weight manifest updated."),
]


def seed():
    app = create_app()
    with app.app_context():
        if User.query.first():
            print("Database already seeded.")
            return

        users = {}
        for username, pw, role, dept in DEMO_USERS:
            u = User(username=username, role=role, department=dept)
            u.set_password(pw)
            db.session.add(u)
            users[username] = u
        db.session.flush()

        for sender_name, dept, subject, body in SAMPLE_MESSAGES:
            sender = users[sender_name]
            import uuid
            msg_uuid = str(uuid.uuid4())
            now = datetime.now(timezone.utc)
            tag, ts = Message.compute_hmac_for(msg_uuid, sender.id, dept, now, body)
            msg = Message(
                message_uuid=msg_uuid, sender_id=sender.id,
                recipient_department=dept, subject=subject,
                body=body, timestamp=now, timestamp_str=ts, hmac_tag=tag,
            )
            db.session.add(msg)

        db.session.commit()
        print("Database seeded with demo users and messages.")
        print("Demo accounts:")
        for username, pw, role, dept in DEMO_USERS:
            print(f"  {username} / {pw}  (role={role}, dept={dept})")


if __name__ == "__main__":
    seed()

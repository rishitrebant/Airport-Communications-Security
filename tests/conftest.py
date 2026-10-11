import pytest
from app import create_app, db as _db
from app.models import User, Message, DEPARTMENTS
from config import TestConfig
from datetime import datetime, timezone
import uuid


@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    return _db


@pytest.fixture
def users(app, db):
    result = {}
    for username, pw, role, dept in [
        ("admin", "Admin123!", "admin", "Operations Control"),
        ("ops", "Ops123!", "operator", "Operations Control"),
        ("gate", "Gate123!", "operator", "Gate Operations"),
        ("baggage", "Bag123!", "operator", "Baggage Handling"),
        ("maint", "Maint123!", "operator", "Maintenance"),
        ("analyst", "Sec123!", "security_analyst", "Operations Control"),
    ]:
        u = User(username=username, role=role, department=dept)
        u.set_password(pw)
        db.session.add(u)
        result[username] = u
    db.session.commit()
    return result


def login(client, username, password):
    return client.post("/login", data={"username": username, "password": password}, follow_redirects=True)

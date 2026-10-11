import os
import secrets
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
    HMAC_SECRET = os.environ.get("HMAC_SECRET") or secrets.token_hex(32)
    default_db = (
    "sqlite:////tmp/airport_comms.db"
    if os.environ.get("VERCEL")
    else "sqlite:///airport_comms.db"
)

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or default_db
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEMO_MODE = os.environ.get("DEMO_MODE", "false").lower() == "true"
    WTF_CSRF_ENABLED = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    MAX_MESSAGE_BODY = 5000
    MAX_MESSAGE_SUBJECT = 200
    RATELIMIT_STORAGE_URI = "memory://"


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
    DEMO_MODE = True
    RATELIMIT_ENABLED = False
    SERVER_NAME = "localhost"

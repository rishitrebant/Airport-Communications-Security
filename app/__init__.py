from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
limiter = Limiter(key_func=get_remote_address, default_limits=[])


def create_app(config_class=None):
    app = Flask(__name__)

    if config_class:
        app.config.from_object(config_class)
    else:
        from config import Config
        app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    if not app.config.get("RATELIMIT_ENABLED") is False:
        limiter.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    from app.routes import auth_bp, main_bp, messages_bp, admin_bp, lab_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(messages_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(lab_bp)

    with app.app_context():
        db.create_all()

        if os.environ.get("SEED_DEMO_USERS", "false").lower() == "true":
            if not User.query.first():
                demo_users = [
                    ("admin", "AdminPass123!", "admin", "Operations Control"),
                    ("ops_controller", "OpsPass123!", "operator", "Operations Control"),
                    ("gate_agent", "GatePass123!", "operator", "Gate Operations"),
                    ("baggage_handler", "BagPass123!", "operator", "Baggage Handling"),
                    ("maint_tech", "MaintPass123!", "operator", "Maintenance"),
                    ("sec_analyst", "SecPass123!", "security_analyst", "Operations Control"),
                ]

                for username, password, role, department in demo_users:
                    user = User(
                        username=username,
                        role=role,
                        department=department,
                    )
                    user.set_password(password)
                    db.session.add(user)

                db.session.commit()
            

    return app

import os
import secrets

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    _default_key = os.environ.get("SECRET_KEY")
    SECRET_KEY = _default_key if _default_key else secrets.token_hex(32)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'bgys.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True

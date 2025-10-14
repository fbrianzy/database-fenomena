import secrets

from flask import (
    request, session
)

def ensure_csrf():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(32)
    return session["csrf_token"]

def require_csrf():
    form_tok = request.form.get("csrf_token", "")
    sess_tok = session.get("csrf_token", "")
    if not sess_tok or form_tok != sess_tok:
        raise RuntimeError("CSRF token invalid")

def is_logged_in() -> bool:
    return bool(session.get("is_admin", False))
import time
from flask import session

from app.config.rateLimit import *

def _login_rate_guard() -> int:
    now = int(time.time())
    lock_until = session.get("login_lock_until", 0)
    if lock_until and now < lock_until:
        return lock_until - now
    return 0

def _attempts_get() -> int:
    return int(session.get("login_attempts", 0))

def _attempts_set(v: int) -> None:
    session["login_attempts"] = max(0, int(v))

def _login_fail_register():
    now = int(time.time())
    attempts = _attempts_get() + 1
    _attempts_set(attempts)
    if attempts >= MAX_ATTEMPTS:
        session["login_lock_until"] = now + LOCK_WINDOW_SECONDS
        _attempts_set(0)

def _login_success_reset():
    for k in ("login_attempts", "login_lock_until"):
        session.pop(k, None)

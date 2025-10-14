import secrets
from werkzeug.security import check_password_hash
from flask import (
    flash, Blueprint, redirect, request, url_for, session, render_template
)

from app.config.logAdmin import *
from app.middlewares.rateLimit import (
    _login_fail_register, _login_rate_guard, _attempts_get, _login_success_reset
)
from app.middlewares.csrf import (
    require_csrf, ensure_csrf, is_logged_in 
)
from app.config.rateLimit import *
from app.routes.admin import bp

@bp.route("/login", methods=["GET", "POST"], endpoint="login")
def login():
    ensure_csrf()
    if is_logged_in():
        return redirect(url_for("admin.admin_home"))

    remaining = _login_rate_guard()
    attempts  = _attempts_get()
    attempts_left = max(0, MAX_ATTEMPTS - attempts)

    if request.method == "POST":
        if remaining > 0:
            flash(f"Akun sementara dikunci. Coba lagi dalam {remaining} detik.", "error")
            return redirect(url_for("admin.login"))

        try:
            require_csrf()
        except RuntimeError as e:
            flash(str(e), "error")
            return redirect(url_for("admin.login"))

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username and not password:
            flash("Username dan password wajib diisi.", "error")
            return redirect(url_for("admin.login"))
        if not username:
            flash("Username wajib diisi.", "error")
            return redirect(url_for("admin.login"))
        if not password:
            flash("Password wajib diisi.", "error")
            return redirect(url_for("admin.login"))

        if not ADMIN_PASSWORD_HASH:
            flash("ADMIN_PASSWORD_HASH belum di-set di environment.", "error")
            return redirect(url_for("admin.login"))

        if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
            session["is_admin"] = True
            _login_success_reset()
            session["csrf_token"] = secrets.token_urlsafe(32)
            dest = session.pop("next_after_login", None) or url_for("admin.admin_home")
            flash("Login berhasil.", "success")
            return redirect(dest)
        else:
            _login_fail_register()
            remaining = _login_rate_guard()
            attempts  = _attempts_get()
            attempts_left = max(0, MAX_ATTEMPTS - attempts)
            if remaining > 0:
                flash(f"Terlalu banyak percobaan. Terkunci {remaining} detik.", "error")
            else:
                flash(f"Username / password salah. Sisa percobaan: {attempts_left}", "error")
            return redirect(url_for("admin.login"))

    return render_template(
        "admin/admin_login.html",
        csrf_token=session.get("csrf_token"),
        lock_remaining=remaining,
        attempts_left=attempts_left,
        max_attempts=MAX_ATTEMPTS,
    )

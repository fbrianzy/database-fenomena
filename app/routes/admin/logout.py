from flask import (
    session, Blueprint, redirect, flash, url_for
)

from app.middlewares.csrf import *
from app.routes.admin import bp

@bp.route("/logout", methods=["POST"], endpoint="logout")
def admin_logout():
    try:
        require_csrf()
    except RuntimeError:
        pass
    session.clear()
    flash("Berhasil logout.", "success")
    return redirect(url_for("admin/admin.login"))
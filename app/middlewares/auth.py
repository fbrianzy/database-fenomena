from flask import (
    session, Blueprint, request, redirect, url_for
)

from app.middlewares.csrf import is_logged_in

bp = Blueprint("admin", __name__, url_prefix="/admin")

@bp.before_request
def gatekeeper():
    open_endpoints = {"admin.login", "admin.logout"}
    if request.endpoint in open_endpoints:
        return
    if not is_logged_in():
        session["next_after_login"] = request.full_path
        return redirect(url_for("admin.login"))
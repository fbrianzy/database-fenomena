from flask import (
    flash, redirect, url_for, Blueprint
)

from app.routes.admin import bp
from app.middlewares.github import *
from app.middlewares.csrf import *

@bp.route("/api/delete-file", methods=["POST"])
def api_delete_file():
    """Delete: hapus file CSV dari repo."""
    # pakai form post biasa atau JSON → dukung keduanya
    if request.is_json:
        require_json_csrf()
        path = (request.get_json(force=True) or {}).get("path")
    else:
        try:
            require_csrf()
        except RuntimeError as e:
            flash(str(e), "error")
            return redirect(url_for("admin.admin_home"))
        path = request.form.get("path")

    if not path:
        return {"ok": False, "error": "Missing path"}, 400

    _, sha = gh_get_file(path)
    if not sha:
        return {"ok": False, "error": "File tidak ditemukan"}, 404

    resp = gh_delete_file(path, sha, f"Admin: delete file {path}")
    if request.is_json:
        return {"ok": True, "commit": resp.get("commit", {}).get("sha")}
    else:
        flash(f"File dihapus: {path}", "success")
        return redirect(url_for("admin.admin_home"))

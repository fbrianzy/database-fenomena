from flask import (
    session, Blueprint, render_template, url_for
)

from app.middlewares.csrf import *
from app.services.githubApiHelpers import *
from app.config.folders import *
from app.routes.admin import bp

@bp.route("/")
def admin_home():
    ensure_csrf()
    def rows(folder):
        try:
            items = gh_list_dir(folder)
            out = []
            for it in items:
                if it.get("type") == "file" and it.get("name", "").lower().endswith(".csv"):
                    out.append({
                        "name": it["name"],
                        "path": it["path"],
                        "size": it.get("size", 0),
                        "html_url": it.get("html_url"),
                        "download_url": it.get("download_url"),
                    })
            return out
        except Exception:
            return []
    return render_template(
        "admin/admin_home.html",
        lu=rows(FOLDER_LU),
        pengeluaran=rows(FOLDER_PG),
        csrf_token=session.get("csrf_token")
    )
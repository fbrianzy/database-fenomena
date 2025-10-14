from flask import (
    Blueprint
)

from app.routes.admin import bp
from app.config.github import *
from app.config.folders import *
from app.middlewares.csrf import *

@bp.route("/diagnostics")
def admin_diagnostics():
    return {
        "GITHUB_TOKEN_set": bool(os.getenv("GITHUB_TOKEN")),
        "GH_OWNER": GH_OWNER,
        "GH_REPO": GH_REPO,
        "GH_BRANCH": GH_BRANCH,
        "FOLDER_LU": FOLDER_LU,
        "FOLDER_PG": FOLDER_PG,
        "is_admin": is_logged_in()
    }, 200

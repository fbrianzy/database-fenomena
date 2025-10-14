import os
from flask import (
    Blueprint, 
    jsonify
)

from app.routes.admin import bp

@bp.route("/envcheck", methods=["GET"])
def admin_envcheck():
    return jsonify({
        "GITHUB_TOKEN_set": bool(os.getenv("GITHUB_TOKEN")),
        "GITHUB_OWNER": os.getenv("GITHUB_OWNER"),
        "GITHUB_REPO": os.getenv("GITHUB_REPO"),
        "GITHUB_BRANCH": os.getenv("GITHUB_BRANCH"),
    }), 200

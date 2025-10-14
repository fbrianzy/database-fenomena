from flask import (
    session, abort, request, Blueprint
)

from app.routes.admin import bp

@bp.route("/clear-cache", methods=["POST"])
def clear_cache():
    sess_tok = session.get("csrf_token", "")
    hdr_tok = request.headers.get("X-CSRF-Token", "")
    if (not sess_tok) or (hdr_tok != sess_tok):
        abort(403, description="CSRF invalid (clear-cache)")

    global _csv_list_cache, _csv_data_cache, _latest_cache
    _csv_list_cache.clear()
    _csv_data_cache.clear()
    _latest_cache = {"ts": None, "value": None}
    return {"status": "success", "message": "Cache cleared"}, 200

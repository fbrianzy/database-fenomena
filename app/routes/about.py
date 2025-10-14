from app.services.cacheSystem import *
from flask import (
    render_template, Blueprint
)

bp = Blueprint("about", __name__, url_prefix="/about")

@bp.route("/")
def about():
    latest_dt_utc, latest_path = get_latest_update_datetime()
    latest_dt_id = to_jakarta(latest_dt_utc)
    latest_iso = latest_dt_id.isoformat()
    return render_template(
        "about.html",
        latest_sync_iso=latest_iso,
        latest_sync_path=latest_path
    )

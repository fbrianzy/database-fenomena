from flask import (
    Blueprint
)

from app.routes.admin import bp
from app.config.cache import (
    _csv_list_cache, _csv_data_cache, _latest_cache
)

@bp.route("/cache-status")
def cache_status():
    return {
        "csv_list_cache_entries": len(_csv_list_cache),
        "csv_data_cache_entries": len(_csv_data_cache),
        "latest_cache_set": _latest_cache["ts"] is not None
    }, 200

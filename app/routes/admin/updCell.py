from flask import (
    Blueprint
)

from app.middlewares.github import *
from app.routes.admin import bp

@bp.route("/api/update-cell", methods=["POST"])
def api_update_cell():
    """Update: edit 1 sel, commit balik ke GitHub."""
    require_json_csrf()
    payload = request.get_json(force=True) or {}
    path      = payload.get("path")
    row_index = int(payload.get("row_index", -1))
    column    = payload.get("column")
    new_value = payload.get("new_value", "")

    if not path or column is None or row_index < 0:
        return {"ok": False, "error": "Bad request"}, 400

    # baca CSV asli (tanpa __row_index__)
    headers, rows = read_csv_headers_rows_from_raw(path)
    if not headers:
        return {"ok": False, "error": "CSV kosong / tidak ditemukan"}, 404
    if column not in headers:
        return {"ok": False, "error": "Kolom tidak dikenal"}, 400
    if row_index >= len(rows):
        return {"ok": False, "error": "Row index out of range"}, 400

    col_idx = headers.index(column)
    rows[row_index][col_idx] = str(new_value).strip()

    out_bytes = write_csv_bytes(headers, rows)
    _, sha = gh_get_file(path)
    if not sha:
        return {"ok": False, "error": "File hilang di repo"}, 404
    resp = gh_put_file(path, out_bytes, f"Admin: edit cell {path} r={row_index} c={column}", sha=sha)
    return {"ok": True, "commit": resp.get("commit", {}).get("sha")}

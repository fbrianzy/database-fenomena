from flask import Blueprint

from app.middlewares.github import *
from app.routes.admin import bp

@bp.route("/api/update-row")
def api_update_row():
    """Update satu baris (full row replace) lalu commit."""
    require_json_csrf()
    p = request.get_json(force=True) or {}
    path      = p.get("path")
    row_index = int(p.get("row_index", -1))
    row_data  = p.get("row_data")  # dict: {header: value}
    message   = p.get("message") or f"Admin: update row {path} r={row_index}"

    if not path or row_index < 0 or not isinstance(row_data, dict):
        return {"ok": False, "error": "Bad request"}, 400

    headers, rows = read_csv_headers_rows_from_raw(path)
    if not headers:
        return {"ok": False, "error": "CSV kosong / tidak ditemukan"}, 404
    if row_index >= len(rows):
        return {"ok": False, "error": "Row index out of range"}, 400

    # susun row baru sesuai urutan headers
    new_row = []
    for h in headers:
        val = row_data.get(h, "")
        new_row.append(str(val))

    rows[row_index] = new_row

    out = write_csv_bytes(headers, rows)
    _, sha = gh_get_file(path)
    if not sha:
        return {"ok": False, "error": "File hilang di repo"}, 404

    resp = gh_put_file(path, out, message, sha=sha)
    return {"ok": True, "commit": resp.get("commit", {}).get("sha")}

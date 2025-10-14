from flask import (
    Blueprint, abort, session, render_template
)

from app.middlewares.csrf import *
from app.middlewares.github import *
from app.routes.admin import bp

@bp.route("/table")
def admin_table():
    """Read: tampilkan CSV sebagai tabel editable."""
    ensure_csrf()
    path = request.args.get("path")
    if not path:
        abort(400, description="Missing ?path")

    # Ambil headers & rows via RAW
    headers, rows = read_csv_headers_rows_from_raw(path)

    # sisipkan __row_index__ untuk UI
    if headers and (len(headers) == 0 or headers[0] != "__row_index__"):
        headers = ["__row_index__"] + headers
        rows = [[str(i)] + r for i, r in enumerate(rows)]

    return render_template(
        "admin/admin_table.html",
        path=path,
        headers=headers,
        rows=rows,
        csrf_token=session.get("csrf_token"),
    )

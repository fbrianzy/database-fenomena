from flask import Blueprint, render_template, request, redirect, url_for, jsonify, abort, session
import os
from datetime import datetime

from config import GITHUB_DATA_DIR, ADMIN_SECRET
from github_client import (
    list_csv_files, read_csv_from_raw, write_csv_bytes, 
    get_file_sha, upload_new_file, update_file, delete_file
)

bp = Blueprint("admin_github", __name__, url_prefix="/admin")

# --------- AUTH SEDERHANA (opsional) ---------
def require_admin():
    token = session.get("admin_token")
    if token != ADMIN_SECRET:
        abort(403)

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("secret") == ADMIN_SECRET:
            session["admin_token"] = ADMIN_SECRET
            return redirect(url_for("admin_github.dashboard"))
        return render_template("admin_login.html", error="Secret salah")
    return render_template("admin_login.html")

# --------- DASHBOARD & LIST FILE ----------
@bp.route("/")
def dashboard():
    require_admin()
    folder = request.args.get("folder", GITHUB_DATA_DIR)
    files = list_csv_files(folder)
    return render_template("admin_dashboard.html", files=files, folder=folder)

# --------- CREATE: UPLOAD CSV -> COMMIT ---------
@bp.route("/upload", methods=["POST"])
def upload():
    require_admin()
    file = request.files.get("csv")
    subdir = request.form.get("subdir", "").strip().strip("/")
    commit_message = request.form.get("message") or f"Upload CSV via Admin {datetime.now():%Y-%m-%d %H:%M:%S}"

    if not file or not file.filename.lower().endswith(".csv"):
        return redirect(url_for("admin_github.dashboard"))

    rel_dir = f"{GITHUB_DATA_DIR}/{subdir}" if subdir else GITHUB_DATA_DIR
    rel_path = f"{rel_dir}/{file.filename}"

    content = file.read()
    sha = get_file_sha(rel_path)

    if sha:
        # update file existing
        update_file(rel_path, content, sha, f"[UPDATE] {commit_message}")
    else:
        # create new
        upload_new_file(rel_path, content, f"[CREATE] {commit_message}")

    return redirect(url_for("admin_github.view_table", path=rel_path))

# --------- READ: VIEW TABEL ----------
@bp.route("/view")
def view_table():
    require_admin()
    path = request.args.get("path")
    if not path:
        abort(400, "missing path")
    headers, rows = read_csv_from_raw(path)

    # inject index kolom untuk identifikasi row
    if headers and (len(headers) == 0 or headers[0] != "__row_index__"):
        headers = ["__row_index__"] + headers
        rows = [[str(i)] + r for i, r in enumerate(rows)]

    return render_template("admin_table.html", path=path, headers=headers, rows=rows)

# --------- UPDATE: EDIT SEL INLINE ----------
@bp.route("/api/update-cell", methods=["POST"])
def api_update_cell():
    require_admin()
    data = request.get_json(force=True)
    path = data["path"]
    row_index = int(data["row_index"])
    column = data["column"]
    new_value = data["new_value"]

    headers, rows = read_csv_from_raw(path)
    if not headers:
        return jsonify({"ok": False, "error": "CSV empty"}), 400

    if column not in headers:
        return jsonify({"ok": False, "error": "Unknown column"}), 400

    # apply change
    col_idx = headers.index(column)
    if row_index < 0 or row_index >= len(rows):
        return jsonify({"ok": False, "error": "Row index out of range"}), 400

    rows[row_index][col_idx] = new_value

    # write back
    content = write_csv_bytes(headers, rows)
    sha = get_file_sha(path)
    if not sha:
        return jsonify({"ok": False, "error": "File not found in repo"}), 404

    resp = update_file(path, content, sha, f"[EDIT] {path} row={row_index} col={column}")
    return jsonify({"ok": True, "commit": resp.get("commit", {}).get("sha")})

# --------- DELETE: HAPUS BARIS ----------
@bp.route("/api/delete-row", methods=["POST"])
def api_delete_row():
    require_admin()
    data = request.get_json(force=True)
    path = data["path"]
    row_index = int(data["row_index"])

    headers, rows = read_csv_from_raw(path)
    if not headers:
        return jsonify({"ok": False, "error": "CSV empty"}), 400

    if row_index < 0 or row_index >= len(rows):
        return jsonify({"ok": False, "error": "Row index out of range"}), 400

    del rows[row_index]

    content = write_csv_bytes(headers, rows)
    sha = get_file_sha(path)
    if not sha:
        return jsonify({"ok": False, "error": "File not found in repo"}), 404

    resp = update_file(path, content, sha, f"[DELETE-ROW] {path} row={row_index}")
    return jsonify({"ok": True, "commit": resp.get("commit", {}).get("sha")})

# --------- DELETE: HAPUS FILE CSV DI REPO ----------
@bp.route("/api/delete-file", methods=["POST"])
def api_delete_file():
    require_admin()
    data = request.get_json(force=True)
    path = data["path"]

    sha = get_file_sha(path)
    if not sha:
        return jsonify({"ok": False, "error": "File not found"}), 404

    resp = delete_file(path, sha, f"[DELETE-FILE] {path}")
    return jsonify({"ok": True, "commit": resp.get("commit", {}).get("sha")})

import pandas as pd
import os
import io
from requests import HTTPError
from werkzeug.utils import secure_filename
from flask import (
    request, flash, redirect, url_for, Blueprint, render_template
)

from app.middlewares.csrf import *
from app.utils.validators import (
    _ensure_github_ready
)
from app.config.uplCsv import *
from app.utils.validators import *
from app.services.githubApiHelpers import *
from app.services.cleaner import *
from app.routes.admin import bp

@bp.route("/upload", methods=["GET", "POST"])
def admin_upload():
    ensure_csrf()
    if request.method == "GET":
        return render_template(
            "admin_upload.html",
            jenis_data_options=[("lapangan_usaha", "Lapangan Usaha"),
                                ("pengeluaran", "Pengeluaran")],
            csrf_token=session.get("csrf_token")
        )

    try:
        require_csrf()
    except RuntimeError as e:
        flash(str(e), "error")
        return redirect(url_for("admin.admin_upload"))

    try:
        _ensure_github_ready()
    except RuntimeError as e:
        flash(str(e), "error")
        return redirect(url_for("admin.admin_home"))

    jenis_data = request.form.get("jenis_data", "lapangan_usaha")
    commit_msg = request.form.get("message") or "Admin: upload & clean CSV"
    file = request.files.get("file")
    if not file or file.filename == "":
        flash("Pilih file CSV dulu.", "error")
        return redirect(url_for("admin.admin_upload"))

    fname = secure_filename(file.filename)
    ext = os.path.splitext(fname)[1].lower()
    if ext not in ALLOWED_EXT:
        flash("Hanya file .csv yang diizinkan.", "error")
        return redirect(url_for("admin.admin_upload"))

    file.seek(0, os.SEEK_END)
    size_mb = file.tell() / (1024 * 1024)
    file.seek(0)
    if size_mb > MAX_UPLOAD_MB:
        flash(f"Ukuran maksimum {MAX_UPLOAD_MB} MB.", "error")
        return redirect(url_for("admin.admin_upload"))

    raw = file.read()
    try:
        df = pd.read_csv(io.BytesIO(raw))
    except Exception as e:
        flash(f"CSV tidak valid: {e}", "error")
        return redirect(url_for("admin.admin_upload"))

    ok, missing = validate_csv(df)
    if not ok:
        flash("Kolom wajib hilang: " + ", ".join(missing), "error")
        return redirect(url_for("admin.admin_upload"))

    df_clean = run_fenomena_cleaner(df)

    buf = io.StringIO()
    df_clean.to_csv(buf, index=False)
    out_bytes = buf.getvalue().encode("utf-8")

    target_folder = choose_target_folder(jenis_data)
    dest_path = f"{target_folder}/{fname}"

    try:
        _, sha = gh_get_file(dest_path)
    except HTTPError as e:
        if e.response is None or e.response.status_code != 404:
            raise
        sha = None

    try:
        gh_put_file(dest_path, out_bytes, commit_msg, sha=sha)
    except HTTPError as e:
        if e.response is not None and e.response.status_code in (401, 403):
            flash("GitHub token/permission kurang (butuh scope repo / Contents: Read & Write).", "error")
            return redirect(url_for("admin.admin_upload"))
        raise

    flash(("Updated: " if sha else "Created: ") + dest_path, "success")
    return redirect(url_for("admin.admin_home"))

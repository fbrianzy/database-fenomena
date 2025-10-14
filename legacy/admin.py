import os
import io
import base64
import secrets
import time
import pandas as pd
import requests
from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash, session, abort
)
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from requests import HTTPError
import csv
from urllib.parse import quote

# =======================
# KONFIG: GITHUB & TARGET
# =======================
GH_OWNER  = os.getenv("GITHUB_OWNER",  "fbrianzy")
GH_REPO   = os.getenv("GITHUB_REPO",   "database-fenomena")
GH_BRANCH = os.getenv("GITHUB_BRANCH", "main")

FOLDER_LU = "data/lapangan_usaha"
FOLDER_PG = "data/pengeluaran"

ALLOWED_EXT    = {".csv"}
MAX_UPLOAD_MB  = 8

# =======================
# KONFIG: LOGIN ADMIN
# =======================
ADMIN_USERNAME      = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH")  # isi hash di production

# Rate limit
MAX_ATTEMPTS = 3
LOCK_WINDOW_SECONDS = 60  # 1 menit

admin = Blueprint("admin", __name__, url_prefix="/admin")

# =======================
# AUTH & CSRF
# =======================
def ensure_csrf():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(32)
    return session["csrf_token"]

def require_csrf():
    form_tok = request.form.get("csrf_token", "")
    sess_tok = session.get("csrf_token", "")
    if not sess_tok or form_tok != sess_tok:
        raise RuntimeError("CSRF token invalid")

def is_logged_in() -> bool:
    return bool(session.get("is_admin", False))

@admin.before_request
def gatekeeper():
    open_endpoints = {"admin.login", "admin.logout"}
    if request.endpoint in open_endpoints:
        return
    if not is_logged_in():
        session["next_after_login"] = request.full_path
        return redirect(url_for("admin.login"))
    
# === Tambahkan helper RAW URL & delete file ===
def gh_raw_url(path: str) -> str:
    return f"https://raw.githubusercontent.com/{GH_OWNER}/{GH_REPO}/{GH_BRANCH}/{path}"

def gh_delete_file(path: str, sha: str, message: str = None):
    url = gh_contents_url(path)
    payload = {
        "message": message or f"Admin: delete {path}",
        "sha": sha,
        "branch": GH_BRANCH,
    }
    r = requests.delete(url, headers=gh_headers(), json=payload, timeout=30)
    r.raise_for_status()
    return r.json()

# === Helper baca CSV via RAW (hemat rate-limit) ===
def read_csv_headers_rows_from_raw(path: str):
    url = gh_raw_url(path)
    r = requests.get(url, timeout=30)
    if r.status_code == 404:
        return [], []
    r.raise_for_status()
    text = r.text
    f = io.StringIO(text, newline="")
    reader = csv.reader(f)
    rows = list(reader)
    if not rows:
        return [], []
    headers = rows[0]
    data = rows[1:]
    return headers, data

# === Helper tulis CSV bytes (untuk update & delete baris) ===
def write_csv_bytes(headers, rows):
    buf = io.StringIO(newline="")
    w = csv.writer(buf)
    w.writerow(headers)
    for r in rows:
        w.writerow(r)
    return buf.getvalue().encode("utf-8")

# === Guard CSRF untuk JSON request (X-CSRF-Token header) ===
def require_json_csrf():
    sess_tok = session.get("csrf_token", "")
    hdr_tok = request.headers.get("X-CSRF-Token", "")
    if (not sess_tok) or (hdr_tok != sess_tok):
        abort(403, description="CSRF invalid (JSON)")

# =======================
# RATE LIMIT HELPERS
# =======================
def _login_rate_guard() -> int:
    now = int(time.time())
    lock_until = session.get("login_lock_until", 0)
    if lock_until and now < lock_until:
        return lock_until - now
    return 0

def _attempts_get() -> int:
    return int(session.get("login_attempts", 0))

def _attempts_set(v: int) -> None:
    session["login_attempts"] = max(0, int(v))

def _login_fail_register():
    now = int(time.time())
    attempts = _attempts_get() + 1
    _attempts_set(attempts)
    if attempts >= MAX_ATTEMPTS:
        session["login_lock_until"] = now + LOCK_WINDOW_SECONDS
        _attempts_set(0)

def _login_success_reset():
    for k in ("login_attempts", "login_lock_until"):
        session.pop(k, None)

# =======================
# GITHUB CONTENTS API
# =======================
def gh_headers():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN belum di-set")
    return {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
    }

def gh_contents_url(path: str) -> str:
    return f"https://api.github.com/repos/{GH_OWNER}/{GH_REPO}/contents/{path}"

def gh_list_dir(path: str):
    r = requests.get(gh_contents_url(path), headers=gh_headers(), params={"ref": GH_BRANCH}, timeout=20)
    r.raise_for_status()
    return r.json()

def gh_get_file(path: str):
    r = requests.get(gh_contents_url(path), headers=gh_headers(), params={"ref": GH_BRANCH}, timeout=20)
    if r.status_code == 404:
        return None, None
    r.raise_for_status()
    js = r.json()
    content = base64.b64decode(js.get("content", b""))
    sha = js.get("sha")
    return content, sha

def gh_put_file(path: str, content_bytes: bytes, message: str, sha: str | None):
    payload = {
        "message": message or f"Admin: write {path}",
        "content": base64.b64encode(content_bytes).decode(),
        "branch": GH_BRANCH,
    }
    if sha:
        payload["sha"] = sha
    r = requests.put(gh_contents_url(path), headers=gh_headers(), json=payload, timeout=30)
    r.raise_for_status()
    return r.json()

# =======================
# FENOMENACLEANER (opsional)
# =======================
try:
    from FenomenaCleaner import clean_tanggal, clean_urls
except Exception:
    import re
    def clean_tanggal(text):
        text = str(text) if text is not None else ""
        dates = re.findall(r'\b\d{1,2}\s+[A-Za-zÀ-ÿ]+', text)
        return '; '.join([d.title() for d in dates])
    def clean_urls(text):
        text = str(text) if text is not None else ""
        urls = re.findall(r'https?://[^\s,;"]+', text)
        return ', '.join(urls)

def run_fenomena_cleaner(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "Tanggal" in df.columns:
        df["Tanggal"] = df["Tanggal"].apply(clean_tanggal)
    if "Url Berita" in df.columns:
        df["Url Berita"] = df["Url Berita"].apply(clean_urls)
    for col in [c for c in ["Kategori", "Ringkasan Fenomena", "Sentiment", "bulan"] if c in df.columns]:
        df[col] = df[col].astype(str).str.strip()
    if "bulan" in df.columns:
        df["bulan"] = df["bulan"].astype(str).str.title()
    return df

# =======================
# VALIDASI CSV
# =======================
def validate_csv(df: pd.DataFrame):
    cols_lower = {c.lower(): c for c in df.columns}
    missing = []
    if not any(k in cols_lower for k in ("ringkasan fenomena", "ringkasan")):
        missing.append("Ringkasan Fenomena/Ringkasan")
    if not any(k in cols_lower for k in ("kategori", "category")):
        missing.append("Kategori/Category")
    return (len(missing) == 0), missing

def choose_target_folder(jenis_data: str) -> str:
    jenis_data = (jenis_data or "").lower()
    if jenis_data == "lapangan_usaha": return FOLDER_LU
    if jenis_data == "pengeluaran":    return FOLDER_PG
    # default ke lapangan_usaha
    return FOLDER_LU

def _ensure_github_ready():
    miss = [k for k in ("GITHUB_TOKEN", "GITHUB_OWNER", "GITHUB_REPO", "GITHUB_BRANCH") if not os.getenv(k)]
    if miss:
        raise RuntimeError("Env belum lengkap: " + ", ".join(miss))

# =======================
# ROUTES: AUTH
# =======================
@admin.route("/login", methods=["GET", "POST"], endpoint="login")
def login():
    ensure_csrf()
    if is_logged_in():
        return redirect(url_for("admin.admin_home"))

    remaining = _login_rate_guard()
    attempts  = _attempts_get()
    attempts_left = max(0, MAX_ATTEMPTS - attempts)

    if request.method == "POST":
        if remaining > 0:
            flash(f"Akun sementara dikunci. Coba lagi dalam {remaining} detik.", "error")
            return redirect(url_for("admin.login"))

        try:
            require_csrf()
        except RuntimeError as e:
            flash(str(e), "error")
            return redirect(url_for("admin.login"))

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username and not password:
            flash("Username dan password wajib diisi.", "error")
            return redirect(url_for("admin.login"))
        if not username:
            flash("Username wajib diisi.", "error")
            return redirect(url_for("admin.login"))
        if not password:
            flash("Password wajib diisi.", "error")
            return redirect(url_for("admin.login"))

        if not ADMIN_PASSWORD_HASH:
            flash("ADMIN_PASSWORD_HASH belum di-set di environment.", "error")
            return redirect(url_for("admin.login"))

        if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
            session["is_admin"] = True
            _login_success_reset()
            session["csrf_token"] = secrets.token_urlsafe(32)
            dest = session.pop("next_after_login", None) or url_for("admin.admin_home")
            flash("Login berhasil.", "success")
            return redirect(dest)
        else:
            _login_fail_register()
            remaining = _login_rate_guard()
            attempts  = _attempts_get()
            attempts_left = max(0, MAX_ATTEMPTS - attempts)
            if remaining > 0:
                flash(f"Terlalu banyak percobaan. Terkunci {remaining} detik.", "error")
            else:
                flash(f"Username / password salah. Sisa percobaan: {attempts_left}", "error")
            return redirect(url_for("admin.login"))

    return render_template(
        "admin_login.html",
        csrf_token=session.get("csrf_token"),
        lock_remaining=remaining,
        attempts_left=attempts_left,
        max_attempts=MAX_ATTEMPTS,
    )

@admin.route("/logout", methods=["POST"], endpoint="logout")
def admin_logout():
    try:
        require_csrf()
    except RuntimeError:
        pass
    session.clear()
    flash("Berhasil logout.", "success")
    return redirect(url_for("admin.login"))

# =======================
# ROUTES: ADMIN PAGES
# =======================
@admin.route("/")
def admin_home():
    ensure_csrf()
    def rows(folder):
        try:
            items = gh_list_dir(folder)
            out = []
            for it in items:
                if it.get("type") == "file" and it.get("name", "").lower().endswith(".csv"):
                    out.append({
                        "name": it["name"],
                        "path": it["path"],
                        "size": it.get("size", 0),
                        "html_url": it.get("html_url"),
                        "download_url": it.get("download_url"),
                    })
            return out
        except Exception:
            return []
    return render_template(
        "admin_home.html",
        lu=rows(FOLDER_LU),
        pengeluaran=rows(FOLDER_PG),
        csrf_token=session.get("csrf_token")
    )

@admin.route("/upload", methods=["GET", "POST"])
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

@admin.route("/diagnostics")
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

# =======================
# ROUTES: READ/UPDATE/DELETE CSV
# =======================

@admin.route("/table")
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
        "admin_table.html",
        path=path,
        headers=headers,
        rows=rows,
        csrf_token=session.get("csrf_token"),
    )

@admin.route("/api/update-cell", methods=["POST"])
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

@admin.route("/api/delete-row", methods=["POST"])
def api_delete_row():
    """Delete: hapus 1 baris kemudian commit."""
    require_json_csrf()
    payload = request.get_json(force=True) or {}
    path      = payload.get("path")
    row_index = int(payload.get("row_index", -1))

    if not path or row_index < 0:
        return {"ok": False, "error": "Bad request"}, 400

    headers, rows = read_csv_headers_rows_from_raw(path)
    if not headers:
        return {"ok": False, "error": "CSV kosong / tidak ditemukan"}, 404
    if row_index >= len(rows):
        return {"ok": False, "error": "Row index out of range"}, 400

    del rows[row_index]

    out_bytes = write_csv_bytes(headers, rows)
    _, sha = gh_get_file(path)
    if not sha:
        return {"ok": False, "error": "File hilang di repo"}, 404
    resp = gh_put_file(path, out_bytes, f"Admin: delete row {path} r={row_index}", sha=sha)
    return {"ok": True, "commit": resp.get("commit", {}).get("sha")}

@admin.route("/api/delete-file", methods=["POST"])
def api_delete_file():
    """Delete: hapus file CSV dari repo."""
    # pakai form post biasa atau JSON → dukung keduanya
    if request.is_json:
        require_json_csrf()
        path = (request.get_json(force=True) or {}).get("path")
    else:
        try:
            require_csrf()
        except RuntimeError as e:
            flash(str(e), "error")
            return redirect(url_for("admin.admin_home"))
        path = request.form.get("path")

    if not path:
        return {"ok": False, "error": "Missing path"}, 400

    _, sha = gh_get_file(path)
    if not sha:
        return {"ok": False, "error": "File tidak ditemukan"}, 404

    resp = gh_delete_file(path, sha, f"Admin: delete file {path}")
    if request.is_json:
        return {"ok": True, "commit": resp.get("commit", {}).get("sha")}
    else:
        flash(f"File dihapus: {path}", "success")
        return redirect(url_for("admin.admin_home"))

@admin.route("/api/update-row", methods=["POST"])
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

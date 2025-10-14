import csv
import io
from flask import (
    session, request, abort
)

from app.config.github import *
from app.services.githubApiHelpers import *

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

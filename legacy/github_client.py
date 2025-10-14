import base64
import csv
import io
import requests
from typing import List, Tuple, Optional

from config import GITHUB_TOKEN, GITHUB_REPO, GITHUB_BRANCH

API_BASE = "https://api.github.com"
RAW_BASE = "https://raw.githubusercontent.com"

session = requests.Session()
session.headers.update({
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
})

def repo_owner_name() -> Tuple[str, str]:
    owner, name = GITHUB_REPO.split("/", 1)
    return owner, name

def list_csv_files(path: str) -> List[dict]:
    """List isi folder di repo (GitHub API), filter .csv"""
    owner, name = repo_owner_name()
    url = f"{API_BASE}/repos/{owner}/{name}/contents/{path}?ref={GITHUB_BRANCH}"
    r = session.get(url)
    r.raise_for_status()
    items = r.json()
    if isinstance(items, dict) and items.get("type") == "file":
        items = [items]
    return [i for i in items if i.get("type") == "file" and i["name"].lower().endswith(".csv")]

def raw_csv_url(path: str) -> str:
    owner, name = repo_owner_name()
    return f"{RAW_BASE}/{owner}/{name}/{GITHUB_BRANCH}/{path}"

def get_file_sha(path: str) -> Optional[str]:
    owner, name = repo_owner_name()
    url = f"{API_BASE}/repos/{owner}/{name}/contents/{path}"
    r = session.get(url, params={"ref": GITHUB_BRANCH})
    if r.status_code == 404:
        return None
    r.raise_for_status()
    return r.json().get("sha")

def upload_new_file(path: str, content_bytes: bytes, message: str) -> dict:
    """Create new file (fails if exists)."""
    owner, name = repo_owner_name()
    url = f"{API_BASE}/repos/{owner}/{name}/contents/{path}"
    data = {
        "message": message,
        "content": base64.b64encode(content_bytes).decode(),
        "branch": GITHUB_BRANCH,
    }
    r = session.put(url, json=data)
    r.raise_for_status()
    return r.json()

def update_file(path: str, content_bytes: bytes, sha: str, message: str) -> dict:
    """Update existing file by sha."""
    owner, name = repo_owner_name()
    url = f"{API_BASE}/repos/{owner}/{name}/contents/{path}"
    data = {
        "message": message,
        "content": base64.b64encode(content_bytes).decode(),
        "sha": sha,
        "branch": GITHUB_BRANCH,
    }
    r = session.put(url, json=data)
    r.raise_for_status()
    return r.json()

def delete_file(path: str, sha: str, message: str) -> dict:
    owner, name = repo_owner_name()
    url = f"{API_BASE}/repos/{owner}/{name}/contents/{path}"
    data = {"message": message, "sha": sha, "branch": GITHUB_BRANCH}
    r = session.delete(url, json=data)
    r.raise_for_status()
    return r.json()

def read_csv_from_raw(path: str) -> Tuple[List[str], List[List[str]]]:
    """Load CSV via RAW (hemat rate-limit). Return (headers, rows as list of str)."""
    url = raw_csv_url(path)
    r = requests.get(url, timeout=30)
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

def write_csv_bytes(headers: List[str], rows: List[List[str]]) -> bytes:
    buf = io.StringIO(newline="")
    writer = csv.writer(buf)
    writer.writerow(headers)
    for row in rows:
        writer.writerow(row)
    return buf.getvalue().encode("utf-8")

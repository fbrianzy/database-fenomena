import requests
from app.config.github import *
import datetime
import base64

def _github_headers():
    headers = {"Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return headers

def _github_get(url, params=None):
    headers = _github_headers()
    r = requests.get(url, headers=headers, params=params, timeout=20)

    # Rate limit info (log)
    remaining = r.headers.get("X-RateLimit-Remaining")
    limit = r.headers.get("X-RateLimit-Limit")
    if remaining and limit:
        print(f"GitHub API Rate Limit: {remaining}/{limit}")

    # Rate limit handling
    if r.status_code == 403 and "rate limit" in r.text.lower():
        reset_time = r.headers.get("X-RateLimit-Reset")
        if reset_time:
            reset_dt = datetime.fromtimestamp(int(reset_time))
            print(f"Rate limit exceeded! Resets at {reset_dt}")
        raise Exception("GitHub API rate limit exceeded")

    r.raise_for_status()
    return r.json()

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
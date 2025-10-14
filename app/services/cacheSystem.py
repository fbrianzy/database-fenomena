from datetime import datetime, timezone, timedelta
from app.services.githubApiHelpers import _github_get
from app.config.cache import _latest_cache

def get_latest_update_datetime():
    """
    Ambil waktu commit terbaru (UTC) dari 2 direktori data (tanpa komoditas).
    Return: (dt_utc: datetime, source_path: str)
    """
    now = datetime.now(timezone.utc)
    if _latest_cache["ts"] and (now - _latest_cache["ts"]).total_seconds() < 180:
        return _latest_cache["value"]

    owner = "fbrianzy"
    repo = "database-fenomena"
    branch = "main"
    paths = [
        "data/lapangan_usaha",
        "data/pengeluaran",
    ]

    latest_dt = None
    latest_path = None
    for p in paths:
        try:
            url = f"https://api.github.com/repos/{owner}/{repo}/commits"
            data = _github_get(url, params={"path": p, "sha": branch, "per_page": 1})
            if not data:
                continue
            commit_dt = data[0]["commit"]["committer"]["date"]
            dt_utc = datetime.fromisoformat(commit_dt.replace("Z", "+00:00"))
            if (latest_dt is None) or (dt_utc > latest_dt):
                latest_dt = dt_utc
                latest_path = p
        except Exception as e:
            print(f"Error getting commit for {p}: {e}")
            continue

    if latest_dt is None:
        latest_dt = now
        latest_path = "N/A"

    _latest_cache["ts"] = now
    _latest_cache["value"] = (latest_dt, latest_path)
    return _latest_cache["value"]

def to_jakarta(dt_utc: datetime) -> datetime:
    return dt_utc.astimezone(timezone(timedelta(hours=7)))

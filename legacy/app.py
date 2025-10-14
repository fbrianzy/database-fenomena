from dotenv import load_dotenv
load_dotenv()

import requests
from urllib.parse import urlparse
from flask import Flask, render_template, request, jsonify, session, abort
import pandas as pd
import os, secrets
import hashlib
from datetime import datetime, timezone, timedelta

# Error handlers (jika ada modulnya)
try:
    from error_handlers import register_error_handlers
except Exception:
    def register_error_handlers(app):  # fallback no-op
        return

app = Flask(__name__)

# WAJIB: secret key untuk session/flash
app.secret_key = os.getenv("FLASK_SECRET_KEY") or secrets.token_hex(32)
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = False  # set True kalau sudah di HTTPS

# Daftarkan error handlers
register_error_handlers(app)

# =======================
# IMPORT & REGISTER BLUEPRINT ADMIN
# =======================
from admin import admin
app.register_blueprint(admin)

# ==== DATA SOURCES (RAW GitHub) — tanpa komoditas ====
DATA_LU_DIR = "https://raw.githubusercontent.com/fbrianzy/database-fenomena/main/data/lapangan_usaha/"
DATA_PENGELUARAN_DIR = "https://raw.githubusercontent.com/fbrianzy/database-fenomena/main/data/pengeluaran/"

# Token GitHub (opsional untuk API)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# =======================
# GITHUB API HELPERS
# =======================
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

# =======================
# CACHING SYSTEM
# =======================
_latest_cache = {"ts": None, "value": None}
_csv_list_cache = {}
_csv_data_cache = {}
_CACHE_TTL_SECONDS = 10  
_DATA_CACHE_TTL_SECONDS = 10  # 10 menit (data CSV)

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

# =======================
# SAMPLE DATA
# =======================
def create_sample_data():
    import random
    months = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni']
    categories = ['Ekonomi', 'Sosial', 'Pendidikan', 'Kesehatan', 'Infrastruktur']
    sentiments = ['Positif', 'Negatif', 'Kosong']
    sample_data = []
    for i in range(50):
        sample_data.append({
            'bulan': random.choice(months),
            'Kategori': random.choice(categories),
            'Sentiment': random.choice(sentiments),
            'Ringkasan Fenomena': f'Sample fenomena {i+1} untuk testing aplikasi',
            'jenis_data': 'Sample Data'
        })
    return pd.DataFrame(sample_data)

# === Month-Year parsing utilities ===
BULAN_ID = {
    "januari": "Januari", "februari": "Februari", "maret": "Maret", "april": "April",
    "mei": "Mei", "juni": "Juni", "juli": "Juli", "agustus": "Agustus",
    "september": "September", "oktober": "Oktober", "november": "November", "desember": "Desember"
}

MONTH_ORDER = ['Januari','Februari','Maret','April','Mei','Juni',
            'Juli','Agustus','September','Oktober','November','Desember']
MONTH_INDEX = {m: i+1 for i, m in enumerate(MONTH_ORDER)}

def parse_bulan_tahun_from_filename(filename: str):
    base = filename.rsplit("/", 1)[-1].replace(".csv", "")
    parts = base.split("_")
    bulan = None
    tahun = None
    for part in parts:
        p = part.strip().lower()
        if p in BULAN_ID and bulan is None:
            bulan = BULAN_ID[p]
        elif p.isdigit() and len(p) == 4:
            tahun = p
    return bulan or base.title(), tahun

def compute_home_mom_stats(df_all):
    """Hitung MoM total fenomena dan perubahan % sentimen positif (p.p.)"""
    from math import isfinite
    if df_all is None or df_all.empty:
        return {
            "fenomena_total_now": 0,
            "fenomena_mom_pct": None,          # None kalau tidak ada prev
            "pos_pct_now": 0.0,
            "pos_pct_prev": 0.0,
            "pos_delta_pp": 0.0,
            "label_now": None,
            "label_prev": None
        }

    # pakai filter valid yang sama seperti di halaman Trend
    df = filter_empty_data_for_trend(df_all, jenis_data="all")

    if ("tahun" not in df.columns) or ("bulan" not in df.columns):
        # fallback: tidak ada dimensi waktu → anggap tidak ada pembanding
        total_now = len(df)
        pos_now = (df["Sentiment"] == "Positif").sum() if "Sentiment" in df.columns else 0
        pos_pct_now = round((pos_now / total_now * 100), 1) if total_now > 0 else 0.0
        return {
            "fenomena_total_now": int(total_now),
            "fenomena_mom_pct": None,
            "pos_pct_now": pos_pct_now,
            "pos_pct_prev": 0.0,
            "pos_delta_pp": 0.0,
            "label_now": None,
            "label_prev": None
        }

    tmp = df[["tahun", "bulan", "Sentiment"]].copy()
    tmp = tmp[tmp["tahun"].notna() & tmp["bulan"].notna()]
    # konversi tahun ke int
    tmp["tahun"] = pd.to_numeric(tmp["tahun"], errors="coerce")
    tmp["m"] = tmp["bulan"].map(lambda x: MONTH_INDEX.get(str(x), None))
    tmp = tmp.dropna(subset=["tahun", "m"])

    if tmp.empty:
        return {
            "fenomena_total_now": 0,
            "fenomena_mom_pct": None,
            "pos_pct_now": 0.0,
            "pos_pct_prev": 0.0,
            "pos_delta_pp": 0.0,
            "label_now": None,
            "label_prev": None
        }

    tmp["key"] = (tmp["tahun"].astype(int) * 100) + tmp["m"].astype(int)
    grp = tmp.groupby("key")
    totals = grp.size()
    pos_counts = grp.apply(lambda g: (g["Sentiment"] == "Positif").sum())

    latest_key = int(totals.index.max())
    prev_candidates = [k for k in totals.index if k < latest_key]
    prev_key = int(max(prev_candidates)) if prev_candidates else None

    total_now = int(totals.get(latest_key, 0))
    total_prev = int(totals.get(prev_key, 0)) if prev_key is not None else 0

    # MoM total fenomena (%)
    if total_prev > 0:
        mom_pct = round((total_now - total_prev) / total_prev * 100, 1)
    else:
        mom_pct = None  # tidak ada pembanding

    # % positif per bulan (pakai p.p. agar maknanya jelas)
    pos_now = int(pos_counts.get(latest_key, 0))
    pos_prev = int(pos_counts.get(prev_key, 0)) if prev_key is not None else 0

    pos_pct_now = round((pos_now / total_now * 100), 1) if total_now > 0 else 0.0
    pos_pct_prev = round((pos_prev / total_prev * 100), 1) if total_prev > 0 else 0.0
    pos_delta_pp = round(pos_pct_now - pos_pct_prev, 1)

    # Label periode
    def label_from_key(k):
        if k is None: return None
        y = k // 100
        m = k % 100
        return f"{MONTH_ORDER[m-1]} {y}" if 1 <= m <= 12 else str(y)

    return {
        "fenomena_total_now": total_now,
        "fenomena_mom_pct": mom_pct,       # contoh: +12.5 atau -7.1 (None kalau tidak ada prev)
        "pos_pct_now": pos_pct_now,        # contoh: 62.5
        "pos_pct_prev": pos_pct_prev,      # contoh: 57.0
        "pos_delta_pp": pos_delta_pp,      # contoh: +5.5 (p.p.)
        "label_now": label_from_key(latest_key),
        "label_prev": label_from_key(prev_key)
    }

# =======================
# CSV LOADING (RAW GitHub + cache)
# =======================
def _list_csv_urls_from_github_raw_dir(raw_dir_url: str):
    now = datetime.now()
    cache_key = hashlib.md5(raw_dir_url.encode()).hexdigest()
    if cache_key in _csv_list_cache:
        cached_data, cached_time = _csv_list_cache[cache_key]
        if (now - cached_time).total_seconds() < _CACHE_TTL_SECONDS:
            print(f"Using cached CSV list for {raw_dir_url}")
            return cached_data

    print(f"Fetching CSV list from GitHub API: {raw_dir_url}")
    u = urlparse(raw_dir_url)
    if "raw.githubusercontent.com" not in u.netloc:
        return []
    parts = [p for p in u.path.split("/") if p]
    if len(parts) < 4:
        return []
    owner, repo, branch = parts[0], parts[1], parts[2]
    path_in_repo = "/".join(parts[3:]).rstrip("/")
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path_in_repo}?ref={branch}"
    try:
        items = _github_get(api_url)
        csvs = []
        for it in items:
            if it.get("type") == "file" and it.get("name", "").lower().endswith(".csv"):
                csvs.append((it["name"], it.get("download_url")))
        _csv_list_cache[cache_key] = (csvs, now)
        print(f"Cached {len(csvs)} CSV files")
        return csvs
    except Exception as e:
        print(f"Error listing CSV files: {e}")
        if cache_key in _csv_list_cache:
            print("Using stale cache due to error")
            return _csv_list_cache[cache_key][0]
        return []

def _load_csv_with_cache(download_url: str, filename: str):
    now = datetime.now()
    cache_key = hashlib.md5(download_url.encode()).hexdigest()
    if cache_key in _csv_data_cache:
        cached_df, cached_time = _csv_data_cache[cache_key]
        if (now - cached_time).total_seconds() < _DATA_CACHE_TTL_SECONDS:
            print(f"Using cached data for {filename}")
            return cached_df.copy()

    print(f"Loading CSV from URL: {filename}")
    df = None
    for enc in ['utf-8', 'latin1', 'cp1252', 'iso-8859-1']:
        try:
            df = pd.read_csv(download_url, encoding=enc)
            print(f"Loaded {filename} with encoding={enc}, rows={len(df)}")
            break
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            break
    if df is not None:
        _csv_data_cache[cache_key] = (df.copy(), now)
        return df
    return None

def load_data_from_folder(data_dir, year: str | None = None):
    """
    Load data dari folder (GitHub RAW URL atau lokal).
    (Hanya lapangan_usaha & pengeluaran)
    """
    all_data = []

    if isinstance(data_dir, str) and data_dir.startswith("http"):
        try:
            csv_files = _list_csv_urls_from_github_raw_dir(data_dir)
            if not csv_files:
                print(f"Tidak menemukan CSV di URL: {data_dir}")
                return create_sample_data()

            for filename, download_url in csv_files:
                if not download_url:
                    continue
                bulan, tahun = parse_bulan_tahun_from_filename(filename)
                if year and (tahun != year):
                    continue
                df = _load_csv_with_cache(download_url, filename)
                if df is None:
                    print(f"Gagal membaca {filename}")
                    continue
                df["bulan"] = bulan
                df["tahun"] = tahun or "Tanpa Tahun"
                all_data.append(df)

            if all_data:
                result = pd.concat(all_data, ignore_index=True)
                print(f"Total loaded from GitHub: {len(result)} rows")
                return result
            else:
                print("Tidak ada data yang berhasil dimuat dari GitHub, pakai sample.")
                return create_sample_data()

        except Exception as e:
            print(f"Error load dari GitHub URL {data_dir}: {e}")
            return create_sample_data()

    # Lokal
    if not os.path.exists(data_dir):
        print(f"Directory tidak ditemukan: {data_dir} (lokal)")
        return create_sample_data()

    files_found = False
    for filename in os.listdir(data_dir):
        if filename.lower().endswith(".csv"):
            files_found = True
            try:
                bulan, tahun = parse_bulan_tahun_from_filename(filename)
                file_path = os.path.join(data_dir, filename)
                df = None
                for enc in ['utf-8', 'latin1', 'cp1252', 'iso-8859-1']:
                    try:
                        df = pd.read_csv(file_path, encoding=enc)
                        print(f"Successfully loaded {filename} with {enc} encoding")
                        break
                    except UnicodeDecodeError:
                        continue
                if df is None:
                    print(f"Failed to read {filename} with any encoding")
                    continue

                if year and tahun and (tahun != year):
                    continue

                df["bulan"] = bulan
                df["tahun"] = tahun or "Tanpa Tahun"
                all_data.append(df)
            except Exception as e:
                print(f"Error reading {filename}: {e}")
                continue

    if not files_found:
        print(f"Tidak ada file CSV ditemukan di {data_dir} (lokal)")
        return create_sample_data()

    return pd.concat(all_data, ignore_index=True) if all_data else create_sample_data()

def load_selected_data(jenis_data="lapangan_usaha", year: str | None = None):
    if jenis_data == "lapangan_usaha":
        return load_data_from_folder(DATA_LU_DIR, year=year)
    elif jenis_data == "pengeluaran":
        return load_data_from_folder(DATA_PENGELUARAN_DIR, year=year)
    else:
        # default ke lapangan_usaha
        return load_data_from_folder(DATA_LU_DIR, year=year)

def load_all_data():
    df_lu = load_data_from_folder(DATA_LU_DIR)
    df_pengeluaran = load_data_from_folder(DATA_PENGELUARAN_DIR)

    if not df_lu.empty:
        df_lu["jenis_data"] = "Lapangan Usaha"
    if not df_pengeluaran.empty:
        df_pengeluaran["jenis_data"] = "Pengeluaran"

    all_data = []
    if not df_lu.empty:
        all_data.append(df_lu)
    if not df_pengeluaran.empty:
        all_data.append(df_pengeluaran)

    if all_data:
        return pd.concat(all_data, ignore_index=True)
    return pd.DataFrame()

# =======================
# TREND & FILTER HELPERS (tanpa komoditas)
# =======================
def filter_empty_data_for_trend(df, jenis_data="all"):
    if df.empty:
        return df

    if jenis_data != "all" and "jenis_data" in df.columns:
        if jenis_data == "lapangan_usaha":
            df = df[df["jenis_data"] == "Lapangan Usaha"]
        elif jenis_data == "pengeluaran":
            df = df[df["jenis_data"] == "Pengeluaran"]

    df_filtered = df.copy()

    if 'Ringkasan Fenomena' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['Ringkasan Fenomena'].notna()]
        df_filtered = df_filtered[df_filtered['Ringkasan Fenomena'].str.strip() != '']

    if 'Kategori' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['Kategori'].notna()]
        df_filtered = df_filtered[df_filtered['Kategori'].str.strip() != '']

    if 'Sentiment' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['Sentiment'].notna()]
        df_filtered = df_filtered[df_filtered['Sentiment'].str.strip() != '']
        valid_sentiment = ['Positif', 'Negatif']
        df_filtered = df_filtered[df_filtered['Sentiment'].isin(valid_sentiment)]

    if 'bulan' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['bulan'].notna()]
        df_filtered = df_filtered[df_filtered['bulan'].str.strip() != '']

    return df_filtered

def prepare_trend_data(df, jenis_data="all", filter_empty=False):
    if df.empty:
        return {
            'monthly_trend': [],
            'sentiment_distribution': {'Positif': 0, 'Negatif': 0, 'Kosong': 0},
            'category_breakdown': [],
            'top_positive_categories': [],
            'top_negative_categories': [],
            'statistics': {
                'total_data': 0,
                'total_raw_data': 0,
                'growth_rate': 0,
                'peak_month': 'N/A',
                'avg_daily': 0,
                'positive_sentiment_pct': 0
            }
        }

    df_raw = df.copy()

    if jenis_data != "all" and "jenis_data" in df.columns:
        if jenis_data == "lapangan_usaha":
            df = df[df["jenis_data"] == "Lapangan Usaha"]
            df_raw = df_raw[df_raw["jenis_data"] == "Lapangan Usaha"]
        elif jenis_data == "pengeluaran":
            df = df[df["jenis_data"] == "Pengeluaran"]
            df_raw = df_raw[df_raw["jenis_data"] == "Pengeluaran"]

    if filter_empty:
        df = filter_empty_data_for_trend(df, jenis_data)
        if df.empty:
            return {
                'monthly_trend': [],
                'sentiment_distribution': {'Positif': 0, 'Negatif': 0, 'Kosong': len(df_raw)},
                'category_breakdown': [],
                'top_positive_categories': [],
                'top_negative_categories': [],
                'statistics': {
                    'total_data': 0,
                    'total_raw_data': len(df_raw),
                    'growth_rate': 0,
                    'peak_month': 'N/A',
                    'avg_daily': 0,
                    'positive_sentiment_pct': 0
                }
            }

    # Monthly trend
    month_order = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
                   'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
    monthly_counts = df.groupby('bulan').size().to_dict() if 'bulan' in df.columns else {}
    monthly_trend = [{'month': m, 'count': monthly_counts.get(m, 0)} for m in month_order]

    # Sentiment distribution (hanya Sentiment)
    sentiment_counts = df['Sentiment'].value_counts().to_dict() if 'Sentiment' in df.columns else {}
    total_raw_records = len(df_raw)
    total_valid_records = len(df)
    kosong_count = total_raw_records - total_valid_records
    sentiment_distribution = {
        'Positif': sentiment_counts.get('Positif', 0),
        'Negatif': sentiment_counts.get('Negatif', 0),
        'Kosong': max(kosong_count, 0)
    }

    # Category breakdown & top categories
    top_positive_categories, top_negative_categories, category_breakdown = [], [], []
    category_col = 'Kategori' if 'Kategori' in df.columns else None
    if category_col and 'Sentiment' in df.columns:
        try:
            df_pos = df[df['Sentiment'] == 'Positif']
            df_neg = df[df['Sentiment'] == 'Negatif']
            if not df_pos.empty:
                pos_counts = df_pos[category_col].value_counts().head(8).to_dict()
                top_positive_categories = [{'category': str(k), 'count': int(v)} for k, v in pos_counts.items()]
            if not df_neg.empty:
                neg_counts = df_neg[category_col].value_counts().head(8).to_dict()
                top_negative_categories = [{'category': str(k), 'count': int(v)} for k, v in neg_counts.items()]
            all_counts = df[category_col].value_counts().head(10).to_dict()
            category_breakdown = [{'category': str(k), 'count': int(v)} for k, v in all_counts.items()]
        except Exception as e:
            print(f"Error processing category data: {e}")

    total_data = len(df)
    total_raw_data = len(df_raw)
    total_sentiments = df['Sentiment'].notna().sum() if 'Sentiment' in df.columns else 0
    positive_count = len(df[df['Sentiment'] == 'Positif']) if 'Sentiment' in df.columns else 0
    positive_sentiment_pct = round((positive_count / total_sentiments * 100), 1) if total_sentiments > 0 else 0

    monthly_values = list(monthly_counts.values())
    if len(monthly_values) >= 2:
        recent_avg = sum(monthly_values[-3:]) / min(3, len(monthly_values))
        earlier_avg = sum(monthly_values[:-3]) / max(1, len(monthly_values) - 3)
        growth_rate = round(((recent_avg - earlier_avg) / max(earlier_avg, 1)) * 100, 1)
    else:
        growth_rate = 0

    peak_month = max(monthly_counts, key=monthly_counts.get) if monthly_counts else 'N/A'
    avg_daily = int(round(total_data / 30, 0)) if total_data > 0 else 0

    statistics = {
        'total_data': total_data,
        'total_raw_data': total_raw_data,
        'growth_rate': growth_rate,
        'peak_month': peak_month,
        'avg_daily': avg_daily,
        'positive_sentiment_pct': positive_sentiment_pct
    }

    return {
        'monthly_trend': monthly_trend,
        'sentiment_distribution': sentiment_distribution,
        'category_breakdown': category_breakdown,
        'top_positive_categories': top_positive_categories,
        'top_negative_categories': top_negative_categories,
        'statistics': statistics
    }

# =======================
# ROUTES
# =======================
@app.route("/")
def home():
    try:
        df = load_all_data()

        # === hitung MoM untuk beranda ===
        mom = compute_home_mom_stats(df)

        if not df.empty and "Ringkasan Fenomena" in df.columns:
            df_fenomena = df["Ringkasan Fenomena"].dropna().unique().tolist()
        else:
            df_fenomena = []

        if not df.empty and "Kategori" in df.columns:
            # tetap: daftar kategori (sudah kamu benahi normalisasi sebelumnya)
            df_kategori = df["Kategori"].astype(str).str.strip().str.title().unique().tolist()
        else:
            df_kategori = []

        total_sentimen = 0
        positif_count = 0
        if not df.empty and "Sentiment" in df.columns:
            total_sentimen = df["Sentiment"].notna().sum()
            positif_count = (df["Sentiment"] == "Positif").sum()

        positif_percent = round((positif_count / total_sentimen) * 100, 2) if total_sentimen > 0 else 0.0

        latest_dt_utc, latest_path = get_latest_update_datetime()
        latest_dt_id = to_jakarta(latest_dt_utc)
        latest_iso = latest_dt_id.isoformat()

        return render_template(
            "home.html",
            data=df_kategori,
            fenomena=df_fenomena,
            sentimen_positif_count=positif_count,
            sentimen_total=total_sentimen,
            sentimen_positif_percent=positif_percent,
            latest_sync_iso=latest_iso,
            latest_sync_path=latest_path,

            # === variabel baru untuk card statistik ===
            fenomena_mom_pct=mom["fenomena_mom_pct"],    # None atau angka (+/-)
            pos_pct_now=mom["pos_pct_now"],              # % bulan ini (valid)
            pos_delta_pp=mom["pos_delta_pp"],            # perubahan p.p. dari bulan lalu
            label_now=mom["label_now"],
            label_prev=mom["label_prev"]
        )
    except Exception as e:
        print(f"Error in home route: {e}")
        return render_template(
            "home.html",
            data=[],
            fenomena=[],
            sentimen_positif_count=0,
            sentimen_total=0,
            sentimen_positif_percent=0.0,
            latest_sync_iso=None,
            latest_sync_path=None,
            fenomena_mom_pct=None,
            pos_pct_now=0.0,
            pos_delta_pp=0.0,
            label_now=None,
            label_prev=None
        )

@app.route("/fenomena")
def fenomena():
    try:
        jenis_data = request.args.get("jenis_data", "lapangan_usaha")
        tahun = request.args.get("tahun")

        df = load_selected_data(jenis_data, year=tahun)
        df_original = df.copy()

        if not df.empty:
            for col in ['Tanggal', 'Kategori', 'Ringkasan Fenomena', 'Sentiment', 'Alasan', 'Url Berita']:
                if col in df.columns:
                    df[col] = df[col].fillna('')
                if col in df_original.columns:
                    df_original[col] = df_original[col].fillna('')

        kategori_list = sorted(df_original["Kategori"].dropna().unique()) if "Kategori" in df_original.columns else []
        bulan_list = sorted(df_original["bulan"].dropna().unique()) if "bulan" in df_original.columns else []
        sentimen_list = sorted(df_original["Sentiment"].dropna().unique()) if "Sentiment" in df_original.columns else []
        tahun_list = sorted([
            t for t in (df_original["tahun"].dropna().astype(str).unique() if "tahun" in df_original.columns else [])
            if t and t != "Tanpa Tahun" and t.strip().isdigit()
        ], reverse=True)

        kategori = request.args.get("kategori")
        bulan = request.args.get("bulan")
        sentimen = request.args.get("sentimen")

        if not df.empty:
            if kategori and kategori in kategori_list:
                df = df[df["Kategori"] == kategori]
            if bulan and bulan in bulan_list:
                df = df[df["bulan"] == bulan]
            if sentimen and sentimen in sentimen_list:
                df = df[df["Sentiment"] == sentimen]

        jenis_data_list = [
            {"value": "lapangan_usaha", "label": "Lapangan Usaha"},
            {"value": "pengeluaran", "label": "Pengeluaran"}
        ]

        return render_template(
            "fenomena.html",
            data=df.to_dict(orient="records") if not df.empty else [],
            kategori_list=kategori_list,
            bulan_list=bulan_list,
            sentimen_list=sentimen_list,
            tahun_list=tahun_list,
            jenis_data_list=jenis_data_list,
            selected_jenis_data=jenis_data,
            selected_kategori=kategori,
            selected_bulan=bulan,
            selected_sentimen=sentimen,
            selected_tahun=tahun
        )

    except Exception as e:
        print(f"Error di route /fenomena: {e}")
        return render_template(
            "fenomena.html",
            data=[],
            kategori_list=[],
            bulan_list=[],
            sentimen_list=[],
            tahun_list=[],
            jenis_data_list=[
                {"value": "lapangan_usaha", "label": "Lapangan Usaha"},
                {"value": "pengeluaran", "label": "Pengeluaran"}
            ],
            selected_jenis_data="lapangan_usaha",
            selected_tahun=None
        )

@app.route("/trend")
def trend():
    try:
        jenis_data = request.args.get("jenis_data", "all")
        tahun = request.args.get("tahun")

        if jenis_data == "all":
            df = load_all_data()
            if tahun and "tahun" in df.columns:
                df = df[df["tahun"] == tahun]
        else:
            df = load_selected_data(jenis_data, year=tahun)

        tahun_list = sorted([
            t for t in (df["tahun"].dropna().astype(str).unique() if "tahun" in df.columns else [])
            if t and t != "Tanpa Tahun" and t.strip().isdigit()
        ], reverse=True)

        chart_data = prepare_trend_data(df, jenis_data, filter_empty=True)

        jenis_data_list = [
            {"value": "all", "label": "Semua Data"},
            {"value": "lapangan_usaha", "label": "Lapangan Usaha"},
            {"value": "pengeluaran", "label": "Pengeluaran"}
        ]

        return render_template(
            "trend.html",
            chart_data=chart_data,
            jenis_data_list=jenis_data_list,
            tahun_list=tahun_list,
            selected_jenis_data=jenis_data,
            selected_tahun=tahun
        )
    except Exception as e:
        print(f"Error in trend route: {e}")

        default_chart_data = {
            'monthly_trend': [{'month': m, 'count': 0} for m in
                              ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
                               'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']],
            'sentiment_distribution': {'Positif': 0, 'Negatif': 0, 'Kosong': 0},
            'category_breakdown': [],
            'top_positive_categories': [],
            'top_negative_categories': [],
            'statistics': {
                'total_data': 0,
                'total_raw_data': 0,
                'growth_rate': 0,
                'peak_month': 'N/A',
                'avg_daily': 0,
                'positive_sentiment_pct': 0
            }
        }

        jenis_data_list = [
            {"value": "all", "label": "Semua Data"},
            {"value": "lapangan_usaha", "label": "Lapangan Usaha"},
            {"value": "pengeluaran", "label": "Pengeluaran"}
        ]

        return render_template(
            "trend.html",
            chart_data=default_chart_data,
            jenis_data_list=jenis_data_list,
            tahun_list=[],
            selected_jenis_data="all",
            selected_tahun=None
        )

@app.route("/api/trend-data")
def api_trend_data():
    try:
        jenis_data = request.args.get("jenis_data", "all")
        if jenis_data == "all":
            df = load_all_data()
        else:
            df = load_selected_data(jenis_data)
        chart_data = prepare_trend_data(df, jenis_data, filter_empty=True)
        return jsonify(chart_data)
    except Exception as e:
        print(f"Error in API trend data: {e}")
        default_data = {
            'monthly_trend': [{'month': m, 'count': 0} for m in
                              ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
                               'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']],
            'sentiment_distribution': {'Positif': 0, 'Negatif': 0, 'Kosong': 0},
            'category_breakdown': [],
            'top_positive_categories': [],
            'top_negative_categories': [],
            'statistics': {
                'total_data': 0,
                'total_raw_data': 0,
                'growth_rate': 0,
                'peak_month': 'N/A',
                'avg_daily': 0,
                'positive_sentiment_pct': 0
            }
        }
        return jsonify(default_data)

@app.route("/about")
def about():
    latest_dt_utc, latest_path = get_latest_update_datetime()
    latest_dt_id = to_jakarta(latest_dt_utc)
    latest_iso = latest_dt_id.isoformat()
    return render_template(
        "about.html",
        latest_sync_iso=latest_iso,
        latest_sync_path=latest_path
    )

@app.route("/admin/envcheck")
def admin_envcheck():
    return {
        "GITHUB_TOKEN_set": bool(os.getenv("GITHUB_TOKEN")),
        "GITHUB_OWNER": os.getenv("GITHUB_OWNER"),
        "GITHUB_REPO": os.getenv("GITHUB_REPO"),
        "GITHUB_BRANCH": os.getenv("GITHUB_BRANCH"),
    }, 200

# =======================
# CACHE MANAGEMENT (opsional)
# =======================
@app.route("/admin/clear-cache", methods=["POST"])
def clear_cache():
    # --- CSRF guard via header, sejalur dengan admin blueprint ---
    sess_tok = session.get("csrf_token", "")
    hdr_tok = request.headers.get("X-CSRF-Token", "")
    if (not sess_tok) or (hdr_tok != sess_tok):
        abort(403, description="CSRF invalid (clear-cache)")

    global _csv_list_cache, _csv_data_cache, _latest_cache
    _csv_list_cache.clear()
    _csv_data_cache.clear()
    _latest_cache = {"ts": None, "value": None}
    return {"status": "success", "message": "Cache cleared"}, 200

@app.route("/admin/cache-status")
def cache_status():
    return {
        "csv_list_cache_entries": len(_csv_list_cache),
        "csv_data_cache_entries": len(_csv_data_cache),
        "latest_cache_set": _latest_cache["ts"] is not None
    }, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

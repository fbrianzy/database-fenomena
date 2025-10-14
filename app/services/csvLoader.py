import datetime
from urllib.parse import urlparse
import hashlib
import pandas as pd
import os

from app.services.githubApiHelpers import (
    _github_get
)
from app.config.cache import (
    _csv_data_cache, _csv_list_cache, _CACHE_TTL_SECONDS, _DATA_CACHE_TTL_SECONDS, _latest_cache
)
from app.models.sampleData import *
from app.utils.dateParsing import *
from app.config.folders import *

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

import pandas as pd
import os

from app.config.folders import *

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
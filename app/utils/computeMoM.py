from app.config.date import *
from app.utils.filterEmpty import *
import pandas as pd

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

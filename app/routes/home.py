from flask import (
    render_template, Blueprint, url_for
)

from app.services.csvLoader import *
from app.utils.computeMoM import *
from app.services.cacheSystem import *

bp = Blueprint("home", __name__)

@bp.route("/")
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

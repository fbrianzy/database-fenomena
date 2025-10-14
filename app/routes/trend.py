from flask import (
    request, render_template, Blueprint
)

from app.services.csvLoader import *
from app.utils.prepareTrend import *

bp = Blueprint("trend", __name__, url_prefix="/trend")

@bp.route("/")
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

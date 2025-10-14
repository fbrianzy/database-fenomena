# app/routes/api_trend.py
from flask import Blueprint, request, jsonify, current_app
from app.services.csvLoader import load_all_data, load_selected_data
from app.utils.prepareTrend import prepare_trend_data

bp = Blueprint("api_trend", __name__, url_prefix="/api/trend-data")

@bp.route("/", methods=["GET"])
def api_trend_data():
    try:
        jenis_data = request.args.get("jenis_data", "all").lower()

        df = load_all_data() if jenis_data == "all" else load_selected_data(jenis_data)
        chart_data = prepare_trend_data(df, jenis_data, filter_empty=True)

        return jsonify(chart_data), 200

    except Exception as e:
        current_app.logger.exception("Error in /api/trend-data: %s", e)
        default_data = {
            "monthly_trend": [
                {"month": m, "count": 0} for m in
                ["Januari","Februari","Maret","April","Mei","Juni",
                 "Juli","Agustus","September","Oktober","November","Desember"]
            ],
            "sentiment_distribution": {"Positif": 0, "Negatif": 0, "Kosong": 0},
            "category_breakdown": [],
            "top_positive_categories": [],
            "top_negative_categories": [],
            "statistics": {
                "total_data": 0, "total_raw_data": 0, "growth_rate": 0,
                "peak_month": "N/A", "avg_daily": 0, "positive_sentiment_pct": 0
            },
        }
        # bisa pilih: kembalikan default_data (200) atau error (500). Di sini pakai default_data.
        return jsonify(default_data), 200

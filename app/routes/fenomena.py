from flask import ( 
    request, render_template, Blueprint
)

from app.services.csvLoader import *

bp = Blueprint("fenomena", __name__, url_prefix="/fenomena")

@bp.route("/")
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

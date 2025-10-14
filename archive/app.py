import os
import re
import io
import time
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# -----------------------------
# Helpers
# -----------------------------

ID_TYPE_CODES = {
    "Lapangan Usaha": "01",
    "Pengeluaran": "02",
}

BULAN_MAP_ID = {
    "januari": "01",
    "februari": "02",
    "maret": "03",
    "april": "04",
    "mei": "05",
    "juni": "06",
    "juli": "07",
    "agustus": "08",
    "september": "09",
    "oktober": "10",
    "november": "11",
    "desember": "12",
}

def normalize_cols(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize column names to lower_snake_case and map likely variants.
    """
    mapping = {
        "tanggal": ["tanggal", "tgl", "date"],
        "kategori": ["kategori", "category"],
        "ringkasan": ["ringkasan",  "ringkasan_fenomena","summary", "deskripsi", "uraian"],
        "sentiment": ["sentiment", "sentimen", "senti"],
        "alasan": ["alasan", "reason", "justifikasi"],
        "url_berita": ["url_berita", "link", "url"],
    }
    # lower and clean
    df = df.copy()
    df.columns = [re.sub(r"\s+", "_", str(c).strip().lower()) for c in df.columns]

    # build reverse index
    reverse = {}
    for target, aliases in mapping.items():
        for a in aliases:
            reverse[a] = target

    new_cols = []
    for c in df.columns:
        new_cols.append(reverse.get(c, c))
    df.columns = new_cols

    # ensure required columns exist (if missing, create empty)
    for req in ["tanggal", "kategori", "ringkasan", "sentiment", "alasan", "url_berita"]:
        if req not in df.columns:
            df[req] = None
    return df[["tanggal", "kategori", "ringkasan", "sentiment", "alasan", "url_berita"]]

def parse_bulan_tahun_from_filename(filename: str):
    """
    Expecting pattern like 'Agustus_2025.csv' -> ('Agustus', 2025, '08', '25')
    """
    name = os.path.splitext(os.path.basename(filename))[0]
    parts = name.split("_")
    if len(parts) < 2:
        raise ValueError("Nama file harus berbentuk Bulan_Tahun, contoh: Agustus_2025.csv")
    bulan_name = parts[0]
    tahun_full = int(parts[1])
    bulan_num = BULAN_MAP_ID.get(bulan_name.strip().lower())
    if bulan_num is None:
        raise ValueError(f"Bulan '{bulan_name}' tidak dikenali. Gunakan nama bulan Indonesia, contoh: Agustus_2025.csv")
    tahun_2d = f"{tahun_full % 100:02d}"
    return bulan_name, tahun_full, bulan_num, tahun_2d

def build_row_id(bulan_num: str, tahun_2d: str, row_index_1based: int, jenis_kode: str) -> int:
    """
    8 digits: MM YY II TT (e.g., 08 25 02 01) -> 08250201
    """
    ii = f"{row_index_1based:02d}"
    raw = f"{bulan_num}{tahun_2d}{ii}{jenis_kode}"
    return int(raw)

def ensure_table(engine):
    ddl = """
    CREATE TABLE IF NOT EXISTS public.fenomena (
      id               BIGINT PRIMARY KEY,
      tanggal          TEXT,
      kategori         TEXT,
      ringkasan        TEXT,
      sentiment        TEXT,
      alasan           TEXT,
      url_berita       TEXT,
      bulan            TEXT NOT NULL,
      tahun            INTEGER NOT NULL,
      jenis_data       TEXT,
      sumber_file      TEXT,
      uploaded_at      TIMESTAMPTZ DEFAULT now()
    );
    """
    with engine.begin() as conn:
        conn.execute(text(ddl))

def upsert_rows(engine, rows):
    """
    Upsert using ON CONFLICT(id) DO UPDATE
    """
    if not rows:
        return 0
    cols = ["id","tanggal","kategori","ringkasan","sentiment","alasan","url_berita","bulan","tahun","jenis_data","sumber_file"]
    placeholders = ", ".join([f":{c}" for c in cols])
    insert_sql = f"""
    INSERT INTO public.fenomena ({", ".join(cols)})
    VALUES ({placeholders})
    ON CONFLICT (id) DO UPDATE SET
      tanggal=EXCLUDED.tanggal,
      kategori=EXCLUDED.kategori,
      ringkasan=EXCLUDED.ringkasan,
      sentiment=EXCLUDED.sentiment,
      alasan=EXCLUDED.alasan,
      url_berita=EXCLUDED.url_berita,
      bulan=EXCLUDED.bulan,
      tahun=EXCLUDED.tahun,
      jenis_data=EXCLUDED.jenis_data,
      sumber_file=EXCLUDED.sumber_file;
    """
    with engine.begin() as conn:
        conn.execute(text(insert_sql), rows)
    return len(rows)

# -----------------------------
# App
# -----------------------------

st.set_page_config(page_title="Upload Fenomena CSV → PostgreSQL", layout="wide")

st.title("📤 Streamlit: Upload Fenomena CSV → PostgreSQL")
st.caption("Mengimpor CSV bulanan ke tabel **public.fenomena** dengan ID 8-digit (MMYYIITT).")

with st.sidebar:
    st.header("⚙️ Koneksi Database")
    load_dotenv()  # allow .env
    default_url = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres")
    db_url = st.text_input("DATABASE_URL", value=default_url, help="Format: postgresql+psycopg2://user:pass@host:port/dbname")
    test_conn = st.button("🔌 Test Koneksi")

    st.markdown("---")
    st.header("🏷️ Jenis Data")
    jenis_data = st.selectbox("Pilih jenis data (menentukan 2 digit terakhir ID)", options=list(ID_TYPE_CODES.keys()))
    jenis_kode = ID_TYPE_CODES[jenis_data]

    st.markdown("---")
    st.header("🧠 Opsi")
    start_index = st.number_input("Mulai nomor indeks baris dari", min_value=1, value=1, step=1,
                                  help="Biasanya 1. Jika ingin melewati header ekstra atau baris tertentu, bisa diubah.")

if test_conn:
    try:
        engine = create_engine(db_url, pool_pre_ping=True)
        with engine.connect() as _:
            st.success("Koneksi OK!")
    except Exception as e:
        st.error(f"Gagal konek: {e}")

st.subheader("1) Unggah CSV")
uploaded = st.file_uploader("Pilih file CSV (format Bulan_Tahun.csv, contoh: Agustus_2025.csv)", type=["csv"])

if uploaded is not None:
    try:
        bulan_name, tahun_full, bulan_num, tahun_2d = parse_bulan_tahun_from_filename(uploaded.name)
        st.info(f"📅 Deteksi dari nama file: **{bulan_name} {tahun_full}** → MM=`{bulan_num}`, YY=`{tahun_2d}`")
    except Exception as e:
        st.error(str(e))

    # Read CSV
    try:
        # Try utf-8 first, fallback to cp1252
        content = uploaded.read()
        try:
            df = pd.read_csv(io.BytesIO(content))
        except UnicodeDecodeError:
            df = pd.read_csv(io.BytesIO(content), encoding="cp1252")
        st.success(f"CSV terbaca: {df.shape[0]} baris × {df.shape[1]} kolom")
    except Exception as e:
        st.error(f"Gagal membaca CSV: {e}")
        df = None

    if df is not None:
        df_norm = normalize_cols(df)
        # Build preview IDs
        preview = df_norm.copy()
        preview.insert(0, "row_index_1based", range(start_index, start_index + len(preview)))
        preview["id_preview"] = preview["row_index_1based"].apply(lambda i: int(f"{bulan_num}{tahun_2d}{i:02d}{jenis_kode}"))
        preview["bulan"] = bulan_name
        preview["tahun"] = tahun_full
        preview["jenis_data"] = jenis_data
        preview["sumber_file"] = uploaded.name

        st.subheader("2) Pratayang & ID yang akan dibuat")
        st.dataframe(preview.head(50))

        st.download_button(
            "⬇️ Unduh Pratayang (CSV)",
            data=preview.to_csv(index=False).encode("utf-8"),
            file_name=f"preview_{uploaded.name}",
            mime="text/csv"
        )

        st.subheader("3) Kirim ke PostgreSQL")
        if st.button("🚀 Kirim Sekarang"):
            try:
                engine = create_engine(db_url, pool_pre_ping=True)
                ensure_table(engine)

                # Optionally deduplicate by url_berita within this batch
                batch = df_norm.copy()

                rows = []
                for idx, rec in enumerate(batch.to_dict(orient="records"), start=start_index):
                    rid = build_row_id(bulan_num, tahun_2d, idx, jenis_kode)
                    rows.append({
                        "id": rid,
                        "tanggal": rec.get("tanggal"),
                        "kategori": rec.get("kategori"),
                        "ringkasan": rec.get("ringkasan"),
                        "sentiment": rec.get("sentiment"),
                        "alasan": rec.get("alasan"),
                        "url_berita": rec.get("url_berita"),
                        "bulan": bulan_name,
                        "tahun": tahun_full,
                        "jenis_data": jenis_data,
                        "sumber_file": uploaded.name,
                    })

                inserted = upsert_rows(engine, rows)
                st.success(f"Sukses kirim {inserted} baris ke public.fenomena")

                with engine.begin() as conn:
                    count_total = conn.execute(text("SELECT count(*) FROM public.fenomena")).scalar()
                st.info(f"Total baris sekarang di public.fenomena: {count_total}")

            except Exception as e:
                st.error(f"Gagal mengirim ke database: {e}")

st.markdown("---")
with st.expander("ℹ️ Skema Tabel & Format ID"):
    st.code("""
CREATE TABLE IF NOT EXISTS public.fenomena (
  id               BIGINT PRIMARY KEY,  -- 8 digit: MMYYIITT
  tanggal          TEXT,
  kategori         TEXT,
  ringkasan        TEXT,
  sentiment        TEXT,
  alasan           TEXT,
  url_berita       TEXT,
  bulan            TEXT NOT NULL,
  tahun            INTEGER NOT NULL,
  jenis_data       TEXT,
  sumber_file      TEXT,
  uploaded_at      TIMESTAMPTZ DEFAULT now()
);

# Contoh ID: 08250201
# MM=08 (Agustus), YY=25 (2025), II=02 (baris ke-2), TT=01 (Lapangan Usaha)
""")
    st.write("Nama file **Bulan_Tahun.csv** digunakan untuk menentukan `bulan` dan `tahun`.")


# Streamlit CSV → PostgreSQL (Tabel `public.fenomena`)

Aplikasi Streamlit untuk mengunggah CSV bulanan (format **`Bulan_Tahun.csv`**, contoh `Agustus_2025.csv`) ke PostgreSQL.
Setiap baris akan memiliki **ID 8-digit (MMYYIITT)**:
- **MM** = bulan (01–12) dari nama file
- **YY** = 2 digit terakhir tahun dari nama file
- **II** = indeks baris (1-based, bisa di-offset)
- **TT** = jenis data (Lapangan Usaha=01, Pengeluaran=02)

Contoh: `08250201` → Agustus 2025, indeks baris 02, jenis **Lapangan Usaha** (01).

## Kolom yang Dipakai dari CSV
Aplikasi akan melakukan normalisasi nama kolom dan mencari kolom-kolom berikut (varian nama didukung):
- `tanggal` (tgl, date)
- `kategori` (category)
- `ringkasan` (summary, deskripsi, uraian)
- `sentiment` (sentimen, senti)
- `alasan` (reason, justifikasi)
- `url_berita` (link, url)

Jika ada kolom yang tidak ditemukan, kolom tersebut akan diisi kosong.

## Skema Tabel
```sql
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
```

> Catatan: Menggunakan `BIGINT` agar menampung 8 digit murni.

## Cara Menjalankan
1. **Clone/unduh** folder ini.
2. Buat file `.env` dari contoh:
   ```bash
   cp .env.example .env
   # lalu sesuaikan DATABASE_URL
   ```
3. Instal dependency (opsi venv direkomendasikan):
   ```bash
   pip install -r requirements.txt
   ```
4. Jalankan:
   ```bash
   streamlit run app.py
   ```
5. Buka UI Streamlit → masukkan `DATABASE_URL` (atau pakai dari `.env`), pilih **Jenis Data**, unggah CSV (mis. `Agustus_2025.csv`), cek pratayang, lalu **Kirim**.

## Catatan ID & Indeks
- Indeks baris default mulai dari **1**. Jika file memiliki baris header tambahan yang ingin dilewati, atur **Mulai nomor indeks baris dari** pada sidebar.
- `TT` (2 digit terakhir ID) ditentukan oleh pilihan **Jenis Data** pada sidebar:
  - Lapangan Usaha → `01`
  - Pengeluaran → `02`

## Dedup
Terdapat opsi untuk menghindari duplikasi berdasarkan `url_berita` di dalam satu unggahan.

## Troubleshooting
- **Koneksi DB gagal** → pastikan `DATABASE_URL` benar (format `postgresql+psycopg2://user:pass@host:port/dbname`) dan DB dapat diakses.
- **Nama bulan tidak dikenali** → pastikan nama file menggunakan bulan Indonesia yang valid (Januari, Februari, ..., Desember).

## Lisensi
MIT

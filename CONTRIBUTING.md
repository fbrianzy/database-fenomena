# PANDUAN KONTRIBUSI DATABASE FENOMENA

Terima kasih atas minat Anda untuk berkontribusi pada Database Fenomena BPS Kabupaten Sidoarjo! Dokumen ini memberikan panduan lengkap untuk memastikan kontribusi Anda memenuhi standar kualitas yang ditetapkan.

---

## DAFTAR ISI

1. [Prasyarat Kontribusi](#prasyarat-kontribusi)
2. [Alur Kontribusi](#alur-kontribusi)
3. [Standar Format Data](#standar-format-data)
4. [Aturan Pemisah (Delimiter)](#aturan-pemisah-delimiter)
5. [Sistem Prioritas Region](#sistem-prioritas-region)
6. [Panduan Sentiment](#panduan-sentiment)
7. [Verifikasi Sumber Berita](#verifikasi-sumber-berita)
8. [Tips Penulisan](#tips-penulisan)
9. [Proses Review](#proses-review)
10. [Contoh Lengkap](#contoh-lengkap)

---

## PRASYARAT KONTRIBUSI

### Pengetahuan Dasar
- Familiar dengan format CSV
- Memahami cara menggunakan Excel atau Google Spreadsheet
- Memiliki akun GitHub
- Familiar dengan Git (minimal clone, commit, push)

### Tools yang Dibutuhkan
- Microsoft Excel, LibreOffice Calc, atau Google Spreadsheet
- Text editor (opsional, untuk validasi CSV)
- Web browser untuk verifikasi berita

### Waktu yang Dibutuhkan
- Pemula: 3-4 jam untuk 10-15 kategori
- Berpengalaman: 1-2 jam untuk 10-15 kategori

---

## ALUR KONTRIBUSI

### Langkah 1: Persiapan

```bash
# 1. Fork repositori melalui tombol "Fork" di GitHub

# 2. Clone ke komputer lokal
git clone https://github.com/username-anda/database-fenomena.git
cd database-fenomena

# 3. Buat branch baru
git checkout -b kontribusi-agustus-2025-lapangan-usaha
```

### Langkah 2: Download Template

Pilih template sesuai kategori data:
- `templates/lapangan_usaha.csv` - untuk sektor produksi/industri
- `templates/pengeluaran.csv` - untuk konsumsi rumah tangga

### Langkah 3: Pengisian Data

**Di Excel/Google Spreadsheet:**
1. Buka template yang sudah didownload
2. Isi data sesuai panduan (lihat bagian [Standar Format Data](#standar-format-data))
3. Jangan mengubah nama atau urutan kolom
4. Jangan menghapus header

### Langkah 4: Validasi Manual

Sebelum save, pastikan:
- ✅ Semua URL dapat diakses
- ✅ Tanggal sesuai dengan bulan file
- ✅ Tidak ada typo di kolom Sentiment (Positif/Negatif/Kosong)
- ✅ Ringkasan minimal 50 kata, Alasan minimal 30 kata
- ✅ Format pemisah sudah benar (`, ` untuk URL, `; ` untuk tanggal)

### Langkah 5: Save sebagai CSV

**Di Microsoft Excel:**
1. File → Save As
2. Pilih "CSV UTF-8 (Comma delimited) (*.csv)"
3. Nama file: `Agustus_2025.csv` (sesuaikan bulan/tahun)
4. Save

**Di Google Spreadsheet:**
1. File → Download → Comma Separated Values (.csv)
2. Rename file menjadi `Agustus_2025.csv`

**Di LibreOffice Calc:**
1. File → Save As
2. Format: Text CSV (.csv)
3. Character set: Unicode (UTF-8)
4. Field delimiter: `,` (koma)
5. String delimiter: `"` (double quote)

### Langkah 6: Penempatan File

Pindahkan file ke folder yang sesuai:

```bash
# Untuk data lapangan usaha
mv Agustus_2025.csv contribution/lapangan_usaha/

# Untuk data pengeluaran
mv Agustus_2025.csv contribution/pengeluaran/
```

Struktur akhir:
```
contribution/
├── lapangan_usaha/
│   └── Agustus_2025.csv
└── pengeluaran/
    └── Agustus_2025.csv
```

### Langkah 7: Commit dan Push

```bash
# Add file
git add contribution/

# Commit dengan pesan deskriptif
git commit -m "Menambahkan data lapangan usaha Agustus 2025

- Total 35 kategori terisi
- Fokus region Sidoarjo
- Sumber: media lokal terverifikasi"

# Push ke GitHub
git push origin kontribusi-agustus-2025-lapangan-usaha
```

### Langkah 8: Buat Pull Request

1. Buka repositori Anda di GitHub
2. Klik tombol "Compare & pull request"
3. Isi deskripsi Pull Request:

```markdown
## Data Kontribusi

**Periode**: Agustus 2025
**Kategori**: Lapangan Usaha
**Jumlah Entri**: 35 kategori

## Ringkasan

- Fokus berita region Sidoarjo
- Menggunakan 12 sumber media lokal
- Total 48 berita yang dirangkum
- Sentiment: 25 Positif, 8 Negatif, 2 Kosong

## Checklist

- [x] Format CSV valid (UTF-8)
- [x] Penamaan file sesuai standar
- [x] Semua URL dapat diakses
- [x] Tanggal sesuai dengan bulan
- [x] Tidak ada hoaks
- [x] Mengikuti kode etik
```

4. Klik "Create pull request"

---

## STANDAR FORMAT DATA

### Struktur Kolom (TIDAK BOLEH DIUBAH)

| No | Kolom | Format | Wajib | Validasi |
|----|-------|--------|-------|----------|
| 1 | Kategori | Text | Ya | Sesuai template, tidak boleh diubah |
| 2 | Url Berita | Text | Tidak* | Format URL valid, dipisah `, ` |
| 3 | Tanggal | Text | Tidak* | Format "DD Bulan", dipisah `; ` |
| 4 | Ringkasan Fenomena | Text | Tidak* | Minimal 50 kata, maksimal 300 kata |
| 5 | Sentiment | Text | Ya | Hanya "Positif", "Negatif", atau "Kosong" |
| 6 | Alasan | Text | Tidak* | Minimal 30 kata jika Sentiment bukan "Kosong" |

*Wajib diisi jika Sentiment bukan "Kosong"

### Aturan Pengisian per Kolom

#### Kolom 1: Kategori

**Aturan:**
- TIDAK BOLEH diubah atau ditambah
- Harus persis sama dengan yang ada di template
- Case-sensitive (perhatikan huruf besar/kecil)

**Benar:**
```csv
Tanaman Pangan
Industri Makanan dan Minuman
```

**Salah:**
```csv
tanaman pangan          # huruf kecil
Tanaman pangan          # kapitalisasi salah
Tanaman Pangan & Olahan # menambah kata
```

#### Kolom 2: Url Berita

**Format Pemisah:** Koma + Spasi (`, `)

**Aturan:**
- Harus URL lengkap dengan protokol (https://)
- Maksimal 5 URL per entri
- Setiap URL harus dapat diakses
- Dipisahkan dengan `, ` (koma spasi)

**Contoh Benar:**

*Satu URL:*
```csv
https://radarsidoarjo.jawapos.com/ekonomi/artikel-contoh
```

*Dua URL:*
```csv
https://radarsidoarjo.jawapos.com/ekonomi/artikel1, https://detik.com/jatim/berita2
```

*Tiga URL:*
```csv
https://radarsidoarjo.jawapos.com/artikel1, https://antaranews.com/artikel2, https://kompas.com/artikel3
```

**Contoh Salah:**

```csv
# Tidak ada spasi setelah koma
https://radarsidoarjo.jawapos.com/artikel1,https://detik.com/artikel2

# Menggunakan titik koma
https://radarsidoarjo.jawapos.com/artikel1; https://detik.com/artikel2

# Tanpa protokol
radarsidoarjo.jawapos.com/artikel1

# URL rusak atau tidak lengkap
https://example.com/
```

#### Kolom 3: Tanggal

**Format Pemisah:** Titik koma + Spasi (`; `)

**Format Penulisan:** `DD Bulan` (tanpa tahun, tanpa leading zero)

**Aturan:**
- Tanggal HARUS 100% sesuai dengan bulan file CSV
- Nama bulan ditulis lengkap (bukan angka)
- Huruf pertama bulan HARUS kapital
- Dipisahkan dengan `; ` (titik koma spasi)
- Tidak menggunakan leading zero (1 bukan 01)

**Contoh Benar:**

*Satu tanggal:*
```csv
15 Agustus
1 Agustus
28 Agustus
```

*Dua tanggal:*
```csv
5 Agustus; 20 Agustus
```

*Tiga tanggal atau lebih:*
```csv
1 Agustus; 15 Agustus; 28 Agustus
5 Agustus; 12 Agustus; 19 Agustus; 26 Agustus
```

**Contoh Salah:**

```csv
# Menggunakan leading zero
01 Agustus; 05 Agustus

# Menggunakan angka bulan
15-08-2025
15/08/2025

# Bulan huruf kecil
15 agustus

# Menggunakan koma sebagai pemisah
15 Agustus, 20 Agustus

# Tidak ada spasi setelah titik koma
15 Agustus;20 Agustus

# Tanggal dari bulan lain (file untuk Agustus)
30 Juli; 5 Agustus
28 Agustus; 2 September

# Menyertakan tahun
15 Agustus 2025
```

#### Kolom 4: Ringkasan Fenomena

**Aturan:**
- Minimal 50 kata, maksimal 300 kata
- Objektif dan faktual (tidak ada opini pribadi)
- Bahasa Indonesia baku
- Sertakan data kuantitatif jika ada
- Tidak copy-paste langsung dari berita (parafrase)

**Struktur yang Baik:**
1. **Kalimat pembuka**: Siapa/apa yang menjadi subjek
2. **Inti berita**: Apa yang terjadi
3. **Detail pendukung**: Data, angka, konteks
4. **Dampak/implikasi** (jika relevan)

**Contoh Benar:**

```csv
"Dinas Pangan dan Pertanian Kabupaten Sidoarjo menggelar Sinkronisasi dan Koordinasi Program Ketahanan Pangan 2025 dengan tema Optimalisasi Pemanfaatan Dana Desa. Acara ini dihadiri oleh Asisten II Administrasi Perekonomian dan pembangunan Sekretaris Daerah Kabupaten Sidoarjo, Kepala Dinas Pangan dan Pertanian, serta para Kepala Desa. Program ketahanan pangan bertujuan untuk meningkatkan ketersediaan pangan yang beragam, bergizi, dan aman. Acara ini juga menekankan pentingnya swasembada pangan sebagai bagian dari misi Asta Cita pemerintah pusat."
```

**Contoh Salah:**

```csv
# Terlalu pendek (kurang dari 50 kata)
"Dinas Pertanian Sidoarjo gelar acara ketahanan pangan. Dihadiri pejabat daerah."

# Copy-paste langsung dari berita (identik 100%)
"Menurut Kepala Dinas...[kutipan persis dari artikel]"

# Mengandung opini pribadi
"Dinas Pertanian menggelar acara yang sangat bagus dan mengesankan..."

# Bahasa tidak baku
"Pemda Sidoarjo ngadain acara buat ngebahas ketahanan pangan."
```

**Tips Penulisan:**
- Gunakan kata hubung yang tepat (sehingga, karena, dengan demikian)
- Hindari pengulangan kata yang tidak perlu
- Tulis secara ringkas tapi informatif
- Fokus pada informasi penting, buang detail yang tidak relevan

#### Kolom 5: Sentiment

**HANYA 3 PILIHAN VALID:**

| Sentiment | Kapan Digunakan | Aturan Penulisan |
|-----------|-----------------|------------------|
| `Positif` | Ada berita dengan dampak positif | P kapital, sisanya huruf kecil |
| `Negatif` | Ada berita dengan dampak negatif | N kapital, sisanya huruf kecil |
| `Kosong` | Tidak ada berita yang ditemukan | K kapital, sisanya huruf kecil |

**Penulisan yang Benar:**
```csv
Positif
Negatif
Kosong
```

**Penulisan yang SALAH:**
```csv
positif       # huruf kecil semua
POSITIF       # huruf besar semua
Netral        # tidak ada opsi netral
Baik          # tidak sesuai format
Buruk         # tidak sesuai format
kosong        # huruf kecil
-             # tidak boleh simbol
(kosong)      # tidak boleh tanda kurung
```

#### Kolom 6: Alasan

**Aturan:**
- Minimal 30 kata (jika Sentiment bukan "Kosong")
- Jelaskan MENGAPA sentiment tersebut dipilih
- Harus analitis, bukan sekadar mengulang ringkasan
- Hubungkan dengan dampak ekonomi/sosial

**Struktur yang Baik:**
1. **Identifikasi poin utama** (1 kalimat)
2. **Jelaskan implikasi/dampak** (1-2 kalimat)
3. **Hubungkan dengan konteks lebih luas** (1 kalimat, opsional)

**Contoh Benar:**

```csv
"Acara koordinasi ketahanan pangan menunjukkan komitmen pemerintah daerah dalam mewujudkan swasembada pangan. Keterlibatan berbagai pihak termasuk perbankan dan kepala desa menunjukkan pendekatan holistik yang dapat meningkatkan keberhasilan program. Inisiatif ini berdampak positif pada ketahanan pangan lokal dan kesejahteraan petani di Kabupaten Sidoarjo."
```

**Contoh Salah:**

```csv
# Terlalu pendek (kurang dari 30 kata)
"Karena ada acara koordinasi pangan yang baik."

# Hanya mengulang ringkasan
"Dinas Pangan menggelar acara koordinasi dengan berbagai pihak untuk membahas ketahanan pangan."

# Tidak ada analisis
"Beritanya bagus dan positif untuk daerah."

# Terlalu subjektif
"Menurut saya program ini akan sangat sukses dan membawa perubahan besar."
```

---

## ATURAN PEMISAH (DELIMITER)

### Ringkasan Format Pemisah

| Data | Pemisah | Contoh |
|------|---------|--------|
| URL | `, ` (koma spasi) | `url1, url2, url3` |
| Tanggal | `; ` (titik koma spasi) | `1 Agustus; 15 Agustus` |
| Kolom CSV | `,` (koma) | Otomatis oleh Excel |

### Detail Penggunaan

#### 1. Pemisah URL: Koma + Spasi (`, `)

**Benar:**
```csv
https://radarsidoarjo.jawapos.com/berita1, https://detik.com/berita2
```

**Salah:**
```csv
https://radarsidoarjo.jawapos.com/berita1,https://detik.com/berita2  # tidak ada spasi
https://radarsidoarjo.jawapos.com/berita1; https://detik.com/berita2  # pakai titik koma
https://radarsidoarjo.jawapos.com/berita1 , https://detik.com/berita2  # spasi sebelum koma
```

#### 2. Pemisah Tanggal: Titik Koma + Spasi (`; `)

**Benar:**
```csv
1 Agustus; 15 Agustus; 28 Agustus
```

**Salah:**
```csv
1 Agustus, 15 Agustus, 28 Agustus  # pakai koma
1 Agustus;15 Agustus;28 Agustus    # tidak ada spasi
1 Agustus ; 15 Agustus ; 28 Agustus  # spasi sebelum titik koma
```

#### 3. Text dengan Koma di Dalamnya

Jika teks mengandung koma (misalnya dalam Ringkasan), gunakan tanda kutip:

**Contoh:**
```csv
"Produksi meningkat 20%, sehingga petani senang"
"Acara dihadiri Bupati, Camat, dan Kepala Desa"
```

Excel/Spreadsheet akan otomatis menambahkan tanda kutip jika diperlukan.

---

## SISTEM PRIORITAS REGION

### Hierarki Pencarian Berita

```
┌─────────────────────────────┐
│   1. SIDOARJO (PRIORITAS)   │  ← UTAMA
└──────────────┬──────────────┘
               │ Tidak ada? ↓
┌──────────────┴──────────────┐
│      2. SURABAYA            │
└──────────────┬──────────────┘
               │ Tidak ada? ↓
┌──────────────┴──────────────┐
│     3. JAWA TIMUR           │
└──────────────┬──────────────┘
               │ Tidak ada? ↓
┌──────────────┴──────────────┐
│     4. INDONESIA            │  ← Opsi terakhir
└─────────────────────────────┘
```

### Aturan Ketat

#### ✅ WAJIB DILAKUKAN:

1. **Prioritaskan Sidoarjo**
   - Selalu cari berita Sidoarjo terlebih dahulu
   - Gunakan kata kunci: "Sidoarjo", "Kab Sidoarjo", "Kabupaten Sidoarjo"
   - Cek media lokal: Radar Sidoarjo, Surya, Jawa Pos edisi Sidoarjo

2. **Dokumentasikan Upaya Pencarian**
   - Jika tidak menemukan berita Sidoarjo, catat kata kunci yang sudah dicoba
   - Screenshot hasil pencarian (opsional, untuk bukti)

3. **Gunakan Level Berikutnya Hanya Jika Benar-Benar Tidak Ada**
   - Jika sudah mencari dengan 5+ kata kunci berbeda
   - Sudah mengecek minimal 3 media lokal
   - Berita yang ditemukan tidak relevan dengan kategori

#### ❌ TIDAK BOLEH DILAKUKAN:

1. **Langsung Menggunakan Berita Nasional**
   ```csv
   # SALAH - Langsung pakai berita nasional tanpa cek Sidoarjo
   Kategori: Tanaman Pangan
   Url: https://kompas.com/ekonomi/pertanian-indonesia
   ```

2. **Menggunakan Berita Luar Region yang Tidak Relevan**
   ```csv
   # SALAH - Berita Jakarta, tidak ada hubungan dengan Sidoarjo
   Kategori: Perikanan
   Url: https://detik.com/perikanan-jakarta-meningkat
   ```

3. **Skip Pencarian dengan Alasan Praktis**
   - "Tidak ada waktu mencari berita Sidoarjo"
   - "Berita nasional lebih lengkap"
   - "Lebih mudah dapat berita Jakarta"

### Contoh Implementasi

#### Contoh 1: Menemukan Berita Sidoarjo (IDEAL)

**Kategori:** Tanaman Pangan

**Proses:**
1. Cari "tanaman pangan Sidoarjo Agustus 2025" → ✅ Dapat berita
2. Verifikasi sumber → ✅ Radar Sidoarjo
3. Cek tanggal → ✅ 15 Agustus 2025

**Hasil:**
```csv
Tanaman Pangan,https://radarsidoarjo.jawapos.com/pertanian/...,15 Agustus,"...",Positif,"..."
```

#### Contoh 2: Tidak Ada di Sidoarjo, Dapat di Surabaya

**Kategori:** Industri Tekstil

**Proses:**
1. Cari "industri tekstil Sidoarjo Agustus 2025" → ❌ Tidak ada
2. Cari "pabrik garmen Sidoarjo Agustus 2025" → ❌ Tidak ada
3. Cari "tekstil Jawa Timur Agustus 2025" → ✅ Dapat berita Surabaya
4. Verifikasi relevansi → ✅ Relevan dengan ekonomi regional

**Hasil:**
```csv
Industri Tekstil,https://suara surabaya.net/industri/...,20 Agustus,"...",Positif,"..."
```

#### Contoh 3: Tidak Ada Sama Sekali

**Kategori:** Perkebunan Semusim

**Proses:**
1. Cari "perkebunan semusim Sidoarjo Agustus 2025" → ❌
2. Cari "perkebunan Sidoarjo Agustus 2025" → ❌
3. Cari "perkebunan semusim Surabaya Agustus 2025" → ❌
4. Cari "perkebunan semusim Jawa Timur Agustus 2025" → ❌
5. Cari "perkebunan semusim Indonesia Agustus 2025" → ❌

**Hasil:**
```csv
Perkebunan Semusim,,,,Kosong,
```

### Tips Pencarian Efektif

**Kata Kunci yang Efektif:**
- "Sidoarjo + [nama kategori] + Agustus 2025"
- "Kabupaten Sidoarjo + [sektor] + berita terbaru"
- "[kategori] + Jawa Timur + Agustus 2025" (jika tidak ada di Sidoarjo)

**Platform Pencarian:**
- Google: `site:radarsidoarjo.jawapos.com [kata kunci]`
- Google News: Filter by location → Jawa Timur
- Langsung ke website media lokal

**Tools Bantu:**
- Google Alerts untuk tracking berita harian
- RSS Reader untuk agregasi berita lokal
- Bookmark folder untuk media lokal favorit

---

## PANDUAN SENTIMENT

### Definisi Lengkap

#### 1. Sentiment "Positif"

**Kapan Menggunakan:**
- Berita menunjukkan pertumbuhan, peningkatan, atau perkembangan baik
- Ada pencapaian, penghargaan, atau keberhasilan
- Program/kebijakan berdampak menguntungkan
- Inovasi atau terobosan baru yang bermanfaat
- Investasi baru atau ekspansi usaha
- Perbaikan kondisi ekonomi/sosial

**Indikator Positif:**
- ✅ Kenaikan produksi, penjualan, ekspor
- ✅ Pembukaan lapangan kerja
- ✅ Investasi atau modal masuk
- ✅ Penghargaan atau sertifikasi
- ✅ Program sosial berhasil
- ✅ Infrastruktur baru dibangun
- ✅ Kerjasama atau MOU strategis
- ✅ Teknologi baru diterapkan

**Contoh Kasus Positif:**
```csv
# Kenaikan produksi
"Produksi padi di Sidoarjo meningkat 20% pada periode tanam kedua tahun 2025"
→ Sentiment: Positif

# Investasi baru
"PT XYZ investasi Rp 50 miliar untuk pabrik baru di Sidoarjo, buka 500 lowongan kerja"
→ Sentiment: Positif

# Penghargaan
"UMKM Sidoarjo raih penghargaan produk terbaik tingkat nasional"
→ Sentiment: Positif
```

#### 2. Sentiment "Negatif"

**Kapan Menggunakan:**
- Berita menunjukkan penurunan, kerugian, atau masalah
- Ada kecelakaan, bencana, atau insiden merugikan
- Penutupan usaha atau PHK
- Pelanggaran hukum, korupsi, atau kasus kriminal
- Penurunan kualitas layanan/produk
- Protes atau penolakan masyarakat
- Dampak merugikan dari kebijakan/kejadian

**Indikator Negatif:**
- ❌ Penurunan produksi, penjualan, ekspor
- ❌ PHK atau pengurangan tenaga kerja
- ❌ Penutupan pabrik/usaha
- ❌ Kecelakaan kerja atau industri
- ❌ Pencemaran lingkungan
- ❌ Korupsi atau pelanggaran hukum
- ❌ Konflik atau protes masyarakat
- ❌ Kenaikan harga signifikan (inflasi)

**Contoh Kasus Negatif:**
```csv
# Penurunan produksi
"Produksi rumput laut di Sidoarjo turun 30% akibat cuaca ekstrem"
→ Sentiment: Negatif

# PHK
"Pabrik tekstil di Sidoarjo tutup, 200 pekerja di-PHK"
→ Sentiment: Negatif

# Pelanggaran
"Perusahaan di Sidoarjo didenda Rp 500 juta karena buang limbah sembarangan"
→ Sentiment: Negatif
```

#### 3. Sentiment "Kosong"

**Kapan Menggunakan:**
- Sudah melakukan pencarian menyeluruh (Sidoarjo → Surabaya → Jatim → Indonesia)
- Tidak menemukan berita relevan untuk kategori tersebut di bulan yang dimaksud
- Berita yang ditemukan tidak kredibel atau tidak memenuhi standar

**Cara Mengisi:**
```csv
Perkebunan Semusim,,,,Kosong,
```

Atau bisa juga kolom 2-4 dan 6 dibiarkan kosong:
```csv
Perkebunan Semusim,,,,,
```

**PENTING:** Jika mengisi "Kosong", kolom Url Berita, Tanggal, Ringkasan Fenomena, dan Alasan HARUS kosong atau tidak diisi.

### Kasus Khusus dan Edge Cases

#### Kasus 1: Berita Campuran (Positif dan Negatif)

**Contoh:**
> "Pabrik baru di Sidoarjo buka 1000 lowongan kerja, namun warga protes karena polusi udara"

**Cara Menentukan:**
1. Identifikasi dampak mana yang lebih dominan
2. Pertimbangkan skala dampak (berapa banyak orang terpengaruh)
3. Lihat fokus utama berita (judul dan lead paragraph)

**Analisis:**
- Positif: 1000 lapangan kerja (dampak ekonomi besar)
- Negatif: Polusi udara (dampak lingkungan dan kesehatan)

**Keputusan:**
- Jika fokus berita pada penciptaan kerja → **Positif**
- Jika fokus berita pada protes warga → **Negatif**

#### Kasus 2: Kebijakan/Program Baru Belum Ada Dampak

**Contoh:**
> "Pemkab Sidoarjo luncurkan program baru untuk UMKM"

**Cara Menentukan:**
- Jika sudah ada bukti keberhasilan/kegagalan awal → Positif/Negatif
- Jika baru peluncuran tanpa implementasi → Cari berita lain yang lebih substantif
- Jika tidak ada berita lain → Pertimbangkan gunakan berita ini dengan analisis hati-hati

**Rekomendasi:**
Lebih baik cari berita tentang dampak nyata daripada sekadar pengumuman.

#### Kasus 3: Data Statistik Rutin

**Contoh:**
> "BPS: Inflasi Sidoarjo 0,5% di bulan Agustus"

**Cara Menentukan:**
1. Bandingkan dengan bulan sebelumnya
2. Lihat tren (naik/turun)
3. Pertimbangkan konteks (apakah normal atau tidak)

**Analisis:**
- Jika inflasi naik signifikan (>1% perbulan) → **Negatif**
- Jika inflasi terkendali (<1%, sesuai target) → **Positif**
- Jika inflasi turun → **Positif**

---

## VERIFIKASI SUMBER BERITA

### Checklist Verifikasi (WAJIB)

Sebelum memasukkan berita, pastikan:

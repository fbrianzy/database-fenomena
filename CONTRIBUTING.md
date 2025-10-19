# PANDUAN KONTRIBUSI

Dokumen ini menjelaskan tata cara berkontribusi data fenomena ke Database BPS Sidoarjo secara lengkap dan terstruktur.

## DAFTAR ISI

1. [Persiapan](#persiapan)
2. [Format Data](#format-data)
3. [Aturan Pengisian](#aturan-pengisian)
4. [Prioritas Region](#prioritas-region)
5. [Panduan Sentiment](#panduan-sentiment)
6. [Tutorial Pull Request](#tutorial-pull-request)
7. [Proses Review](#proses-review)

---

## PERSIAPAN

### Prasyarat
- Akun GitHub
- Microsoft Excel, LibreOffice Calc, atau Google Spreadsheet
- Pemahaman dasar format CSV

### Langkah Awal
1. Fork repositori ke akun GitHub pribadi
2. Clone repositori hasil fork ke komputer lokal
3. Download template dari folder `templates/`
4. Pilih template sesuai kategori: `lapangan_usaha.csv` atau `pengeluaran.csv`

---

## FORMAT DATA

### Struktur Kolom

| No | Nama Kolom | Tipe | Wajib | Keterangan |
|----|------------|------|-------|------------|
| 1 | Kategori | Text | Ya | Sesuai template, tidak boleh diubah |
| 2 | Url Berita | Text | Kondisional | Link sumber berita lengkap |
| 3 | Tanggal | Text | Kondisional | Tanggal publikasi berita |
| 4 | Ringkasan Fenomena | Text | Kondisional | Minimal 50 kata, maksimal 300 kata |
| 5 | Sentiment | Text | Ya | Hanya: `Positif`, `Negatif`, atau `Kosong` |
| 6 | Alasan | Text | Kondisional | Minimal 30 kata |

**Kondisional:** Wajib diisi jika Sentiment bukan `Kosong`

### Aturan Pemisah

| Elemen | Pemisah | Contoh |
|--------|---------|--------|
| URL | `, ` (koma spasi) | `https://url1, https://url2, https://url3` |
| Tanggal | `; ` (titik koma spasi) | `1 Agustus; 15 Agustus; 28 Agustus` |

### Penamaan File

Format: `{Nama_Bulan}_{Tahun}.csv`

**Valid:**
- `Agustus_2025.csv`
- `September_2025.csv`
- `Januari_2026.csv`

**Tidak Valid:**
- `agustus_2025.csv` (huruf kecil)
- `08_2025.csv` (format angka)
- `Agustus 2025.csv` (mengandung spasi)

---

## ATURAN PENGISIAN

### Kolom 1: Kategori
- Tidak boleh diubah atau ditambah
- Harus persis sama dengan template
- Case-sensitive

### Kolom 2: Url Berita
**Format:**
```
https://radarsidoarjo.jawapos.com/berita1
https://radarsidoarjo.jawapos.com/berita1, https://detik.com/berita2
```

**Aturan:**
- Maksimal 5 URL per entri
- Harus lengkap dengan `https://`
- Dipisahkan dengan `, ` (koma spasi)
- Semua URL harus dapat diakses

### Kolom 3: Tanggal
**Format:** `DD Bulan` (tanpa tahun, tanpa leading zero)

**Contoh:**
```
15 Agustus
1 Agustus; 20 Agustus
5 Agustus; 12 Agustus; 28 Agustus
```

**Aturan:**
- Tanggal harus 100% sesuai bulan file CSV
- Nama bulan ditulis lengkap dengan huruf kapital pertama
- Tidak menggunakan leading zero (tulis `1` bukan `01`)
- Dipisahkan dengan `; ` (titik koma spasi)
- Tidak boleh mencantumkan tanggal dari bulan lain

### Kolom 4: Ringkasan Fenomena
**Aturan:**
- Minimal 50 kata, maksimal 300 kata
- Objektif dan faktual tanpa opini pribadi
- Bahasa Indonesia baku dan profesional
- Sertakan data kuantitatif jika tersedia
- Tidak copy-paste langsung dari artikel (parafrase)

**Struktur yang Baik:**
1. Kalimat pembuka: subjek utama
2. Inti berita: kejadian yang terjadi
3. Detail pendukung: data dan konteks
4. Dampak atau implikasi (jika relevan)

### Kolom 5: Sentiment
**Hanya 3 pilihan:**
- `Positif` - Berita menunjukkan perkembangan baik atau dampak menguntungkan
- `Negatif` - Berita menunjukkan masalah atau dampak merugikan
- `Kosong` - Tidak menemukan berita relevan setelah pencarian menyeluruh

**Penulisan Benar:**
```
Positif
Negatif
Kosong
```

**Penulisan Salah:**
```
positif, POSITIF, Netral, kosong, -, (kosong)
```

### Kolom 6: Alasan
**Aturan:**
- Minimal 30 kata (jika Sentiment bukan `Kosong`)
- Jelaskan mengapa sentiment tersebut dipilih
- Harus analitis, bukan mengulang ringkasan
- Hubungkan dengan dampak ekonomi atau sosial

**Struktur:**
1. Identifikasi poin utama (1 kalimat)
2. Jelaskan implikasi atau dampak (1-2 kalimat)
3. Hubungkan dengan konteks lebih luas (opsional)

### Ketentuan "Kosong"
Jika Sentiment adalah `Kosong`, kolom 2-4 dan 6 dibiarkan kosong:
```csv
Perkebunan Semusim,,,,Kosong,
```

---

## PRIORITAS REGION

### Hierarki Pencarian

```
1. SIDOARJO (Prioritas Utama)
   ↓ Tidak ada?
2. SURABAYA
   ↓ Tidak ada?
3. JAWA TIMUR
   ↓ Tidak ada?
4. INDONESIA (Opsi Terakhir)
```

### Aturan Ketat

**Wajib:**
- Selalu cari berita Sidoarjo terlebih dahulu
- Minimal gunakan 5 kata kunci berbeda
- Cek minimal 3 media lokal berbeda
- Dokumentasikan upaya pencarian

**Tidak Boleh:**
- Langsung menggunakan berita nasional tanpa cek Sidoarjo
- Skip pencarian dengan alasan praktis
- Menggunakan berita luar region yang tidak relevan

### Kata Kunci Efektif
- "Sidoarjo + [kategori] + Agustus 2025"
- "Kabupaten Sidoarjo + [sektor] + berita"
- "[kategori] + Jawa Timur + Agustus" (jika tidak ada di Sidoarjo)

### Sumber Media Prioritas

**Media Lokal (Prioritas Tinggi):**
- Radar Sidoarjo (radarsidoarjo.jawapos.com)
- Jawa Pos
- Surya.co.id
- Berita Jatim

**Media Nasional (Jika tidak ada lokal):**
- Kompas, Tempo, Detik, Liputan6
- Antara News, Bisnis Indonesia
- CNBC Indonesia, Kontan, Katadata

**Website Pemerintah:**
- Semua domain .go.id
- sidoarjokab.go.id
- bps.go.id

---

## PANDUAN SENTIMENT

### Positif
**Indikator:**
- Kenaikan produksi, penjualan, ekspor
- Investasi baru atau ekspansi usaha
- Penciptaan lapangan kerja
- Penghargaan atau sertifikasi
- Program berhasil dilaksanakan
- Inovasi atau teknologi baru

**Contoh:**
```
"Produksi padi Sidoarjo meningkat 20% pada periode tanam kedua"
→ Sentiment: Positif
```

### Negatif
**Indikator:**
- Penurunan produksi atau penjualan
- PHK atau penutupan usaha
- Kecelakaan atau bencana
- Pelanggaran hukum atau korupsi
- Pencemaran lingkungan
- Protes atau penolakan masyarakat

**Contoh:**
```
"Pabrik tekstil tutup, 200 pekerja terkena PHK"
→ Sentiment: Negatif
```

### Kosong
**Kapan Digunakan:**
- Sudah melakukan pencarian menyeluruh di semua prioritas region
- Tidak menemukan berita relevan untuk kategori di bulan tersebut
- Berita yang ditemukan tidak memenuhi standar kredibilitas

### Kasus Khusus

**Berita Campuran (Positif dan Negatif):**
- Tentukan dampak mana yang lebih dominan
- Pertimbangkan skala dampak
- Lihat fokus utama berita (judul dan lead)

**Kebijakan Baru Tanpa Implementasi:**
- Lebih baik cari berita tentang dampak nyata
- Jika tidak ada pilihan lain, analisis dengan hati-hati

**Data Statistik Rutin:**
- Bandingkan dengan periode sebelumnya
- Lihat tren (naik/turun)
- Pertimbangkan konteks dan normalitas

---

## TUTORIAL PULL REQUEST

### Langkah 1: Persiapan File

```bash
# Clone repositori hasil fork
git clone https://github.com/username-anda/database-fenomena.git
cd database-fenomena

# Buat branch baru
git checkout -b kontribusi-agustus-2025
```

### Langkah 2: Isi Data

1. Buka template di Excel atau Google Spreadsheet
2. Isi data sesuai panduan
3. Validasi manual:
   - Semua URL dapat diakses
   - Tanggal sesuai bulan file
   - Format pemisah benar
   - Tidak ada typo di kolom Sentiment

### Langkah 3: Save sebagai CSV

**Di Microsoft Excel:**
```
File → Save As → CSV UTF-8 (Comma delimited)
Nama: Agustus_2025.csv
```

**Di Google Spreadsheet:**
```
File → Download → Comma Separated Values (.csv)
Rename: Agustus_2025.csv
```

### Langkah 4: Tempatkan File

```bash
# Pindahkan ke folder contribution
mv Agustus_2025.csv contribution/lapangan_usaha/
# atau
mv Agustus_2025.csv contribution/pengeluaran/
```

### Langkah 5: Commit

```bash
# Stage file
git add contribution/

# Commit dengan pesan deskriptif
git commit -m "Menambahkan data lapangan usaha Agustus 2025

- Total 35 kategori terisi
- Fokus region Sidoarjo
- Sumber dari 12 media lokal terverifikasi"

# Push ke GitHub
git push origin kontribusi-agustus-2025
```

### Langkah 6: Buat Pull Request

1. Buka repositori fork di GitHub
2. Akan muncul notifikasi "Compare & pull request"
3. Klik tombol tersebut
4. Isi deskripsi Pull Request:

```markdown
## Informasi Kontribusi

**Periode:** Agustus 2025
**Kategori:** Lapangan Usaha
**Jumlah Entri Terisi:** 35 dari 55 kategori

## Detail

- Fokus berita: Kabupaten Sidoarjo
- Sumber media: 12 media lokal dan nasional terverifikasi
- Total berita dirangkum: 48 artikel
- Distribusi sentiment: 25 Positif, 8 Negatif, 2 Kosong

## Verifikasi

- Format CSV UTF-8: Ya
- Penamaan file sesuai: Ya
- Semua URL dapat diakses: Ya
- Tanggal sesuai bulan: Ya
- Tidak ada hoaks: Ya
- Mengikuti kode etik: Ya
```

5. Klik "Create pull request"

### Langkah 7: Menunggu Review

- Tim akan melakukan review dalam 3-7 hari kerja
- Periksa notifikasi untuk feedback
- Jika ada permintaan revisi, lakukan perbaikan dan push ulang
- File akan dimerge setelah approved

---

## PROSES REVIEW

### Timeline

| Tahap | Durasi | Keterangan |
|-------|--------|------------|
| Auto-check | 1 jam | Validasi format file |
| Manual review | 3-7 hari | Pengecekan konten dan sumber |
| Feedback | 1-2 hari | Notifikasi hasil review |
| Revisi | 7 hari | Waktu untuk perbaikan |
| Approval | 1-2 hari | Merge ke database utama |

### Kriteria Review

Tim akan memeriksa:
- Format dan struktur file CSV
- Kualitas dan kredibilitas sumber berita
- Kesesuaian tanggal dengan periode file
- Objektifitas ringkasan dan analisis sentiment
- Kepatuhan terhadap kode etik

### Hasil Review

**Approved:**
- Langsung dimerge ke folder `data/`
- Notifikasi akan dikirim

**Revision Requested:**
- Daftar perbaikan akan diberikan di komentar
- Lakukan revisi dan push ulang
- Review ulang dalam 1-3 hari

**Rejected:**
- Penjelasan alasan penolakan
- Dapat mengajukan ulang setelah perbaikan menyeluruh

---

## TIPS DAN BEST PRACTICES

### Efisiensi Kerja
- Kumpulkan berita secara berkala, jangan tunggu akhir bulan
- Gunakan Google Alerts untuk tracking berita harian
- Bookmark media lokal favorit
- Buat draft di Google Spreadsheet untuk kolaborasi

### Kualitas Data
- Validasi sendiri sebelum submit
- Minta peer review dari rekan
- Gunakan spell checker
- Cross-check data dengan sumber lain

### Penulisan
- Gunakan kalimat aktif dan jelas
- Hindari jargon tanpa penjelasan
- Sertakan konteks yang memadai
- Pisahkan fakta dari interpretasi

---

## KONTAK

Jika mengalami kesulitan atau memiliki pertanyaan:

- **Email:** cs@dashfena.bps.go.id
- **GitHub Issues:** [Laporkan masalah teknis](https://github.com/fbrianzy/database-fenomena/issues)
- **GitHub Discussions:** [Diskusi umum](https://github.com/fbrianzy/database-fenomena/discussions)

---

Terima kasih atas kontribusi Anda dalam memperkaya Database Fenomena BPS Sidoarjo.

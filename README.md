# DATABASE FENOMENA - DASHFENA

Repositori ini merupakan **sumber data utama** untuk aplikasi web [Dashfena](https://github.com/fbrianzy/dashfena) - Dashboard Fenomena BPS Kabupaten Sidoarjo. Repositori ini menyimpan dan mengelola data fenomena ekonomi, sosial, dan pembangunan dalam format CSV yang dikurasi dari berbagai sumber berita terpercaya.

## TENTANG REPOSITORI

### Fungsi Utama
- **Penyimpanan Data**: Basis data fenomena berita tersentralisasi dalam format CSV
- **Integrasi Otomatis**: Data secara otomatis dibaca oleh aplikasi Dashfena untuk visualisasi
- **Kontribusi Terbuka**: Memungkinkan kontribusi data dari masyarakat dengan standar kualitas tinggi
- **Versi Kontrol**: Melacak perubahan dan riwayat data dengan sistem Git

### Cakupan Data
- **Wilayah**: Kabupaten Sidoarjo, Jawa Timur
- **Kategori**: 
  - Lapangan Usaha (sektor produksi/industri)
  - Pengeluaran (konsumsi rumah tangga)
- **Periode**: Data bulanan sejak [tahun mulai]
- **Sumber**: Media massa terpercaya dan terverifikasi

---

## STRUKTUR DIREKTORI

```
database-fenomena/
├── data/                          # Data CSV yang telah diverifikasi
│   ├── lapangan_usaha/
│   │   ├── Agustus_2025.csv
│   │   ├── September_2025.csv
│   │   └── ...
│   └── pengeluaran/
│       ├── Agustus_2025.csv
│       ├── September_2025.csv
│       └── ...
├── contribution/                  # Folder untuk kontribusi data baru
│   ├── lapangan_usaha/
│   └── pengeluaran/
├── templates/                     # Template CSV untuk kontributor
│   ├── lapangan_usaha.csv
│   └── pengeluaran.csv
├── README.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
└── SECURITY.md
```

---

## KONTRIBUSI DATA

Kami membuka kesempatan bagi masyarakat untuk berkontribusi memperkaya database fenomena. Kontribusi Anda sangat berarti untuk meningkatkan kualitas analisis dan monitoring ekonomi daerah.

### Panduan Singkat

#### 1. Format File
- **Hanya file CSV** (Comma-Separated Values)
- Encoding: UTF-8
- Disarankan mengerjakan di Excel/Google Spreadsheet, lalu simpan sebagai CSV

#### 2. Penamaan File
Format: `{Nama_Bulan}_{Tahun}.csv`

**Contoh benar:**
- ✅ `Agustus_2025.csv`
- ✅ `September_2025.csv`
- ✅ `Januari_2026.csv`

**Contoh salah:**
- ❌ `agustus_2025.csv` (huruf kecil)
- ❌ `08-2025.csv` (format angka)
- ❌ `Agustus 2025.csv` (ada spasi)

#### 3. Penempatan File
Tempatkan file kontribusi di folder yang sesuai:
```
contribution/lapangan_usaha/Agustus_2025.csv
contribution/pengeluaran/Agustus_2025.csv
```

---

## FORMAT DATA CSV

### Struktur Kolom

| No | Nama Kolom | Tipe | Wajib | Keterangan |
|----|------------|------|-------|------------|
| 1 | Kategori | Text | Ya | Nama sektor/subsektor (sesuai template) |
| 2 | Url Berita | Text | Kondisional* | Link sumber berita |
| 3 | Tanggal | Text | Kondisional* | Tanggal publikasi berita |
| 4 | Ringkasan Fenomena | Text | Kondisional* | Ringkasan objektif minimal 50 kata |
| 5 | Sentiment | Text | Ya | "Positif", "Negatif", atau "Kosong" |
| 6 | Alasan | Text | Kondisional* | Penjelasan analitis minimal 30 kata |

*Kondisional: Wajib diisi jika Sentiment bukan "Kosong"

### Aturan Format Detail

#### 1. Url Berita
**Format pemisah:** Koma diikuti spasi `, `

**Contoh:**
```
https://radarsidoarjo.jawapos.com/berita1
https://detik.com/jatim/berita1, https://kompas.com/berita2
https://antaranews.com/berita1, https://tempo.co/berita2, https://cnbcindonesia.com/berita3
```

**Aturan:**
- Maksimal 5 sumber per entri
- Harus menggunakan protokol lengkap (https://)
- Link harus dapat diakses dan tidak rusak

#### 2. Tanggal
**Format pemisah:** Titik koma diikuti spasi `; `

**Format penulisan:** `DD Bulan` (tanpa tahun)

**Contoh:**
```
15 Agustus
1 Agustus; 20 Agustus
5 Agustus; 12 Agustus; 28 Agustus
```

**Aturan:**
- Tanggal HARUS sesuai dengan bulan file CSV
- Nama bulan harus ditulis lengkap (bukan angka)
- Huruf pertama bulan kapital
- Tidak boleh ada tanggal dari bulan lain

#### 3. Sentiment
**Hanya 3 pilihan yang valid:**

| Sentiment | Kapan Digunakan | Contoh Kasus |
|-----------|-----------------|--------------|
| **Positif** | Berita menunjukkan perkembangan baik, peningkatan, keberhasilan | Kenaikan produksi, investasi baru, penghargaan |
| **Negatif** | Berita menunjukkan masalah, penurunan, kerugian | Penurunan penjualan, PHK, kecelakaan |
| **Kosong** | Tidak ada berita yang ditemukan untuk kategori tersebut | Tidak ditemukan berita relevan di wilayah prioritas |

**Aturan Penulisan:**
- ✅ `Positif` (P kapital)
- ✅ `Negatif` (N kapital)
- ✅ `Kosong` (K kapital)
- ❌ `positif`, `POSITIF`, `Netral`, `kosong` (tidak valid)

**Penting:** Tidak ada opsi "Netral". Jika tidak ada data, gunakan "Kosong".

#### 4. Ketentuan "Kosong"

Gunakan sentiment "Kosong" dengan aturan berikut:

**Prioritas Pencarian Berita:**
1. **Sidoarjo** (prioritas utama)
2. Surabaya (jika tidak ada di Sidoarjo)
3. Jawa Timur (jika tidak ada di Surabaya)
4. Indonesia (jika tidak ada di Jawa Timur)

**Batasan Region:**
- **WAJIB** prioritaskan berita yang terjadi di Kabupaten Sidoarjo
- Jika benar-benar tidak ada berita Sidoarjo, baru gunakan Surabaya
- Jika masih tidak ada, baru perluas ke Jawa Timur
- Indonesia hanya digunakan sebagai opsi terakhir

**Kapan mengisi "Kosong":**
- Sudah melakukan pencarian menyeluruh di semua prioritas region
- Tidak menemukan berita relevan untuk kategori tersebut di bulan yang dimaksud
- Berita yang ditemukan tidak memenuhi standar kredibilitas

**Cara mengisi baris "Kosong":**
```csv
Kategori,Url Berita,Tanggal,Ringkasan Fenomena,Sentiment,Alasan
Perkebunan Semusim,,,,Kosong,
```
Atau:
```csv
Kategori,Url Berita,Tanggal,Ringkasan Fenomena,Sentiment,Alasan
Perkebunan Semusim,,,,,
```

### Contoh Data Lengkap

```csv
Kategori,Url Berita,Tanggal,Ringkasan Fenomena,Sentiment,Alasan
Tanaman Pangan,"https://radarsidoarjo.jawapos.com/berita1, https://antaranews.com/berita2","15 Agustus; 20 Agustus","Dinas Pangan dan Pertanian Kabupaten Sidoarjo menggelar Sinkronisasi dan Koordinasi Program Ketahanan Pangan 2025. Acara ini dihadiri oleh pejabat tinggi daerah dan bertujuan meningkatkan ketersediaan pangan yang beragam, bergizi, dan aman. Program ini mendukung misi Asta Cita yaitu swasembada pangan melalui optimalisasi dana desa.",Positif,"Acara koordinasi ketahanan pangan menunjukkan komitmen pemerintah daerah dalam mewujudkan swasembada pangan. Dukungan dari berbagai pihak termasuk perbankan menunjukkan pendekatan holistik yang dapat meningkatkan keberhasilan program."
Perkebunan Semusim,,,,Kosong,
Tanaman Hortikultura Semusim,https://radarsidoarjo.jawapos.com/berita3,24 Agustus,"Stok pupuk subsidi di Sidoarjo 2025 dipastikan aman hingga akhir tahun dengan alokasi dana Rp 12,4 triliun dari pemerintah pusat. Data BPKP menunjukkan ketersediaan pupuk mencukupi untuk kebutuhan petani setempat.",Positif,"Ketersediaan stok pupuk subsidi yang aman menunjukkan kesiapan pemerintah dalam mendukung sektor pertanian. Hal ini berdampak positif pada produktivitas pertanian dan stabilitas harga pangan di Sidoarjo."
```

---

## STANDAR SUMBER BERITA

### Prioritas Region (WAJIB DIIKUTI)

```
1. SIDOARJO (UTAMA) ⭐
   └─ Jika tidak ada ↓
2. Surabaya
   └─ Jika tidak ada ↓
3. Jawa Timur
   └─ Jika tidak ada ↓
4. Indonesia (opsi terakhir)
```

**Contoh Implementasi:**

❌ **SALAH** - Langsung menggunakan berita nasional:
```
Kategori: Industri Makanan
Url: https://kompas.com/ekonomi/industri-makanan-indonesia-tumbuh
Region: Indonesia (Padahal ada berita Sidoarjo)
```

✅ **BENAR** - Prioritaskan Sidoarjo:
```
Kategori: Industri Makanan
Url: https://radarsidoarjo.jawapos.com/industri-makanan-sidoarjo
Region: Sidoarjo
```

### Sumber Media Terpercaya

**✅ DIPERBOLEHKAN:**

**Kategori 1: Media Lokal Sidoarjo/Surabaya (PRIORITAS)**
- Radar Sidoarjo (radarsidoarjo.jawapos.com)
- Jawa Pos Radar Surabaya
- Surya.co.id
- Memo X
- Berita Jatim

**Kategori 2: Media Nasional Terverifikasi**
- Kompas, Tempo, Detik, Liputan6
- CNN Indonesia, CNBC Indonesia
- Antara News, Bisnis Indonesia
- Kontan, Katadata

**Kategori 3: Website Pemerintah**
- Semua domain .go.id
- sidoarjokab.go.id
- bps.go.id
- kemenkeu.go.id

**❌ TIDAK DIPERBOLEHKAN:**
- Blog pribadi atau website non-verifikasi
- Media sosial (Facebook, Twitter, Instagram, TikTok)
- Forum atau platform user-generated content
- Website yang tidak jelas kredibilitasnya
- Sumber yang tidak dapat diakses

### Verifikasi Tanggal

**ATURAN KETAT:**
- Tanggal berita **HARUS 100% sesuai** dengan bulan file CSV
- **TIDAK BOLEH** sedikitpun lebih atau kurang dari bulan yang diambil
- Periksa tanggal publikasi di artikel (biasanya di bagian atas/bawah artikel)

**Contoh:**

File: `Agustus_2025.csv`
- ✅ Berita tanggal 1-31 Agustus 2025: **VALID**
- ❌ Berita tanggal 31 Juli 2025: **TIDAK VALID**
- ❌ Berita tanggal 1 September 2025: **TIDAK VALID**

### Verifikasi Anti-Hoaks

**WAJIB DIPASTIKAN:**
1. Media terdaftar di Dewan Pers (cek: dewanpers.or.id)
2. Artikel memiliki 5W+1H lengkap
3. Ada nama penulis atau kontributor
4. Informasi dapat di-cross-check dengan sumber lain
5. Tidak ada red flag: clickbait, sensasional, atau provokatif

**Tools Verifikasi (Opsional tapi Direkomendasikan):**
- turnbackhoax.id
- cekfakta.com
- kominfo.go.id (info hoaks)

---

## KODE ETIK KONTRIBUTOR

### Berdasarkan Kode Etik Kementerian Komunikasi dan Digital

Kontributor wajib:

1. **Menjunjung Kebenaran dan Akurasi**
   - Hanya menggunakan informasi yang dapat diverifikasi
   - Tidak memanipulasi atau mengubah fakta
   - Mencantumkan sumber dengan jelas dan akurat

2. **Menolak Hoaks dan Misinformasi**
   - Melakukan fact-checking sebelum memasukkan data
   - Tidak menyebarkan informasi yang belum terverifikasi
   - Melaporkan jika menemukan informasi yang mencurigakan

3. **Menghormati Privasi dan Data Pribadi**
   - Tidak mencantumkan informasi pribadi yang sensitif
   - Mengikuti prinsip perlindungan data
   - Menghormati hak privasi individu dalam berita

4. **Bertanggung Jawab**
   - Siap mempertanggungjawabkan setiap data yang dikontribusikan
   - Bersedia melakukan revisi jika ada kesalahan
   - Transparan dalam proses pengumpulan data

### Berdasarkan Kode Etik Badan Pusat Statistik

Kontributor wajib:

1. **Menjaga Objektivitas**
   - Tidak memasukkan bias pribadi dalam analisis sentimen
   - Menghindari interpretasi subjektif
   - Fokus pada fakta, bukan opini

2. **Memastikan Integritas Data**
   - Data harus valid dan dapat dipertanggungjawabkan
   - Tidak melakukan fabrikasi atau pemalsuan data
   - Konsisten dalam metodologi pengumpulan

3. **Profesionalisme**
   - Menggunakan bahasa Indonesia baku dan profesional
   - Menjaga kualitas setiap entri data
   - Mengikuti standar dan prosedur yang ditetapkan

4. **Kerahasiaan dan Keamanan**
   - Tidak menyalahgunakan akses ke repositori
   - Melindungi integritas database
   - Melaporkan jika menemukan celah keamanan

### Sanksi Pelanggaran

Pelanggaran kode etik dapat mengakibatkan:
- ⚠️ Peringatan pertama: Kontribusi ditolak dengan penjelasan
- ⚠️⚠️ Peringatan kedua: Banned sementara (1 bulan)
- 🚫 Pelanggaran berulang atau berat: Banned permanen

---

## PROSES KONTRIBUSI

### Langkah-Langkah

1. **Fork repositori** ini ke akun GitHub Anda
2. **Clone** ke komputer lokal
3. **Download template** dari folder `templates/`
4. **Isi data** sesuai standar (gunakan Excel/Spreadsheet)
5. **Simpan sebagai CSV** dengan format UTF-8
6. **Tempatkan file** di folder `contribution/`
7. **Commit dan push** ke repositori Anda
8. **Buat Pull Request** dengan deskripsi jelas
9. **Tunggu review** dari tim (3-7 hari kerja)
10. **Revisi** jika diperlukan
11. **Merge** setelah approved

### Timeline Review

| Tahap | Waktu | Keterangan |
|-------|-------|------------|
| Auto-check format | 1 jam | Validasi otomatis struktur file |
| Manual review | 3-7 hari | Tim memeriksa konten dan sumber |
| Feedback | 1-2 hari | Notifikasi hasil review |
| Revisi | 7 hari | Waktu untuk perbaikan |
| Final approval | 1-2 hari | Merge ke database utama |

### Status Pull Request

- 🟢 **Approved**: Langsung dimerge
- 🟡 **Revision Requested**: Perlu perbaikan (lihat komentar)
- 🔴 **Rejected**: Tidak memenuhi standar

---

## TOOLS DAN BANTUAN

### Template CSV
Download template kosong:
- [Template Lapangan Usaha](templates/lapangan_usaha.csv)
- [Template Pengeluaran](templates/pengeluaran.csv)

### Dokumentasi Lengkap
- [Panduan Kontribusi Detail](CONTRIBUTING.md)
- [Kode Etik](CODE_OF_CONDUCT.md)
- [Kebijakan Keamanan](SECURITY.md)

### Kontak Bantuan
- **Email**: database@dashfena.bps.go.id
- **GitHub Issues**: [Laporkan masalah atau pertanyaan](https://github.com/fbrianzy/database-fenomena/issues)
- **Diskusi**: [GitHub Discussions](https://github.com/fbrianzy/database-fenomena/discussions)

---

## FAQ (Frequently Asked Questions)

**Q: Berapa banyak data yang harus saya kontribusikan?**  
A: Minimal 5 kategori terisi untuk satu bulan. Semakin banyak semakin baik, namun kualitas lebih penting dari kuantitas.

**Q: Bagaimana jika tidak menemukan berita untuk kategori tertentu di Sidoarjo?**  
A: Ikuti prioritas region: Sidoarjo → Surabaya → Jawa Timur → Indonesia. Jika tetap tidak ada, isi dengan sentiment "Kosong".

**Q: Bolehkah menggunakan berita yang sama dengan kontributor lain?**  
A: Boleh, selama ringkasan dan analisis ditulis dengan kata-kata sendiri (tidak copy-paste).

**Q: Berapa lama waktu review?**  
A: Normalnya 3-7 hari kerja. Bisa lebih cepat jika kualitas data sangat baik.

**Q: Apakah ada reward untuk kontributor?**  
A: Saat ini belum ada reward finansial, namun kontributor aktif akan dicantumkan di halaman penghargaan dashboard.

---

## LISENSI DAN PENGGUNAAN

Data dalam repositori ini dilisensikan di bawah **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

**Anda bebas untuk:**
- Menggunakan data untuk analisis, penelitian, atau visualisasi
- Membagikan dan mendistribusikan data
- Mengadaptasi dan membangun berdasarkan data ini

**Dengan ketentuan:**
- Harus mencantumkan atribusi ke "Database Fenomena BPS Sidoarjo"
- Tidak boleh digunakan untuk tujuan komersial tanpa izin
- Penggunaan untuk publikasi akademis harus mencantumkan sitasi yang tepat

---

## SITASI

Jika menggunakan data ini untuk publikasi atau penelitian, gunakan format sitasi:

```
BPS Kabupaten Sidoarjo. (2025). Database Fenomena Ekonomi dan Sosial Kabupaten Sidoarjo. 
GitHub Repository. https://github.com/fbrianzy/database-fenomena
```

---

**Terima kasih atas kontribusi Anda dalam memperkaya data fenomena Kabupaten Sidoarjo!** 🙏

Untuk informasi lebih detail, silakan baca [CONTRIBUTING.md](CONTRIBUTING.md)

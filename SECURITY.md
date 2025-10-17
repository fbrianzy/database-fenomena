# KEBIJAKAN KEAMANAN DATA

Dokumen ini menetapkan kebijakan keamanan untuk Database Fenomena BPS Sidoarjo, khususnya terkait verifikasi sumber berita, pencegahan hoaks, dan aturan ketat penggunaan data.

## VERIFIKASI SUMBER BERITA

### Kriteria Sumber Terpercaya

#### Sumber yang Diperbolehkan

**1. Media Nasional Terverifikasi**

Media yang terdaftar di Dewan Pers RI dan memiliki track record kredibel:
- Kompas.com, Kompas.id
- Tempo.co, Tempo Interaktif
- Detik.com (semua kanal)
- Liputan6.com
- CNN Indonesia
- CNBC Indonesia
- Bisnis Indonesia
- Kontan.co.id
- Katadata.co.id

**2. Media Lokal Jawa Timur**

Media lokal dengan kredibilitas tinggi dan fokus pada Jawa Timur:
- Radar Sidoarjo (radarsidoarjo.jawapos.com)
- Jawa Pos (jawapos.com)
- Surya.co.id
- Tribun Jatim (jatim.tribunnews.com)
- Berita Jatim (beritajatim.com)
- Memo X (memox.co.id)

**3. Lembaga Berita Resmi**

- Antara News (antaranews.com)
- RRI (rri.co.id)
- TVRI (tvri.go.id)

**4. Website Pemerintah**

Semua website dengan domain resmi pemerintah:
- .go.id (semua kementerian dan lembaga)
- sidoarjokab.go.id
- bps.go.id
- kemenkeu.go.id
- kemendag.go.id
- esdm.go.id

**5. Media Khusus Industri**

Media yang fokus pada sektor tertentu dengan kredibilitas tinggi:
- Industry.co.id (industri manufaktur)
- Agroindonesia.co.id (pertanian)
- Maritim.go.id (kelautan dan perikanan)

#### Sumber yang Dilarang

**Dilarang Keras:**
- Blog pribadi atau website tidak terverifikasi
- Media sosial: Facebook, Twitter, Instagram, TikTok, WhatsApp
- Forum online: Kaskus, Reddit, Quora
- Platform user-generated content tanpa kurasi editorial
- Website yang masuk daftar penyebar hoaks Kominfo
- Sumber yang tidak dapat diakses atau link rusak
- Screenshot tanpa sumber asli yang dapat diverifikasi

### Prosedur Verifikasi Wajib

Setiap berita harus melalui tahapan verifikasi berikut:

#### Tahap 1: Verifikasi Sumber Media

**Checklist:**
- Media terdaftar di Dewan Pers (cek: dewanpers.or.id)
- Website memiliki halaman "Tentang Kami" atau "Redaksi" yang jelas
- Memiliki kontak redaksi yang dapat dihubungi
- Memiliki struktur organisasi editorial yang jelas
- Tidak masuk daftar media penyebar hoaks

**Tools Verifikasi:**
- Database Dewan Pers: dewanpers.or.id
- Cek Hoaks Kominfo: kominfo.go.id/kategori/hoaks
- Daftar media terverifikasi: dewanpers.or.id/data/perusahaanpers

#### Tahap 2: Verifikasi Konten Berita

**Checklist:**
- Artikel memiliki 5W+1H lengkap (Who, What, When, Where, Why, How)
- Ada nama penulis atau kontributor yang jelas
- Tanggal publikasi tercantum dengan jelas
- Terdapat narasumber yang dapat diidentifikasi
- Data atau statistik disertai sumbernya
- Tidak menggunakan bahasa sensasional atau clickbait

**Red Flags yang Harus Dihindari:**
- Judul tidak sesuai isi (clickbait)
- Tidak ada nama penulis
- Banyak typo atau tata bahasa buruk
- Informasi tidak lengkap atau samar
- Bahasa provokatif atau bias ekstrem
- Tidak ada tanggal publikasi
- Sumber data tidak jelas

#### Tahap 3: Verifikasi Tanggal

**Aturan Ketat:**
- Tanggal publikasi harus 100% sesuai dengan bulan file CSV
- Toleransi nol untuk tanggal di luar periode
- Verifikasi tanggal dari metadata artikel atau footer
- Jika tanggal tidak jelas, berita tidak boleh digunakan

**Contoh Pengecekan:**
```
File: Agustus_2025.csv
Berita Valid: 1-31 Agustus 2025
Berita Tidak Valid: 31 Juli 2025, 1 September 2025
```

#### Tahap 4: Cross-Check dengan Sumber Lain

**Prosedur:**
- Cari berita serupa dari minimal 1 media lain
- Bandingkan fakta dan angka yang dilaporkan
- Pastikan konsistensi informasi antar sumber
- Jika ada perbedaan signifikan, gunakan sumber yang lebih kredibel

**Tools Cross-Check:**
- Google News dengan filter tanggal
- Search engine dengan kata kunci spesifik
- Database berita online

### Tools Verifikasi Hoaks

Gunakan tools berikut untuk memverifikasi kebenaran berita:

**1. Cek Fakta Indonesia**
- Website: cekfakta.com
- Jaringan media yang melakukan fact-checking
- Database hoaks yang sudah terverifikasi

**2. Turn Back Hoax**
- Website: turnbackhoax.id
- Forum anti-hoaks dengan database lengkap
- Verifikasi crowdsourced dengan moderasi ketat

**3. Kominfo Cek Hoaks**
- Website: kominfo.go.id/kategori/hoaks
- Database resmi hoaks dari pemerintah
- Update berkala tentang hoaks yang beredar

**4. Mafindo (Masyarakat Anti Fitnah Indonesia)**
- Website: mafindo.or.id
- Organisasi independen fact-checker
- Partner Facebook dan Google untuk fact-checking

**5. Google Fact Check Explorer**
- Website: toolbox.google.com/factcheck/explorer
- Database global hasil fact-checking
- Filter berdasarkan region dan topik

---

## PENCEGAHAN HOAKS

### Definisi Hoaks

Hoaks adalah informasi yang tidak benar, menyesatkan, atau direkayasa dengan tujuan tertentu yang merugikan. Kategori hoaks meliputi:

**1. Fabricated Content (Konten Palsu)**
- Informasi sepenuhnya dibuat-buat
- Tidak ada dasar fakta sama sekali
- Dibuat dengan tujuan menyesatkan

**2. Manipulated Content (Konten Dimanipulasi)**
- Informasi asli yang diubah atau diedit
- Gambar atau video yang dipalsukan
- Data yang dimanipulasi untuk mendukung narasi tertentu

**3. Misleading Content (Konten Menyesatkan)**
- Informasi yang diambil di luar konteks
- Judul yang tidak sesuai isi
- Interpretasi yang menyimpang dari fakta

**4. False Context (Konteks Keliru)**
- Informasi asli disajikan dalam konteks yang salah
- Berita lama dijadikan seolah baru
- Lokasi atau waktu kejadian diubah

**5. Imposter Content (Konten Penyamar)**
- Menggunakan nama media atau lembaga palsu
- Website yang meniru situs berita resmi
- Akun palsu yang mengatasnamakan tokoh atau institusi

### Indikator Hoaks

**Tanda-tanda umum berita hoaks:**

**Dari Sisi Sumber:**
- Website tidak memiliki "Tentang Kami" yang jelas
- Tidak ada kontak redaksi
- Domain mencurigakan (.tk, .ml, .ga, dll)
- Website baru dibuat (cek via whois.com)
- Meniru nama media terkenal dengan domain berbeda

**Dari Sisi Konten:**
- Judul sangat sensasional atau mengejutkan
- Bahasa provokatif dan emosional berlebihan
- Banyak kesalahan ejaan dan tata bahasa
- Tidak ada sumber atau narasumber jelas
- Menggunakan kata "VIRAL", "HEBOH", "MENGEJUTKAN" berlebihan
- Informasi tidak lengkap atau samar

**Dari Sisi Visual:**
- Gambar blur atau resolusi rendah
- Gambar tidak sesuai konteks berita
- Tanda-tanda editing yang jelas
- Metadata gambar mencurigakan (gunakan reverse image search)

### Langkah Pencegahan

**Untuk Kontributor:**

1. **Sebelum Memasukkan Data:**
   - Verifikasi sumber dengan tools yang disediakan
   - Cross-check dengan minimal satu sumber lain
   - Periksa tanggal publikasi dengan teliti
   - Cek apakah berita pernah dibantah (cek di cekfakta.com)

2. **Saat Menganalisis:**
   - Pisahkan fakta dari opini
   - Jangan terpengaruh bias konfirmasi
   - Pertanyakan informasi yang terlalu bagus atau buruk untuk jadi kenyataan
   - Waspadai generalisasi berlebihan

3. **Sebelum Submit:**
   - Review ulang semua sumber yang digunakan
   - Pastikan tidak ada sumber yang mencurigakan
   - Dokumentasikan proses verifikasi (opsional tapi direkomendasikan)

**Untuk Reviewer:**

1. **Saat Menerima Kontribusi:**
   - Cek kredibilitas semua sumber yang dicantumkan
   - Verifikasi ketersediaan dan validitas link
   - Cross-check informasi dengan database internal
   - Gunakan tools verifikasi hoaks

2. **Jika Menemukan Indikasi Hoaks:**
   - Tolak kontribusi dengan penjelasan detail
   - Beri feedback konstruktif kepada kontributor
   - Dokumentasikan kasus untuk referensi
   - Laporkan ke Kominfo jika perlu

---

## ATURAN KETAT PENGGUNAAN DATA

### Batasan Tanggal

**Aturan Absolut:**
- Tanggal berita HARUS 100% sesuai bulan file CSV
- Tidak ada toleransi untuk tanggal di luar periode
- Tidak boleh menggunakan berita yang diterbitkan di bulan sebelum atau sesudah
- Jika berita di-update, gunakan tanggal publikasi awal

**Sanksi Pelanggaran:**
- Penolakan otomatis untuk seluruh kontribusi
- Peringatan tertulis kepada kontributor
- Kontribusi ulang harus melalui review lebih ketat

### Batasan Region

**Hierarki Prioritas (Wajib Diikuti):**

```
1. SIDOARJO (Prioritas Mutlak)
   ↓
2. Surabaya
   ↓
3. Jawa Timur
   ↓
4. Indonesia
```

**Aturan Detail:**
- Berita Sidoarjo HARUS diprioritaskan
- Hanya gunakan berita luar Sidoarjo jika benar-benar tidak ada
- Berita nasional hanya untuk konteks pelengkap, bukan data utama
- Dokumentasikan upaya pencarian berita Sidoarjo

**Bukti Pencarian:**
Jika menggunakan berita luar Sidoarjo, siapkan bukti bahwa sudah mencari berita Sidoarjo:
- Minimal 5 kata kunci berbeda
- Minimal 3 media lokal yang dicek
- Screenshot hasil pencarian (opsional)

### Batasan Sentiment

**Aturan Ketat:**
- Hanya 3 pilihan: `Positif`, `Negatif`, `Kosong`
- Tidak ada opsi lain (tidak boleh `Netral`, `Campuran`, dll)
- Case-sensitive: huruf pertama kapital
- Jika ragu antara Positif dan Negatif, tentukan berdasarkan dampak dominan

### Larangan Mutlak

**Dilarang Keras:**
- Menggunakan berita hoaks yang sudah terverifikasi
- Memalsukan tanggal atau sumber berita
- Plagiarisme atau copy-paste langsung dari artikel
- Memasukkan opini pribadi sebagai fakta
- Menggunakan sumber dari media sosial
- Mencantumkan data pribadi sensitif
- Memanipulasi sentiment untuk tujuan tertentu

**Konsekuensi:**
- Banned permanen dari repositori
- Pelaporan ke pihak berwenang jika terbukti sengaja menyebarkan hoaks
- Pencabutan seluruh kontribusi sebelumnya

---

## PELAPORAN KERENTANAN KEAMANAN

### Jenis Kerentanan

Laporkan segera jika menemukan:
- Berita hoaks yang lolos verifikasi
- Sumber tidak kredibel yang masuk database
- Data yang dimanipulasi atau dipalsukan
- Kesalahan sistemik dalam proses verifikasi
- Celah dalam prosedur keamanan

### Cara Melaporkan

**Email:** security@dashfena.bps.go.id  
**Subject:** [SECURITY] - Deskripsi Singkat

**Informasi yang Diperlukan:**
- Deskripsi detail masalah keamanan
- Lokasi data yang bermasalah (file, baris, kolom)
- Bukti pendukung (screenshot, link verifikasi)
- Dampak potensial
- Saran perbaikan (jika ada)

**Timeline Respons:**
- Acknowledgment: 24 jam
- Investigasi awal: 3 hari kerja
- Tindakan perbaikan: 7 hari kerja
- Notifikasi penyelesaian: 1 hari setelah perbaikan

### Jaminan Pelapor

- Identitas pelapor dijaga kerahasiaannya
- Tidak ada sanksi untuk pelapor yang beritikad baik
- Apresiasi untuk pelapor yang membantu meningkatkan keamanan
- Pelapor akan diinformasikan tentang tindakan yang diambil

---

## AUDIT DAN MONITORING

### Audit Berkala

Database akan diaudit secara berkala untuk memastikan:
- Semua sumber masih kredibel dan dapat diakses
- Tidak ada berita hoaks yang lolos verifikasi
- Konsistensi sentiment dengan isi berita
- Kepatuhan terhadap standar tanggal dan region

**Frekuensi Audit:**
- Audit ringan: Setiap bulan
- Audit menyeluruh: Setiap 6 bulan
- Audit khusus: Jika ada laporan masalah

### Monitoring Aktif

Tim pengelola akan:
- Memantau perkembangan status kredibilitas media
- Update daftar sumber terpercaya secara berkala
- Tracking berita yang dibantah atau dikoreksi
- Monitoring tools verifikasi hoaks untuk update

---

## PEMBARUAN KEBIJAKAN

Kebijakan keamanan ini akan diperbarui sesuai dengan:
- Perkembangan regulasi pemerintah
- Perubahan landscape media dan teknologi
- Pembelajaran dari kasus-kasus yang terjadi
- Feedback dari kontributor dan pengguna

**Notifikasi Pembaruan:**
- Semua kontributor aktif akan diberi notifikasi
- Perubahan signifikan akan diumumkan di README
- Riwayat perubahan didokumentasikan

---

**Versi:** 1.0  
**Tanggal Berlaku:** 1 Januari 2025  
**Revisi Terakhir:** -

**Database Fenomena BPS Sidoarjo**  
Komitmen kami: Data akurat, terverifikasi, dan bebas hoaks.

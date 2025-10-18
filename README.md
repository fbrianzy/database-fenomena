# DATABASE FENOMENA BPS SIDOARJO

Repositori ini merupakan sumber data utama untuk aplikasi web [Dashfena](https://github.com/fbrianzy/dashfena) - Dashboard Fenomena BPS Kabupaten Sidoarjo. Database ini menyimpan dan mengelola data fenomena ekonomi, sosial, dan pembangunan dalam format CSV yang dikurasi dari berbagai sumber berita terpercaya.

## TENTANG REPOSITORI

### Fungsi
- Penyimpanan data fenomena berita tersentralisasi dalam format CSV
- Integrasi otomatis dengan aplikasi Dashfena untuk visualisasi data
- Platform kontribusi terbuka dengan standar kualitas tinggi
- Sistem kontrol versi untuk pelacakan perubahan data

### Cakupan
- **Wilayah**: Kabupaten Sidoarjo, Jawa Timur
- **Kategori**: Lapangan Usaha (sektor produksi) dan Pengeluaran (konsumsi rumah tangga)
- **Periode**: Data bulanan dengan update berkala
- **Sumber**: Media massa terverifikasi dan kredibel

## STRUKTUR REPOSITORI

```
database-fenomena/
├── data/                      # Data CSV terverifikasi
│   ├── lapangan_usaha/
│   └── pengeluaran/
├── contribution/              # Folder kontribusi publik
│   ├── lapangan_usaha/
│   └── pengeluaran/
├── templates/                 # Template CSV
│   ├── lapangan_usaha.csv
│   └── pengeluaran.csv
├── LICENSE                    # by MIT License
├── README.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
└── SECURITY.md
```

## KONTRIBUSI

Kami membuka kesempatan bagi masyarakat untuk berkontribusi memperkaya database. Kontribusi dapat berupa penambahan data fenomena berita bulanan sesuai kategori yang tersedia.

### Ringkasan Persyaratan

- File harus dalam format CSV dengan encoding UTF-8
- Penamaan file: `{Nama_Bulan}_{Tahun}.csv` (contoh: `Agustus_2025.csv`)
- Tempatkan di folder `contribution/lapangan_usaha/` atau `contribution/pengeluaran/`
- Gunakan template yang tersedia di folder `templates/`
- Prioritaskan berita dari wilayah Sidoarjo
- Pastikan sumber berita terverifikasi dan tidak mengandung hoaks

### Format Data

| Kolom | Pemisah | Contoh |
|-------|---------|--------|
| Url Berita | `, ` (koma spasi) | `https://url1, https://url2` |
| Tanggal | `; ` (titik koma spasi) | `15 Agustus; 20 Agustus` |
| Sentiment | - | `Positif`, `Negatif`, atau `Kosong` |

### Prioritas Region

Pencarian berita mengikuti urutan prioritas:
1. **Sidoarjo** (utama)
2. Surabaya (jika tidak ada di Sidoarjo)
3. Jawa Timur (jika tidak ada di Surabaya)
4. Indonesia (opsi terakhir)

Gunakan sentiment `Kosong` jika tidak menemukan berita relevan setelah pencarian menyeluruh.

### Dokumentasi Lengkap

Untuk panduan detail, silakan baca:

- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Panduan lengkap kontribusi data, format, dan proses review
- **[SECURITY.md](SECURITY.md)** - Kebijakan verifikasi sumber dan pencegahan hoaks
- **[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)** - Kode etik berdasarkan standar Kominfo dan BPS

## PROSES REVIEW

1. Kontributor submit Pull Request ke folder `contribution/`
2. Validasi otomatis format file (1 jam)
3. Review manual oleh tim (3-7 hari kerja)
4. Feedback atau approval
5. Merge ke folder `data/` jika approved
6. Integrasi otomatis ke aplikasi Dashfena

## PENGGUNAAN DATA

Data dalam repositori ini dilisensikan di bawah **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

### Ketentuan Penggunaan
- Bebas digunakan untuk analisis, penelitian, dan visualisasi
- Wajib mencantumkan atribusi ke "Database Fenomena BPS Sidoarjo"
- Penggunaan komersial memerlukan izin tertulis
- Publikasi akademis harus mencantumkan sitasi yang tepat

### Sitasi
```
BPS Kabupaten Sidoarjo. (2025). Database Fenomena Ekonomi dan Sosial Kabupaten Sidoarjo. 
GitHub Repository. https://github.com/fbrianzy/database-fenomena
```

## KONTAK DAN DUKUNGAN

- **Email**: database@dashfena.bps.go.id
- **Issues**: [GitHub Issues](https://github.com/fbrianzy/database-fenomena/issues)
- **Diskusi**: [GitHub Discussions](https://github.com/fbrianzy/database-fenomena/discussions)

## LISENSI

Proyek ini dilisensikan di bawah [MIT License](LICENSE) untuk kode dan CC BY 4.0 untuk data.

---

**Database Fenomena BPS Sidoarjo** | Dikelola oleh BPS Kabupaten Sidoarjo

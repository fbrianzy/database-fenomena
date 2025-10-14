import pandas as pd
import re

url = "/content/Tim-UNESA_3515 Fenomena September.xlsx - Lapangan Usaha.csv"
df = pd.read_csv(url)

def clean_tanggal(text):
    text = str(text)
    # Ambil semua pola "25 Juli", "26 juli", dst.
    dates = re.findall(r'\d{1,2}\s+[JjFfMmAaSsOoNnDd]\w+', text)  # cocokkan dengan nama bulan
    # Kapitalisasi huruf pertama bulan agar konsisten
    dates = [d.title() for d in dates]
    return '; '.join(dates)

# Fungsi untuk membersihkan URL
def clean_urls(text):
    text = str(text)
    urls = re.findall(r'https?://[^\s,;]+', text)
    return ', '.join(urls)

df['Tanggal'] = df['Tanggal'].apply(clean_tanggal)
df['Url Berita'] = df['Url Berita'].apply(clean_urls)

df.to_csv("September.csv", index=False)
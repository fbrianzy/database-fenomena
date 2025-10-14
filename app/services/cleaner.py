import pandas as pd

try:
    from app.utils.phenomCleaner import clean_tanggal, clean_urls
except Exception:
    import re
    def clean_tanggal(text):
        text = str(text) if text is not None else ""
        dates = re.findall(r'\b\d{1,2}\s+[A-Za-zÀ-ÿ]+', text)
        return '; '.join([d.title() for d in dates])
    def clean_urls(text):
        text = str(text) if text is not None else ""
        urls = re.findall(r'https?://[^\s,;"]+', text)
        return ', '.join(urls)

def run_fenomena_cleaner(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "Tanggal" in df.columns:
        df["Tanggal"] = df["Tanggal"].apply(clean_tanggal)
    if "Url Berita" in df.columns:
        df["Url Berita"] = df["Url Berita"].apply(clean_urls)
    for col in [c for c in ["Kategori", "Ringkasan Fenomena", "Sentiment", "bulan"] if c in df.columns]:
        df[col] = df[col].astype(str).str.strip()
    if "bulan" in df.columns:
        df["bulan"] = df["bulan"].astype(str).str.title()
    return df
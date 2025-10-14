def filter_empty_data_for_trend(df, jenis_data="all"):
    if df.empty:
        return df

    if jenis_data != "all" and "jenis_data" in df.columns:
        if jenis_data == "lapangan_usaha":
            df = df[df["jenis_data"] == "Lapangan Usaha"]
        elif jenis_data == "pengeluaran":
            df = df[df["jenis_data"] == "Pengeluaran"]

    df_filtered = df.copy()

    if 'Ringkasan Fenomena' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['Ringkasan Fenomena'].notna()]
        df_filtered = df_filtered[df_filtered['Ringkasan Fenomena'].str.strip() != '']

    if 'Kategori' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['Kategori'].notna()]
        df_filtered = df_filtered[df_filtered['Kategori'].str.strip() != '']

    if 'Sentiment' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['Sentiment'].notna()]
        df_filtered = df_filtered[df_filtered['Sentiment'].str.strip() != '']
        valid_sentiment = ['Positif', 'Negatif']
        df_filtered = df_filtered[df_filtered['Sentiment'].isin(valid_sentiment)]

    if 'bulan' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['bulan'].notna()]
        df_filtered = df_filtered[df_filtered['bulan'].str.strip() != '']

    return df_filtered

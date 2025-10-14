import pandas as pd

def create_sample_data():
    import random
    months = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni']
    categories = ['Ekonomi', 'Sosial', 'Pendidikan', 'Kesehatan', 'Infrastruktur']
    sentiments = ['Positif', 'Negatif', 'Kosong']
    sample_data = []
    for i in range(50):
        sample_data.append({
            'bulan': random.choice(months),
            'Kategori': random.choice(categories),
            'Sentiment': random.choice(sentiments),
            'Ringkasan Fenomena': f'Sample fenomena {i+1} untuk testing aplikasi',
            'jenis_data': 'Sample Data'
        })
    return pd.DataFrame(sample_data)
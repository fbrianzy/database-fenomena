from app.utils.filterEmpty import *

def prepare_trend_data(df, jenis_data="all", filter_empty=False):
    if df.empty:
        return {
            'monthly_trend': [],
            'sentiment_distribution': {'Positif': 0, 'Negatif': 0, 'Kosong': 0},
            'category_breakdown': [],
            'top_positive_categories': [],
            'top_negative_categories': [],
            'statistics': {
                'total_data': 0,
                'total_raw_data': 0,
                'growth_rate': 0,
                'peak_month': 'N/A',
                'avg_daily': 0,
                'positive_sentiment_pct': 0
            }
        }

    df_raw = df.copy()

    if jenis_data != "all" and "jenis_data" in df.columns:
        if jenis_data == "lapangan_usaha":
            df = df[df["jenis_data"] == "Lapangan Usaha"]
            df_raw = df_raw[df_raw["jenis_data"] == "Lapangan Usaha"]
        elif jenis_data == "pengeluaran":
            df = df[df["jenis_data"] == "Pengeluaran"]
            df_raw = df_raw[df_raw["jenis_data"] == "Pengeluaran"]

    if filter_empty:
        df = filter_empty_data_for_trend(df, jenis_data)
        if df.empty:
            return {
                'monthly_trend': [],
                'sentiment_distribution': {'Positif': 0, 'Negatif': 0, 'Kosong': len(df_raw)},
                'category_breakdown': [],
                'top_positive_categories': [],
                'top_negative_categories': [],
                'statistics': {
                    'total_data': 0,
                    'total_raw_data': len(df_raw),
                    'growth_rate': 0,
                    'peak_month': 'N/A',
                    'avg_daily': 0,
                    'positive_sentiment_pct': 0
                }
            }

    # Monthly trend
    month_order = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
                   'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
    monthly_counts = df.groupby('bulan').size().to_dict() if 'bulan' in df.columns else {}
    monthly_trend = [{'month': m, 'count': monthly_counts.get(m, 0)} for m in month_order]

    # Sentiment distribution (hanya Sentiment)
    sentiment_counts = df['Sentiment'].value_counts().to_dict() if 'Sentiment' in df.columns else {}
    total_raw_records = len(df_raw)
    total_valid_records = len(df)
    kosong_count = total_raw_records - total_valid_records
    sentiment_distribution = {
        'Positif': sentiment_counts.get('Positif', 0),
        'Negatif': sentiment_counts.get('Negatif', 0),
        'Kosong': max(kosong_count, 0)
    }

    # Category breakdown & top categories
    top_positive_categories, top_negative_categories, category_breakdown = [], [], []
    category_col = 'Kategori' if 'Kategori' in df.columns else None
    if category_col and 'Sentiment' in df.columns:
        try:
            df_pos = df[df['Sentiment'] == 'Positif']
            df_neg = df[df['Sentiment'] == 'Negatif']
            if not df_pos.empty:
                pos_counts = df_pos[category_col].value_counts().head(8).to_dict()
                top_positive_categories = [{'category': str(k), 'count': int(v)} for k, v in pos_counts.items()]
            if not df_neg.empty:
                neg_counts = df_neg[category_col].value_counts().head(8).to_dict()
                top_negative_categories = [{'category': str(k), 'count': int(v)} for k, v in neg_counts.items()]
            all_counts = df[category_col].value_counts().head(10).to_dict()
            category_breakdown = [{'category': str(k), 'count': int(v)} for k, v in all_counts.items()]
        except Exception as e:
            print(f"Error processing category data: {e}")

    total_data = len(df)
    total_raw_data = len(df_raw)
    total_sentiments = df['Sentiment'].notna().sum() if 'Sentiment' in df.columns else 0
    positive_count = len(df[df['Sentiment'] == 'Positif']) if 'Sentiment' in df.columns else 0
    positive_sentiment_pct = round((positive_count / total_sentiments * 100), 1) if total_sentiments > 0 else 0

    monthly_values = list(monthly_counts.values())
    if len(monthly_values) >= 2:
        recent_avg = sum(monthly_values[-3:]) / min(3, len(monthly_values))
        earlier_avg = sum(monthly_values[:-3]) / max(1, len(monthly_values) - 3)
        growth_rate = round(((recent_avg - earlier_avg) / max(earlier_avg, 1)) * 100, 1)
    else:
        growth_rate = 0

    peak_month = max(monthly_counts, key=monthly_counts.get) if monthly_counts else 'N/A'
    avg_daily = int(round(total_data / 30, 0)) if total_data > 0 else 0

    statistics = {
        'total_data': total_data,
        'total_raw_data': total_raw_data,
        'growth_rate': growth_rate,
        'peak_month': peak_month,
        'avg_daily': avg_daily,
        'positive_sentiment_pct': positive_sentiment_pct
    }

    return {
        'monthly_trend': monthly_trend,
        'sentiment_distribution': sentiment_distribution,
        'category_breakdown': category_breakdown,
        'top_positive_categories': top_positive_categories,
        'top_negative_categories': top_negative_categories,
        'statistics': statistics
    }

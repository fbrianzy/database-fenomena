# === Month-Year parsing utilities ===
BULAN_ID = {
    "januari": "Januari", "februari": "Februari", "maret": "Maret", "april": "April",
    "mei": "Mei", "juni": "Juni", "juli": "Juli", "agustus": "Agustus",
    "september": "September", "oktober": "Oktober", "november": "November", "desember": "Desember"
}

MONTH_ORDER = ['Januari','Februari','Maret','April','Mei','Juni',
            'Juli','Agustus','September','Oktober','November','Desember']
MONTH_INDEX = {m: i+1 for i, m in enumerate(MONTH_ORDER)}
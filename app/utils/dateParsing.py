from app.config.date import *

def parse_bulan_tahun_from_filename(filename: str):
    base = filename.rsplit("/", 1)[-1].replace(".csv", "")
    parts = base.split("_")
    bulan = None
    tahun = None
    for part in parts:
        p = part.strip().lower()
        if p in BULAN_ID and bulan is None:
            bulan = BULAN_ID[p]
        elif p.isdigit() and len(p) == 4:
            tahun = p
    return bulan or base.title(), tahun

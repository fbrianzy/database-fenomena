# Struktur Folder Project

```
project_root/
│
├── app/
│   ├── __init__.py                 # Factory pattern untuk create_app()
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py             # Konfigurasi environment & constants
│   │
│   ├── middlewares/
│   │   ├── __init__.py
│   │   ├── auth.py                 # Login required, admin check
│   │   ├── csrf.py                 # CSRF protection middleware
│   │   └── rate_limit.py           # Rate limiting logic
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── dataframe.py            # Data models/schemas (jika perlu)
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── github_service.py       # GitHub API interactions
│   │   ├── data_service.py         # Load & process CSV data
│   │   ├── cache_service.py        # Caching logic
│   │   └── cleaner_service.py      # FenomenaCleaner logic
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── validators.py           # CSV validation, file checks
│   │   ├── date_utils.py           # Parsing bulan/tahun, formatting
│   │   ├── stats.py                # MoM calculations, statistics
│   │   └── helpers.py              # General helper functions
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py                 # Home, about routes
│   │   ├── fenomena.py             # /fenomena routes
│   │   ├── trend.py                # /trend routes
│   │   ├── api.py                  # API endpoints
│   │   └── admin/
│   │       ├── __init__.py
│   │       ├── auth.py             # Admin login/logout
│   │       ├── upload.py           # Admin upload
│   │       └── dashboard.py        # Admin home & diagnostics
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── fenomena.html
│   │   ├── trend.html
│   │   ├── about.html
│   │   └── admin/
│   │       ├── base_admin.html
│   │       ├── admin_login.html
│   │       ├── admin_home.html
│   │       └── admin_upload.html
│   │
│   └── static/
│       ├── css/
│       ├── js/
│       └── images/
│
├── tests/
│   ├── __init__.py
│   ├── test_services/
│   ├── test_utils/
│   └── test_routes/
│
├── .env                            # Environment variables
├── .env.example                    # Template untuk .env
├── .gitignore
├── requirements.txt
├── run.py                          # Entry point aplikasi
└── README.md
```

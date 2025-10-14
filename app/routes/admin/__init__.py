# app/routes/admin/__init__.py
from flask import Blueprint

# Inisialisasi blueprint utama untuk seluruh halaman dan API admin
bp = Blueprint("admin", __name__, url_prefix="/admin")

# Import semua sub-route agar otomatis terdaftar di blueprint
# (urutan import tidak terlalu penting, tapi yang umum lebih dulu)
from app.routes.admin import (
    home,             # /admin/
    envCheck,         # /admin/envcheck
    diagnostics,      # /admin/diagnostics
    cacheStatus,     # /admin/cache-status
    clearCache,      # /admin/clear-cache
    delFile,      # /admin/api/delete-file
    table,            # /admin/table
    updCell,      # /admin/api/update-cell
    updRow,       # /admin/api/update-row
    upload,           # /admin/upload
    login,            # /admin/login
    logout            # /admin/logout
)

# wsgi.py
import os
from app import create_app

# Gunakan config object kalau kamu punya (mis. "app.config.settings.ProdConfig")
# app = create_app("app.config.settings.BaseConfig")
app = create_app()

if __name__ == "__main__":
    # Mode dev/local run: flask run digantikan run langsung
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host=host, port=port, debug=debug)

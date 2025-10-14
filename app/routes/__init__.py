# app/routes/__init__.py
from app.routes.home import bp as home_bp
from app.routes.fenomena import bp as fenomena_bp
from app.routes.trend import bp as trend_bp
from app.routes.about import bp as about_bp
from app.routes.apiTrend import bp as api_trend_bp  # sudah punya prefix sendiri

ALL_BLUEPRINTS = [home_bp, fenomena_bp, trend_bp, about_bp, api_trend_bp]

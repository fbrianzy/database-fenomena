import os
from flask import Flask

def create_app(config_object: str | None = None) -> Flask:
    here = os.path.dirname(__file__)  # .../app
    templates_dir = os.path.join(here, "templates")
    static_dir = os.path.join(here, "static")

    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder=templates_dir,
        static_folder=static_dir,
    )

    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "dev-insecure-secret")
    app.config.setdefault("TEMPLATES_AUTO_RELOAD", True)

    if config_object:
        app.config.from_object(config_object)
    else:
        app.config.from_pyfile("config.py", silent=True)

    try:
        from app.middlewares.errors import register_error_handlers 
        register_error_handlers(app)
    except Exception:
        pass

    # Register blueprints publik
    from app.routes import ALL_BLUEPRINTS
    for bp in ALL_BLUEPRINTS:
        app.register_blueprint(bp)

    # Register blueprint admin (sub-routes)
    from app.routes.admin import bp as admin_bp
    app.register_blueprint(admin_bp)

    # (Opsional) Flush cache template waktu dev
    if app.debug:
        app.jinja_env.cache = {}

    # (Opsional) endpoint debug list template
    @app.get("/_debug/templates")
    def _list_templates():
        try:
            names = sorted(app.jinja_env.list_templates())
            return {"count": len(names), "templates": names}, 200
        except Exception as e:
            return {"error": str(e)}, 500

    return app

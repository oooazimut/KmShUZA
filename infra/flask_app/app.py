from flask import Flask

from domain import UseCases

from .auth.views import auth_bp
from .pr_info.views import info_bp


def create_flask_app():
    app = Flask(__name__)
    app.config["use_cases"] = UseCases()
    app.register_blueprint(auth_bp)
    app.register_blueprint(info_bp)
    return app


app = create_flask_app()

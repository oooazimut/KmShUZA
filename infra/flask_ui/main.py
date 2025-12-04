from flask import Flask

from .auth.views import auth_bp


def create_flask_ui():
    flask_ui = Flask(__name__)
    flask_ui.register_blueprint(auth_bp)
    return flask_ui

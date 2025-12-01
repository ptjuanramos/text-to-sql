from flask import Flask
# from .extensions import db
from .routes.app import app

def create_app():
    flask_app = Flask(__name__, template_folder="templates")
    # flaskApp = Flask(__name__)
    # app.config.from_object()

    # db.init_app(flaskApp)

    flask_app.register_blueprint(app)

    return flask_app
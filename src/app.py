from flask import Flask
from flask_migrate import Migrate

from src import consts, urls
from src.db import db


def create_app():
    app = Flask(__name__.split(".")[0])
    app.config["SQLALCHEMY_DATABASE_URI"] = consts.SQLALCHEMY_DATABASE_URI

    db.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db)

    app.register_blueprint(urls.views.mod)

    return app

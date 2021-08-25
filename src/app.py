from flask import Flask
from flask_migrate import Migrate

from src import consts, urls
from src.db import db


def create_app(test=False):
    app = Flask(__name__.split(".")[0])
    if test:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = consts.SQLALCHEMY_TEST_DATABASE_URI
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = consts.SQLALCHEMY_DATABASE_URI

    db.init_app(app)
    app.app_context().push()
    migrate = Migrate()
    migrate.init_app(app, db)

    app.register_blueprint(urls.views.mod)

    return app

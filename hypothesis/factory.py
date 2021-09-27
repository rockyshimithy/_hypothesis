import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from hypothesis.extensions import init_swagger

PKG_NAME = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]
db = SQLAlchemy()

# pylint: disable=import-outside-toplevel
def create_app(settings_override={}):
    app = Flask(PKG_NAME)
    app.config.from_object('hypothesis.settings.Configuration')

    db.init_app(app)

    init_swagger(app)

    from hypothesis.views import blueprint

    app.register_blueprint(blueprint)
    return app


app = create_app()
migrate = Migrate(app, db)

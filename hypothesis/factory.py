import os

from flask import Blueprint, Flask
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

    blueprint = Blueprint('api', __name__)

    from hypothesis.views import CustomerView, TransactionView

    blueprint.add_url_rule(
        '/customers/',
        view_func=CustomerView.as_view('customer'),
        methods=['GET', 'POST'],
    )
    blueprint.add_url_rule(
        '/transactions/',
        view_func=TransactionView.as_view('transaction'),
        methods=['GET', 'POST'],
    )

    app.register_blueprint(blueprint)
    return app


app = create_app()
migrate = Migrate(app, db)

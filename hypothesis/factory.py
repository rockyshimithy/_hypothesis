import os

from flask import Flask

from hypothesis.extensions import init_swagger

PKG_NAME = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]


# pylint: disable=import-outside-toplevel
def create_app():
    app = Flask(PKG_NAME)

    init_swagger(app)

    from hypothesis.views import blueprint

    app.register_blueprint(blueprint)
    return app

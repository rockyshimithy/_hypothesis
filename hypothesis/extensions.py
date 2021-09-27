from flasgger import Swagger

from hypothesis.settings import Configuration


def init_swagger(app):
    return Swagger(app, template=Configuration.SWAGGER_TEMPLATE)

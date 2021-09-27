"""
This module is used to create extensions, according to the recommendation
from the official flask docs for app factories:
https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/#factories-extensions
"""

from flasgger import Swagger

from hypothesis.settings import Configuration


def init_swagger(app):
    return Swagger(app, template=Configuration.SWAGGER_TEMPLATE)

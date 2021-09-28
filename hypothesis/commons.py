import os
from functools import lru_cache
from pathlib import Path

from flask import jsonify, request
from flask.views import MethodView


class BaseView(MethodView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = {}
        self.page = 1
        self.query_string = request.args.to_dict()
        self.status_code = 200

    def get(self):
        page = self.query_string.get('page')
        if isinstance(page, int):
            self.page = page

    def get_response(self):
        response = [
            self.schema.dump(obj)
            for obj in self.query.paginate(self.page, 20).items
        ]
        return self.response(response)

    def post(self):
        payload = request.get_json()
        self.data = self.schema.load(payload)

    def response(self, response):
        return jsonify(response), self.status_code


def get_version_file_path():
    root_path = Path().absolute()
    file_path = os.path.join(str(root_path), 'VERSION')

    if not os.path.exists(file_path):
        root_path = root_path.parent
        file_path = os.path.join(str(root_path), 'VERSION')

    return file_path


@lru_cache(maxsize=None)
def get_app_version():
    file_path = get_version_file_path()
    with open(file_path, 'r', encoding='utf-8') as version_file:
        return version_file.read().replace('\n', '')

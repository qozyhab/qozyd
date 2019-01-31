import json


class Bag(dict):
    def get_bool(self, key, default=None):
        try:
            values = self[key]

            return True if values[-1] in ("true", "1", "True") else False
        except KeyError:
            return default


class Request():
    def __init__(self, method, path, headers, get, request_body):
        self.method = method
        self.path = path
        self.headers = headers
        self.get = get
        self.request_body = request_body

        self.matched_path = None

    @property
    def request_json(self):
        return json.loads(self.request_body)

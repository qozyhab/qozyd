import json


class Bag(dict):
    def get_bool(self, key, default=None):
        try:
            value = self[key]

            if not isinstance(value, str):
                # if multiple arguments for specific key are given we'll get a list of values, we simply use the last one here
                value = value[-1]

            return True if value in ("true", "1", "True") else False
        except KeyError:
            return default

    def get_number(self, key, default=None):
        try:
            value = self[key]

            if not isinstance(value, str):
                # if multiple arguments for specific key are given we'll get a list of values, we simply use the last one here
                value = value[-1]
        except KeyError:
            return default

        try:
            return int(value)
        except ValueError:
            return float(value)


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

class HttpException(Exception):
    def __init__(self, status_code, data=None):
        super().__init__()

        self.status_code = status_code
        self.data = data


class NotFoundException(HttpException):
    def __init__(self, data="Not found"):
        super().__init__(404, data)

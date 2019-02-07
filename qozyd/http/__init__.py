import re
import urllib

from .request import Bag, Request

from qozyd.http.exceptions import HttpException, NotFoundException
from qozyd.utils.json import JsonEncoder


class Router():
    def __init__(self, routes):
        self.routes = routes

    def match(self, request):
        for route in self.routes:
            match = route.match(request)

            if match:
                return match

    def remove(self, route):
        self.routes.remove(route)

    def add(self, route):
        self.routes.append(route)


class Route():
    def __init__(self, path_regex, view, method=None, name=None, **kwargs):
        self.path_regex = re.compile(path_regex)
        self.method = method
        self.view = view
        self.name = name
        self.kwargs = kwargs

    def match(self, request):
        if self.method and request.method != self.method:
            return None

        matches = self.path_regex.match(request.path)

        if matches:
            return self, matches.groupdict(), matches.string[matches.start():matches.end()]


def http_server_handler(context):
    from http.server import BaseHTTPRequestHandler

    class HTTPRequestHandler(BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            pass

        def process(self, method):
            content_length = self.headers["content-length"]
            length = int(content_length) if content_length else 0

            request_body = self.rfile.read(length).decode()

            url = urllib.parse.urlparse(self.path)

            request = Request(method, url.path, dict(self.headers), Bag(urllib.parse.parse_qs(url.query)), request_body)

            try:
                response = context.handle(request)

                # send response status code
                self.send_response(response.status_code)

                # write headers
                headers = list(response.headers)
                for header, value in headers:
                    self.send_header(header, value)

                # add cors headers if needed
                if self.headers["Origin"]:
                    self.send_header("Access-Control-Expose-Headers", "Content-Type,Date,Content-Length,Authorization,X-Request-ID")
                    self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
                    self.send_header("Access-Control-Allow-Credentials", "true")

                self.end_headers()

                # write response body
                response.write(self.wfile)
            except HttpException as http_exception:
                self.process_http_exception(http_exception)
            except Exception as e:
                self.process_exception(e)
                return

        def process_http_exception(self, http_exception):
            self.send_response(http_exception.status_code)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            
            self.wfile.write(JsonEncoder().encode(http_exception.data).encode("utf-8"))

        def process_exception(self, exception):
            self.send_response(503)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            import traceback

            self.wfile.write(JsonEncoder().encode({
                "message": str(exception),
                "e": traceback.format_exc()}).encode("utf-8"))

        do_HEAD = lambda self: self.process("HEAD")
        do_GET = lambda self: self.process("GET")
        do_POST = lambda self: self.process("POST")
        do_DELETE = lambda self: self.process("DELETE")
        do_PUT = lambda self: self.process("PUT")
        do_PATCH = lambda self: self.process("PATCH")

        def do_OPTIONS(self):
            # CORS Preflight
            self.send_response(200)
            self.send_header("Access-Control-Allow-Methods", "OPTIONS,HEAD,GET,POST,PUT,DELETE")
            self.send_header("Access-Control-Allow-Headers", "Content-Type,Accept,Accept-Language,Authorization,X-Request-ID")
            self.end_headers()

    return HTTPRequestHandler

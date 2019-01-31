import socketserver
from qozyd.http import http_server_handler


class HttpServer():
    def __init__(self, context):
        self.context = context

    def start(self):
        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.TCPServer(("", 9876), http_server_handler(self.context)) as httpd:
            print("serving at port", 9876)

            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                httpd.shutdown()

    def stop(self):
        pass

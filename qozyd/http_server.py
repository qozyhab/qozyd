import logging
import socketserver
from qozyd.http import http_server_handler_factory


logger = logging.getLogger(__name__)


class HttpServer():
    def __init__(self, context, host="127.0.0.1", port=9876):
        self.context = context

        self.host = host
        self.port = port

    def start(self):
        socketserver.TCPServer.allow_reuse_address = True

        httpd = socketserver.TCPServer((self.host, self.port), http_server_handler_factory(self.context))
        logger.info("serving at http://{:s}:{:d}".format(self.host, self.port))

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.shutdown()

    def stop(self):
        pass

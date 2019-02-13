import re

import urllib.parse

from qozyd.http.exceptions import NotFoundException
from qozyd.http.request import Request
from qozyd.services.service_container import ServiceContainer, Instance


class UnfittableException(Exception):
    pass


class Context():
    def __init__(self, services, parent=None):
        self.service_container = ServiceContainer(
            (Instance(self, name="context"),) + services
        )
        self.parent = parent

    def start(self):
        self.service_container.start()

        return self

    def stop(self):
        self.service_container.stop()

        return self


class HttpContext(Context):
    def __init__(self, services, router, base_path="/", parent=None):
        super().__init__(services, parent=parent)

        self.router = router
        self.base_path = base_path

    @property
    def path(self):
        if self.parent and isinstance(self.parent, HttpContext):
            joined_path = "/".join([self.parent.path, self.base_path])
            joined_path = re.sub(r"/[\/]*/", "/", joined_path)

            return joined_path

        return self.base_path

    def fit(self, request):
        if not request.path.startswith(self.path):
            raise UnfittableException("Request can't be fitted unter {:s}".format(self.path))

        fitted_path = request.path[len(self.path):]

        if len(fitted_path) == 0:
            fitted_path = "/"

        return Request(request.method, fitted_path, request.headers, request.get, request.request_body)

    def handle(self, request):
        route_match = self.router.match(request)

        if route_match:
            route, url_view_args, matched_path = route_match
            view_service_name, view_method = route.view

            view_args = route.kwargs
            view_args.update(url_view_args)

            request.matched_path = matched_path

            view_service = self.service_container.get(view_service_name)
            response = getattr(view_service, view_method)(request, **view_args)

            return response

        raise NotFoundException

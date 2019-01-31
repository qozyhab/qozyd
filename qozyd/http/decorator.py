import json
import functools
from qozyd.http.response import Response, JsonResponse
from qozyd.http.exceptions import HttpException
from qozyd.utils.json import JsonEncoder
from jsonschema import validate, ValidationError
from jsonschema.validators import validator_for


def json_response(func):
    @functools.wraps(func)
    def wrapper_func(*args, **kwargs):
        controller_result = func(*args, **kwargs)
        
        if isinstance(controller_result, Response):
            return controller_result

        return JsonResponse(json.dumps(controller_result, cls=JsonEncoder))

    return wrapper_func


def json_validate(schema):
    def decorator(func):
        @functools.wraps(func)
        def wrapper_func(self, request, *args, **kwargs):
            try:
                validate(request.request_json, schema)
            except ValidationError:
                errors = [str(error.message) for error in validator_for(schema)(schema).iter_errors(request.request_json)]

                raise HttpException(422, errors)                    

            return func(self, request, *args, **kwargs)

        return wrapper_func

    return decorator

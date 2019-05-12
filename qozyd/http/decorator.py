import json
import functools
from functools import partial

from aiohttp import web
from aiohttp.web_response import Response
from json import JSONDecodeError

from qozyd.utils.json import JsonEncoder, json_encode
from jsonschema import validate, ValidationError
from jsonschema.validators import validator_for


def json_response(func):
    @functools.wraps(func)
    async def wrapper_func(*args, **kwargs):
        controller_result = await func(*args, **kwargs)
        
        if isinstance(controller_result, Response):
            return controller_result

        return web.json_response(controller_result, dumps=partial(json.dumps, cls=JsonEncoder))

    return wrapper_func


def json_validate(schema):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper_func(self, request, *args, **kwargs):
            try:
                json_data = None

                try:
                    json_data = await request.json()
                except JSONDecodeError:
                    pass

                validate(json_data, schema)
            except ValidationError:
                json_data = None

                try:
                    json_data = await request.json()
                except JSONDecodeError:
                    pass

                errors = [str(error.message) for error in validator_for(schema)(schema).iter_errors(json_data)]

                raise web.HTTPUnprocessableEntity(text=json_encode(errors), content_type="application/json")

            return await func(self, request, *args, **kwargs)

        return wrapper_func

    return decorator

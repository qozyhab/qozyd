import asyncio

import importlib
import functools


def import_symbol(name):
    components = name.split(".")

    module_path = ".".join(components[:-1])
    symbol_name = components[-1]

    module = importlib.import_module(module_path)
    symbol = getattr(module, symbol_name)

    return symbol


def as_coroutine(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        loop = asyncio.get_running_loop()
        return loop.run_in_executor(None, functools.partial(f, *args, **kwargs))

    return inner

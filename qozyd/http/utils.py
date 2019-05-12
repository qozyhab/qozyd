from aiohttp import web


def get_or_404(dictionary, key):
    if key not in dictionary:
        raise web.HTTPNotFound()

    return dictionary[key]

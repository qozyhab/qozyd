from .exceptions import NotFoundException


def get_or_404(dictionary, key):
    if key not in dictionary:
        raise NotFoundException()

    return dictionary[key]

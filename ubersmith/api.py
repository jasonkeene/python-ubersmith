# lower level api stuff, configuration, and http stuff goes here

from threading import local

_DEFAULT_REQUEST_HANDLER = local()
_DEFAULT_REQUEST_HANDLER.value = None


class RequestHandler(object):
    pass


def get_default_request_handler():
    if not _DEFAULT_REQUEST_HANDLER.value:
        raise Exception("Request handler required but no default was found.")
    return _DEFAULT_REQUEST_HANDLER.value


def set_default_request_handler(request_handler):
    if not isinstance(request_handler, RequestHandler):
        raise TypeError(
            "Attempted to set an invalid request handler as default.")
    _DEFAULT_REQUEST_HANDLER.value = request_handler

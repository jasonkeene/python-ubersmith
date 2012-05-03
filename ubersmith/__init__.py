from ubersmith.api import HttpRequestHandler, set_default_request_handler

__all__ = [
    # package modules
    'api',
    'exceptions',
    'utils',
    # call classes
    'calls',
    # call functions
    'client',
    'device',
    'order',
    'sales',
    'support',
    'uber',
    # init function
    'init',
]


def init(base_url, username=None, password=None):
    """Initialize ubersmith API module with HTTP request handler."""
    handler = HttpRequestHandler(base_url, username, password)
    set_default_request_handler(handler)
    return handler

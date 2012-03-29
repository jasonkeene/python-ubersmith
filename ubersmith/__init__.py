from ubersmith.api import HttpRequestHandler, set_default_request_handler

__all__ = [
    'api',
    'calls',
    'client',
    'device',
    'exceptions',
    'order',
    'sales',
    'init',
    'support',
    'uber',
    'utils',
]

def init(base_url, username=None, password=None):
    """Initialize ubersmith API module with HTTP request handler."""
    handler = HttpRequestHandler(base_url, username, password)
    set_default_request_handler(handler)
    return handler

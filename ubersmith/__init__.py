from ubersmith.api import HttpRequestHandler, set_default_request_handler

__all__ = [
    'api',
    'calls',
    'client',
    'device',
    'exceptions',
    'order',
    'sales',
    'setup'
    'support',
    'uber',
    'utils',
]


def setup(base_url, username=None, password=None):
    """Quickly setup ubersmith API via HTTP."""
    handler = HttpRequestHandler(base_url, username, password)
    set_default_request_handler(handler)

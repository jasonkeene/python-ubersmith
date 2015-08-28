from ubersmith.api import RequestHandler, set_default_request_handler
from ubersmith import (
    api,
    exceptions,
    utils,
    calls,
    client,
    device,
    order,
    sales,
    support,
    uber,
)

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


def init(base_url, username=None, password=None, verify=True):
    """Initialize ubersmith API module with HTTP request handler."""
    handler = RequestHandler(base_url, username, password, verify)
    set_default_request_handler(handler)
    return handler

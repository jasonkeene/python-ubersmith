from ubersmith.calls import generate_generic_calls
from ubersmith.calls.uber import (
    ApiExportCall,
    CheckLoginCall,
    ClientWelcomeStatsCall,
    MethodGetCall,
    MethodListCall,
    DocumentationCall,
)

__all__ = [
    'api_export',
    'check_login',
    'client_welcome_stats',
    'method_get',
    'method_list',
    'documentation',
]


# call functions with proper signatures and docstrings

def api_export(table, gzip=False, order_by=None, request_handler=None, **kwargs):
    """Export table data in CSV format."""
    kwargs.update({
        'table': table,
        'order_by': order_by,
    })
    if gzip:
        kwargs['gzip'] = 1
    return ApiExportCall(kwargs, request_handler).render()


def check_login(username, password, request_handler=None, **kwargs):
    """Check the specified username and password."""
    kwargs.update({
        'login': username,
        'pass': password,
    })
    return CheckLoginCall(kwargs, request_handler).render()


def client_welcome_stats(client_id, request_handler=None, **kwargs):
    """Output the statistics that are at the top of the client interface."""
    kwargs.update({'client_id': client_id})
    return ClientWelcomeStatsCall(kwargs, request_handler).render()


def method_get(method_name, request_handler=None, **kwargs):
    """Get the details of an API method."""
    kwargs.update({'method_name': method_name})
    return MethodGetCall(kwargs, request_handler).render()


def method_list(request_handler=None):
    """Get a list of all available API methods."""
    return MethodListCall(None, request_handler).render()


def documentation(request_handler=None):
    """Get a PDF document with details of all available API methods."""
    return DocumentationCall(None, request_handler).render()


generate_generic_calls('uber', globals())

from ubersmith.calls.base import api_call
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

@api_call
def api_export(table, gzip=False, order_by=None, request_handler=None):
    """Export table data in CSV format."""
    return ApiExportCall(request_handler, table, gzip, order_by).render()


@api_call
def check_login(username, password, request_handler=None):
    """Check the specified username and password."""
    return CheckLoginCall(request_handler, username, password).render()


@api_call
def client_welcome_stats(client_id, request_handler=None):
    """Output the statistics that are at the top of the client interface."""
    return ClientWelcomeStatsCall(request_handler, client_id).render()


@api_call
def method_get(method_name, request_handler=None):
    """Get the details of an API method."""
    return MethodGetCall(request_handler, method_name).render()


@api_call
def method_list(request_handler=None):
    """Get a list of all available API methods."""
    return MethodListCall(request_handler).render()


@api_call
def documentation(request_handler=None):
    """Get a PDF document with details of all available API methods."""
    return DocumentationCall(request_handler).render()

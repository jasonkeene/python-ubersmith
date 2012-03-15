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

def api_export(table, gzip=False, order_by=None, request_handler=None):
    """Export table data in CSV format."""
    request_data = {'table': table}
    if gzip:
        request_data['gzip'] = 1
    if order_by:
        request_data['order_by'] = order_by

    return ApiExportCall(request_data, request_handler).render()


def check_login(username, password, request_handler=None):
    """Check the specified username and password."""
    request_data = {
        'login': username,
        'pass': password,
    }

    return CheckLoginCall(request_data, request_handler).render()


def client_welcome_stats(client_id, request_handler=None):
    """Output the statistics that are at the top of the client interface."""
    request_data = {'client_id': client_id}
    return ClientWelcomeStatsCall(request_data, request_handler).render()


def method_get(method_name, request_handler=None):
    """Get the details of an API method."""
    request_data = {'method_name': method_name}
    return MethodGetCall(request_data, request_handler).render()


def method_list(request_handler=None):
    """Get a list of all available API methods."""
    return MethodListCall(None, request_handler).render()


def documentation(request_handler=None):
    """Get a PDF document with details of all available API methods."""
    return DocumentationCall(None, request_handler).render()

from ubersmith.calls import generate_generic_calls
from ubersmith.calls.uber import (
    ApiExportCall,
    ClientWelcomeStatsCall,
    MethodGetCall,
)

__all__ = [
    'api_export',
    'client_welcome_stats',
    'method_get',
]


def api_export(table, gzip=False, order_by=None, request_handler=None, **kwargs):
    """Export table data in CSV format."""
    kwargs['table'] = table
    if gzip:
        kwargs['gzip'] = 1
    if order_by is not None:
        kwargs['order_by'] = order_by
    return ApiExportCall(kwargs, request_handler).render()


def client_welcome_stats(client_id, request_handler=None, **kwargs):
    """Output the statistics that are at the top of the client interface."""
    kwargs.update({'client_id': client_id})
    return ClientWelcomeStatsCall(kwargs, request_handler).render()


def method_get(method_name, request_handler=None, **kwargs):
    """Get the details of an API method."""
    kwargs.update({'method_name': method_name})
    return MethodGetCall(kwargs, request_handler).render()


generate_generic_calls('uber', globals())

from ubersmith.calls import generate_generic_calls
from ubersmith.calls.order import (
    GetCall,
    ListCall,
)

__all__ = [
    'get',
    'list',
]


# call functions with proper signatures and docstrings

def get(order_id=None, request_handler=None, **kwargs):
    """Get the details of a specified order."""
    if order_id is not None:
        kwargs['order_id'] = order_id
    return GetCall(kwargs, request_handler).render()


def list(request_handler=None, **kwargs):
    """Get a list of orders."""
    return ListCall(kwargs, request_handler).render()


generate_generic_calls('order', globals())

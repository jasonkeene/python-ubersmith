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

def get(order_id=None, hash_=None, request_handler=None, **kwargs):
    """Get the details of a specified order."""
    kwargs.update({
        'order_id': order_id,
        'hash': hash_
    })
    return GetCall(kwargs, request_handler).render()


def list(request_handler=None, **kwargs):
    """Get a list of orders."""
    return ListCall(kwargs, request_handler).render()


generate_generic_calls('order', globals())

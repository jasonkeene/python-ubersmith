from ubersmith.calls import generate_generic_calls
from ubersmith.calls.order import GetCall

__all__ = ['get']


def get(order_id=None, request_handler=None, **kwargs):
    """Get the details of a specified order."""
    if order_id is not None:
        kwargs['order_id'] = order_id
    return GetCall(kwargs, request_handler).render()


generate_generic_calls(__name__.split('.')[-1], globals())

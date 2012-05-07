"""Order call functions.

These are light weight call functions that basically just wrap call classes
under ubersmith.calls.  If a call function doesn't exist it will be generated
by generate_generic_calls which searches for a call class and if one isn't
found one is created using ubersmith.calls.BaseCall.

"""

from ubersmith.calls import generate_generic_calls
from ubersmith.calls.order import GetCall

__all__ = ['get']


def get(order_id=None, request_handler=None, **kwargs):
    if order_id is not None:
        kwargs['order_id'] = order_id
    return GetCall(kwargs, request_handler).render()


generate_generic_calls(__name__.split('.')[-1], globals())

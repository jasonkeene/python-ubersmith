"""Device call functions.

These are light weight call functions that basically just wrap call classes
under ubersmith.calls.  If a call function doesn't exist it will be generated
by generate_generic_calls which searches for a call class and if one isn't
found one is created using ubersmith.calls.BaseCall.

"""

from ubersmith.calls import generate_generic_calls
from ubersmith.calls.device import GetCall

__all__ = ['get']


def get(device_id, request_handler=None, **kwargs):
    """Get a device's details."""
    kwargs.update({'device_id': device_id})
    return GetCall(kwargs, request_handler).render()


generate_generic_calls(__name__.split('.')[-1], globals())

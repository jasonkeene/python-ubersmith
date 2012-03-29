from ubersmith.calls import generate_generic_calls
from ubersmith.calls.device import GetCall

__all__ = ['get']


def get(device_id, request_handler=None, **kwargs):
    """Get a device's details."""
    kwargs.update({'device_id': device_id})
    return GetCall(kwargs, request_handler).render()


generate_generic_calls(__name__.split('.')[-1], globals())

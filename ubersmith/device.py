from ubersmith.calls import generate_generic_calls
from ubersmith.calls.device import (
    GetCall,
    ListCall,
)

__all__ = [
    'get',
    'list',
]


# call functions with proper signatures and docstrings

def get(device_id, request_handler=None, **kwargs):
    """Get a device's details."""
    kwargs.update({'device_id': device_id})
    return GetCall(kwargs, request_handler).render()


def list(request_handler=None, **kwargs):
    """List devices in the system."""
    return ListCall(request_handler, kwargs).render()


generate_generic_calls('device', globals())

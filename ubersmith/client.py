from ubersmith.calls.base import api_call
from ubersmith.calls.client import (
    GetCall,
    ListCall,
)

__all__ = [
    'get',
    'list',
]


# call functions w/ proper signatures and documentation

@api_call
def get(client_id=None, username=None, email=None, metadata=False,
        disabled=False, request_handler=None):
    """Get a client's details."""
    return GetCall(request_handler, client_id, username, email, metadata,
                    disabled).render()


@api_call
def list(request_handler=None):
    """Get a list of all active clients in the system."""
    return ListCall(request_handler).render()

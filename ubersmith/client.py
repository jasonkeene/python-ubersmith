from ubersmith.calls import generate_generic_calls
from ubersmith.calls.client import (
    GetCall,
    ListCall,
)

__all__ = [
    'get',
    'list',
]


# call functions w/ proper signatures and documentation

def get(client_id=None, user_login=None, email=None, request_handler=None,
                                                                    **kwargs):
    """Get a client's details.
    
    client_id
        Either this, user_login or email must be provided.
    user_login
        Either this, client_id or email must be provided.
    email
        Either this, user_login or client_id must be provided.

    """
    kwargs.update({
        'client_id': client_id,
        'user_login': user_login,
        'email': email,
    })
    return GetCall(kwargs, request_handler).render()


def list(request_handler=None, **kwargs):
    """Get a list of all active clients in the system."""
    return ListCall(kwargs, request_handler).render()


generate_generic_calls('client', globals())

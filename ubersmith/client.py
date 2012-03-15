from ubersmith.calls.client import (
    GetCall,
    ListCall,
)

__all__ = [
    'get',
    'list',
]


# call functions w/ proper signatures and documentation

def get(client_id=None, user_login=None, email=None, request_data=None,
        request_handler=None):
    """Get a client's details.
    
    client_id
        Either this, user_login or email must be provided.
    user_login
        Either this, client_id or email must be provided.
    email
        Either this, user_login or client_id must be provided.

    """
    request_data = request_data or {}
    if client_id:
        request_data['client_id'] = client_id
    elif user_login:
        request_data['user_login'] = user_login
    elif email:
        request_data['email'] = email

    return GetCall(request_data, request_handler).render()


def list(request_data=None, request_handler=None):
    """Get a list of all active clients in the system."""
    return ListCall(request_data, request_handler).render()

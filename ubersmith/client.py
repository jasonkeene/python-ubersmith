from ubersmith.calls import generate_generic_calls
from ubersmith.calls.client import GetCall

__all__ = ['get']


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
    kwargs.update(dict((k, v) for k, v in locals().iteritems() if k in [
        'client_id',
        'user_login',
        'email',
    ] and v is not None))
    return GetCall(kwargs, request_handler).render()


generate_generic_calls('client', globals())

"""Client call functions.

These are light weight call functions that basically just wrap call classes
under ubersmith.calls.  If a call function doesn't exist it will be generated
by generate_generic_calls which searches for a call class and if one isn't
found one is created using ubersmith.calls.BaseCall.

"""

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


generate_generic_calls(__name__.split('.')[-1], globals())

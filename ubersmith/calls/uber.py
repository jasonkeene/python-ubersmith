# uber calls implemented as documented in api docs go here

from ubersmith.exceptions import UbersmithResponseError
from ubersmith.calls.base import BaseCall, api_call
from ubersmith.utils import prepend_base

__all__ = [
    'check_login',
]

_METHOD_BASE = "uber"
prepend_base = prepend_base.init(_METHOD_BASE)


class _CheckLoginCall(BaseCall):
    method = prepend_base('check_login')

    def __init__(self, request_handler, username, password):
        super(_CheckLoginCall, self).__init__(request_handler)
        self.username = username
        self.password = password

    def validate(self):
        if self.username and self.password:
            return True

    def build_request_data(self):
        self.request_data = {
            'login': self.username,
            'pass': self.password,
        }

    def request(self):
        try:
            super(_CheckLoginCall, self).request()
        except UbersmithResponseError, exc:
            if exc.error_code == 3 and \
                            exc.error_message == 'Invalid login or password.':
                self.response_data = False
            else:
                raise  # re-raises the last exception

    def clean(self):
        self.cleaned = bool(self.response_data)


# call functions w/ proper signatures and documentation

@api_call
def check_login(username='', password='', request_handler=None):
    """Check the specified username and password."""
    if username and password:
        return _CheckLoginCall(request_handler, username, password).render()
    else:
        return False

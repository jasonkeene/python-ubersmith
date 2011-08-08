# uber calls implemented as documented in api docs go here

import ubersmith.api as _api
import ubersmith.calls.base as _base


_METHOD_BASE = "uber"
_prepend_base = lambda method: '.'.join((_METHOD_BASE, method))


class _CheckLoginCall(_base.BaseCall):
    method = _prepend_base('check_login')

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
            self.process_result = self.process()
        except _api.UbersmithError, e:
            if e.error_code == 3 and \
                              e.error_message == 'Invalid login or password.':
                self.process_result = False
            else:
                raise  # re-raises the last exception

    def clean(self):
        return bool(self.process_result)


# convenience functions w/ proper signatures and documentation

@_base.api_call
def check_login(username='', password='', request_handler=None):
    """Check the specified username and password."""
    return _CheckLoginCall(request_handler, username, password).render()

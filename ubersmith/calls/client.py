# client calls implemented as documented in api docs go here

import ubersmith.calls.base as _base

_METHOD_BASE = "client"
_prepend_base = lambda method: '.'.join((_METHOD_BASE, method))


class _GetCall(_base.BaseCall):
    method = _prepend_base('get')
    rename_fields = {
        'clientid': 'client_id',
    }
    int_fields = (
        'client_id',
        'class_id',
    )
    decimal_fields = (
        'balance',
        'discount',
        'inv_balance',
    )
    timestamp_fields = (
        'created',
        'password_changed',
    )
    php_serialized_fields = (
        'access',
    )

    def __init__(self, request_handler, client_id, username, email, metadata,
                 disabled):
        super(_GetCall, self).__init__(request_handler)
        self.client_id = client_id
        self.username = username
        self.email = email
        self.metadata = metadata
        self.disabled = disabled

    def validate(self):
        if self.client_id or self.username or self.email:
            return True

    def build_request_data(self):
        self.request_data = {}

        if self.client_id:
            self.request_data['client_id'] = self.client_id
        elif self.username:
            self.request_data['username'] = self.username
        elif self.email:
            self.request_data['email'] = self.email

        if self.metadata:
            self.request_data['metadata'] = 1

        if self.disabled:
            self.request_data['allclients'] = 1

    def request(self):
        self.process_result = self.process()


class _ListCall(_base.BaseCall):
    method = _prepend_base('list')

    def __init__(self, request_handler):
        super(_ListCall, self).__init__(request_handler)

    def validate(self):
        return True

    def build_request_data(self):
        self.request_data = {}

    def clean(self):
        return super(_ListCall, self).clean(True)

    def request(self):
        self.process_result = self.process()


# convenience functions w/ proper signatures and documentation

@_base.api_call
def get(client_id=None, username=None, email=None, metadata=False,
        disabled=False, request_handler=None):
    """Get a client's details."""
    return _GetCall(request_handler, client_id, username, email, metadata,
                    disabled).render()


@_base.api_call
def list(request_handler=None):
    """Get a list of all active clients in the system."""
    return _ListCall(request_handler).render()

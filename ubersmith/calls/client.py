"""Client calls implemented as documented in api docs."""

from ubersmith.calls.base import FlatCall, GroupCall
from ubersmith.utils import prepend_base

__all__ = [
    'GetCall',
    'ListCall',
]

prepend_base = prepend_base.init("client")


class GetCall(FlatCall):
    method = prepend_base('get')
    rename_fields = {
        'clientid': 'client_id',
    }
    int_fields = [
        'client_id',
        'class_id',
    ]
    decimal_fields = [
        'balance',
        'discount',
        'inv_balance',
    ]
    timestamp_fields = [
        'created',
        'password_changed',
    ]
    php_serialized_fields = [
        'access',
    ]

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


class ListCall(GroupCall):
    method = prepend_base('list')
    rename_fields = {
        'clientid': 'client_id',
    }
    int_fields = [
        'client_id',
        'class_id',
    ]
    decimal_fields = [
        'balance',
        'discount',
    ]
    timestamp_fields = [
        'created',
        'password_changed',
    ]
    php_serialized_fields = [
        'access',
    ]

"""Uber calls implemented as documented in api docs."""

from ubersmith.api import VALID_METHODS
from ubersmith.exceptions import (
    ResponseError,
    ValidationError,
    ValidationErrorDefault,
)
from ubersmith.calls.base import BaseCall, FlatCall, FileCall
from ubersmith.utils import prepend_base

__all__ = [
    'ApiExportCall',
    'CheckLoginCall',
    'ClientWelcomeStatsCall',
    'MethodGetCall',
    'MethodListCall',
    'DocumentationCall',
]

prepend_base = prepend_base.init("uber")


class ApiExportCall(BaseCall):
    method = prepend_base('api_export')

    def __init__(self, request_handler, table, gzip=False, order_by=None):
        super(ApiExportCall, self).__init__(request_handler)
        self.table = table
        self.gzip = gzip
        self.order_by = order_by

    def validate(self):
        if self.table:
            return True

    def build_request_data(self):
        self.request_data = {
            'table': self.table,
        }
        if self.gzip:
            self.request_data['gzip'] = 1
        if self.order_by:
            self.request_data['order_by'] = self.order_by


class CheckLoginCall(BaseCall):
    method = prepend_base('check_login')

    def __init__(self, request_handler, username, password):
        super(CheckLoginCall, self).__init__(request_handler)
        self.username = username
        self.password = password

    def validate(self):
        if not (self.username and self.password):
            raise ValidationErrorDefault(False)
        return True

    def build_request_data(self):
        self.request_data = {
            'login': self.username,
            'pass': self.password,
        }

    def request(self):
        try:
            super(CheckLoginCall, self).request()
        except ResponseError, exc:
            if exc.error_code == 3 and \
                            exc.error_message == 'Invalid login or password.':
                self.response_data = False
            else:
                raise  # re-raises the last exception

    def clean(self):
        self.cleaned = bool(self.response_data)


class ClientWelcomeStatsCall(FlatCall):
    method = prepend_base('client_welcome_stats')
    timestamp_fields = [
        'client_activity',
    ]
    date_fields = [
        'next_inv',
    ]
    int_fields = [
        'client_activity_type',
        'closed_count',
        'inv_count',
        'pack_count',
        'ticket',
        'type',
    ]

    def __init__(self, request_handler, client_id):
        super(ClientWelcomeStatsCall, self).__init__(request_handler)
        self.client_id = client_id

    def validate(self):
        if self.client_id:
            return True

    def build_request_data(self):
        self.request_data = {
            'client_id': self.client_id,
        }


class MethodGetCall(BaseCall):
    method = prepend_base('method_get')

    def __init__(self, request_handler, method_name):
        super(MethodGetCall, self).__init__(request_handler)
        self.method_name = method_name

    def validate(self):
        if self.method_name not in VALID_METHODS:
            raise ValidationError("Invalid method_name.")
        return True

    def build_request_data(self):
        self.request_data = {
            'method_name': self.method_name,
        }


class MethodListCall(BaseCall):
    method = prepend_base('method_list')


class DocumentationCall(FileCall):
    method = prepend_base('documentation')

"""Uber calls implemented as documented in api docs."""

from ubersmith.api import VALID_METHODS
from ubersmith.exceptions import (
    ResponseError,
    ValidationError,
    ValidationErrorDefault,
)
from ubersmith.calls.base import AbstractCall, FlatCall, FileCall
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


class ApiExportCall(AbstractCall):
    method = prepend_base('api_export')

    def validate(self):
        return bool(self.request_data.get('table'))


class CheckLoginCall(AbstractCall):
    method = prepend_base('check_login')

    def validate(self):
        if not (self.username and self.password):
            raise ValidationErrorDefault(False)
        return True

    def process_request(self):
        try:
            super(CheckLoginCall, self).process_request()
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

    def validate(self):
        return self.request_data.get('client_id')


class MethodGetCall(AbstractCall):
    method = prepend_base('method_get')

    def validate(self):
        if self.method_name not in VALID_METHODS:
            raise ValidationError("Invalid method_name.")
        return True


class MethodListCall(AbstractCall):
    method = prepend_base('method_list')


class DocumentationCall(FileCall):
    method = prepend_base('documentation')

"""Uber calls implemented as documented in api docs."""

from ubersmith.exceptions import (
    ResponseError,
    ValidationError,
    ValidationErrorDefault,
)
from ubersmith.calls.base import BaseCall, FileCall
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
    required_fields = ['table']


class CheckLoginCall(BaseCall):
    method = prepend_base('check_login')

    def process_request(self):
        # if login invalid just have the call return false
        try:
            super(CheckLoginCall, self).process_request()
        except ResponseError, e:
            if e.error_code == 3 and \
                            e.error_message == 'Invalid login or password.':
                self.response_data = False
            else:
                raise  # re-raises the last exception

    def clean(self):
        self.cleaned = bool(self.response_data)


class ClientWelcomeStatsCall(BaseCall):
    method = prepend_base('client_welcome_stats')
    required_fields = ['client_id']
    timestamp_fields = ['client_activity']
    date_fields = ['next_inv']
    int_fields = [
        'client_activity_type',
        'closed_count',
        'inv_count',
        'pack_count',
        'ticket',
        'type',
    ]


class MethodGetCall(BaseCall):
    method = prepend_base('method_get')


class MethodListCall(BaseCall):
    method = prepend_base('method_list')


class DocumentationCall(FileCall):
    method = prepend_base('documentation')

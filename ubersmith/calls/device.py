"""Device calls implemented as documented in api docs."""

from ubersmith.calls.base import BaseCall, GroupCall
from ubersmith.utils import prepend_base

__all__ = [
    'GetCall',
    'ListCall',
]

prepend_base = prepend_base.init("device")


class GetCall(BaseCall):
    method = prepend_base('get')

    def validate(self):
        return bool(self.request_data.get('device_id'))


class ListCall(GroupCall):
    method = prepend_base('list')
    rename_fields = {
        'clientid': 'client_id',
    }
    int_fields = [
        'client_id',
    ]

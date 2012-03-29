"""Device calls implemented as documented in api docs."""

from ubersmith.calls import BaseCall, GroupCall
from ubersmith.utils import prepend_base

__all__ = [
    'GetCall',
    'ListCall',
]

_ = prepend_base(__name__.split('.')[-1])


class GetCall(BaseCall):
    method = _('get')
    required_fields = ['device_id']


class ListCall(GroupCall):
    method = _('list')
    rename_fields = {'clientid': 'client_id'}
    int_fields = ['client_id']

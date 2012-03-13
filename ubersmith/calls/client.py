"""Client calls implemented as documented in api docs."""

from ubersmith.calls.base import FlatCall, GroupCall
from ubersmith.utils import prepend_base

__all__ = [
    'GetCall',
    'ListCall',
]

prepend_base = prepend_base.init("client")


class _ClientCallMixin(object):
    rename_fields = {
        'clientid': 'client_id',
    }
    bool_fields = [
        'active',
    ]
    int_fields = [
        'client_id',
        'class_id',
        'priority',
    ]
    decimal_fields = [
        'balance',
        'commission',
        'commission_rate',
        'discount',
        'inv_balance',
        'tier_commission',
        'tier_commission_rate',
    ]
    timestamp_fields = [
        'created',
        'latest_inv',
        'password_changed',
    ]
    php_serialized_fields = [
        'access',
    ]


class GetCall(_ClientCallMixin, FlatCall):
    method = prepend_base('get')

    def validate(self):
        if self.request_data.get('client_id') or \
           self.request_data.get('username') or \
           self.request_data.get('email'):
            return True


class ListCall(_ClientCallMixin, GroupCall):
    method = prepend_base('list')

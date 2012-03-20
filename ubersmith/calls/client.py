"""Client calls implemented as documented in api docs."""

from ubersmith.calls import BaseCall, GroupCall
from ubersmith.utils import prepend_base

__all__ = [
    'GetCall',
    'ListCall',
]

_ = prepend_base("client")


class _ClientCallMixin(object):
    rename_fields = {'clientid': 'client_id'}
    bool_fields = ['active']
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
    php_serialized_fields = ['access']


class GetCall(_ClientCallMixin, BaseCall):
    method = _('get')
    required_fields = [('client_id', 'username', 'email')]


class ListCall(_ClientCallMixin, GroupCall):
    method = _('list')

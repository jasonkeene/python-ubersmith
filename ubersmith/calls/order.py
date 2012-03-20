"""Order calls implemented as documented in api docs."""

from ubersmith.calls.base import BaseCall, GroupCall
from ubersmith.utils import prepend_base

__all__ = [
    'GetCall',
    'ListCall',
]

_ = prepend_base("order")


class GetCall(BaseCall):
    method = _('get')
    required_fields = [('order_id', 'hash')]


class ListCall(GroupCall):
    method = _('list')

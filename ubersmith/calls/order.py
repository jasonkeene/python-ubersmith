"""Order calls implemented as documented in api docs."""

from ubersmith.calls.base import BaseCall, GroupCall
from ubersmith.utils import prepend_base

__all__ = [
    'GetCall',
    'ListCall',
]

prepend_base = prepend_base.init("order")


class GetCall(BaseCall):
    method = prepend_base('get')

    def validate(self):
        return bool(self.request_data.get('order_id') or
                    self.request_data.get('hash'))



class ListCall(GroupCall):
    method = prepend_base('list')

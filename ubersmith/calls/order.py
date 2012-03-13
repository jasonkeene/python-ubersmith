"""Order calls implemented as documented in api docs."""

from ubersmith.calls.base import FlatCall, GroupCall
from ubersmith.utils import prepend_base

__all__ = [
    'GetCall',
    'ListCall',
]

prepend_base = prepend_base.init("order")


class GetCall(FlatCall):
    method = prepend_base('get')

    def __init__(self, request_handler, order_id=None, hash_=None):
        super(GetCall, self).__init__(request_handler)

        self.order_id = order_id
        self.hash = hash_

    def validate(self):
        if self.order_id or self.hash:
            return True

    def build_request_data(self):
        self.request_data = {}

        if self.order_id:
            self.request_data['order_id'] = self.order_id
        elif self.hash:
            self.request_data['hash'] = self.hash


class ListCall(GroupCall):
    method = prepend_base('list')

    def __init__(self, request_handler, order_step_id=None,
                 order_queue_id=None, brand_id=None, step_name=None,
                 min_ts=None, max_ts=None, client_id=None,
                 opportunity_id=None, order_by=None, direction=None,
                 offset=None, limit=None):
        super(ListCall, self).__init__(request_handler)

        self.order_step_id = order_step_id
        self.order_queue_id = order_queue_id
        self.brand_id = brand_id
        self.step_name = step_name
        self.min_ts = min_ts
        self.max_ts = max_ts
        self.client_id = client_id
        self.opportunity_id = opportunity_id
        self.order_by = order_by
        self.direction = direction
        self.offset = offset
        self.limit = limit

    def build_request_data(self):
        self.request_data = {}
        if self.order_step_id:
            self.request_data['order_step_id'] = self.order_step_id
        if self.order_queue_id:
            self.request_data['order_queue_id'] = self.order_queue_id
        if self.brand_id:
            self.request_data['brand_id'] = self.brand_id
        if self.step_name:
            self.request_data['step_name'] = self.step_name
        if self.min_ts:
            self.request_data['min_ts'] = self.min_ts
        if self.max_ts:
            self.request_data['max_ts'] = self.max_ts
        if self.client_id:
            self.request_data['client_id'] = self.client_id
        if self.opportunity_id:
            self.request_data['opportunity_id'] = self.opportunity_id
        if self.order_by:
            self.request_data['order_by'] = self.order_by
        if self.direction:
            self.request_data['direction'] = self.direction
        if self.offset:
            self.request_data['offset'] = self.offset
        if self.limit:
            self.request_data['limit'] = self.limit

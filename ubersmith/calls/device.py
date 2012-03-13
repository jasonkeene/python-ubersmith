"""Device calls implemented as documented in api docs."""

from ubersmith.calls.base import FlatCall, GroupCall
from ubersmith.utils import prepend_base

__all__ = [
    'GetCall',
    'ListCall',
]

prepend_base = prepend_base.init("device")


class GetCall(FlatCall):
    method = prepend_base('get')

    def __init__(self, request_handler, device_id, metadata=None,
                 service=None, modules=None, tags=None):
        super(GetCall, self).__init__(request_handler)
        self.device_id = device_id
        self.metadata = metadata
        self.service = service
        self.modules = modules
        self.tags = tags

    def validate(self):
        if self.device_id:
            return True

    def build_request_data(self):
        self.request_data = {
            'device_id': self.device_id,
        }
        if self.metadata:
            self.request_data['metadata'] = self.metadata
        if self.service:
            self.request_data['service'] = self.service
        if self.modules:
            self.request_data['modules'] = self.modules
        if self.tags:
            self.request_data['tags'] = self.tags


class ListCall(GroupCall):
    method = prepend_base('list')
    rename_fields = {
        'clientid': 'client_id',
    }
    int_fields = [
        'client_id',
    ]

    def __init__(self, request_handler, parent=None, client_id=None,
                 service_id=None, status=None, label=None, dev_desc=None,
                 devtype_group_id=None, type_id=None, rack_id=None,
                 row_id=None, cage_id=None, zone_id=None, fac_id=None,
                 require_ip=None, metadata=None, order_by=None,
                 direction=None, offset=None, limit=None):
        super(ListCall, self).__init__(request_handler)
        self.parent = parent
        self.client_id = client_id
        self.service_id = service_id
        self.status = status
        self.label = label
        self.dev_desc = dev_desc
        self.devtype_group_id = devtype_group_id
        self.type_id = type_id
        self.rack_id = rack_id
        self.row_id = row_id
        self.cage_id = cage_id
        self.zone_id = zone_id
        self.fac_id = fac_id
        self.require_ip = require_ip
        self.metadata = metadata
        self.order_by = order_by
        self.direction = direction
        self.offset = offset
        self.limit = limit

    def build_request_data(self):
        self.request_data = {}
        if self.parent:
            self.request_data['parent'] = self.parent
        if self.client_id:
            self.request_data['client_id'] = self.client_id
        if self.service_id:
            self.request_data['service_id'] = self.service_id
        if self.status:
            self.request_data['status'] = self.status
        if self.label:
            self.request_data['label'] = self.label
        if self.dev_desc:
            self.request_data['dev_desc'] = self.dev_desc
        if self.devtype_group_id:
            self.request_data['devtype_group_id'] = self.devtype_group_id
        if self.type_id:
            self.request_data['type_id'] = self.type_id
        if self.rack_id:
            self.request_data['rack_id'] = self.rack_id
        if self.row_id:
            self.request_data['row_id'] = self.row_id
        if self.cage_id:
            self.request_data['cage_id'] = self.cage_id
        if self.zone_id:
            self.request_data['zone_id'] = self.zone_id
        if self.fac_id:
            self.request_data['fac_id'] = self.fac_id
        if self.require_ip:
            self.request_data['require_ip'] = self.require_ip
        if self.metadata:
            self.request_data['metadata'] = self.metadata
        if self.order_by:
            self.request_data['order_by'] = self.order_by
        if self.direction:
            self.request_data['direction'] = self.direction
        if self.offset:
            self.request_data['offset'] = self.offset
        if self.limit:
            self.request_data['limit'] = self.limit

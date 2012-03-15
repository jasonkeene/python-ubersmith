from ubersmith.calls.device import (
    GetCall,
    ListCall,
)

__all__ = [
    'get',
    'list',
]


# call functions with proper signatures and docstrings

def get(device_id, metadata=None, service=None, modules=None, tags=None,
        request_handler=None):
    """Get a device's details."""
    request_data = {'device_id': device_id}
    if metadata:
        request_data['metadata'] = metadata
    if service:
        request_data['service'] = service
    if modules:
        request_data['modules'] = modules
    if tags:
        request_data['tags'] = tags

    return GetCall(request_data, request_handler).render()


def list(parent=None, client_id=None, service_id=None, status=None,
          label=None, dev_desc=None, devtype_group_id=None, type_id=None,
          rack_id=None, row_id=None, cage_id=None, zone_id=None, fac_id=None,
          require_ip=None, metadata=None, order_by=None, direction=None,
          offset=None, limit=None, request_handler=None):
    """List devices in the system."""
    request_data = {}
    if parent:
        request_data['parent'] = parent
    if client_id:
        request_data['client_id'] = client_id
    if service_id:
        request_data['service_id'] = service_id
    if status:
        request_data['status'] = status
    if label:
        request_data['label'] = label
    if dev_desc:
        request_data['dev_desc'] = dev_desc
    if devtype_group_id:
        request_data['devtype_group_id'] = devtype_group_id
    if type_id:
        request_data['type_id'] = type_id
    if rack_id:
        request_data['rack_id'] = rack_id
    if row_id:
        request_data['row_id'] = row_id
    if cage_id:
        request_data['cage_id'] = cage_id
    if zone_id:
        request_data['zone_id'] = zone_id
    if fac_id:
        request_data['fac_id'] = fac_id
    if require_ip:
        request_data['require_ip'] = require_ip
    if metadata:
        request_data['metadata'] = metadata
    if order_by:
        request_data['order_by'] = order_by
    if direction:
        request_data['direction'] = direction
    if offset:
        request_data['offset'] = offset
    if limit:
        request_data['limit'] = limit

    return ListCall(request_data, request_handler).render()

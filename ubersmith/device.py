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
    return GetCall(request_handler, device_id, metadata, service, modules,
                    tags).render()


def list(parent=None, client_id=None, service_id=None, status=None,
          label=None, dev_desc=None, devtype_group_id=None, type_id=None,
          rack_id=None, row_id=None, cage_id=None, zone_id=None, fac_id=None,
          require_ip=None, metadata=None, order_by=None, direction=None,
          offset=None, limit=None, request_handler=None):
    """List devices in the system."""
    return ListCall(request_handler, parent, client_id, service_id, status,
                     label, dev_desc, devtype_group_id, type_id, rack_id,
                     row_id, cage_id, zone_id, fac_id, require_ip, metadata,
                     order_by, direction, offset, limit).render()

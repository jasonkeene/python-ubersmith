"""Device call classes.

These classes implement any response cleaning and validation needed.  If a
call class isn't defined for a given method then one is created using
ubersmith.calls.BaseCall.

"""

from ubersmith.calls import BaseCall
from ubersmith.clean import clean
from ubersmith.utils import prepend_base

__all__ = [
    'ConnectionListCall',
    'GetCall',
    'ListCall',
    # 'ModuleGraphCall',
    'MonitorListCall',
]

_ = prepend_base(__name__.split('.')[-1])


_DEVICE_CLEANER = clean(dict, values={
    'active': 'int',
    'cage_id': 'int',
    'clientid': 'int',
    'dev': 'int',
    'devtype_group_id': 'int',
    'disabled': 'int',
    'down': 'int',
    'fac_id': 'int',
    'owner': 'int',
    'parent': 'int',
    'rack_id': 'int',
    'row_id': 'int',
    'total': 'int',
    'type_id': 'int',
    'up': 'int',
    'warn': 'int',
    'zone_id': 'int',
    'depth': float,
    'height': float,
    'width': float,
})


class ConnectionListCall(BaseCall):
    method = _('connection_list')
    required_fields = ['device_id']
    cleaner = clean(dict, keys='int', values=clean(dict, values={
        'connection_id': 'int',
        'connection_type_id': 'int',
        'connection_class_id': 'int',
        'status': 'int',
        'client_id': 'int',
        'service_id': 'int',
        'src_device_id': 'int',
        'src_interface_id': 'int',
        'src_node_type_id': 'int',
        'dst_device_id': 'int',
        'dst_interface_id': 'int',
        'dst_node_type_id': 'int',
        'num_links': 'int',
        'start_ts': 'timestamp',
        'end_ts': 'timestamp',
        'created_ts': 'timestamp',
        'updated_ts': 'timestamp',
    }))


class GetCall(BaseCall):
    method = _('get')
    required_fields = ['device_id']
    cleaner = _DEVICE_CLEANER


class ListCall(BaseCall):
    method = _('list')
    cleaner = clean(dict, keys='int', values=_DEVICE_CLEANER)


class IpAssignmentListCall(BaseCall):
    method = _('ip_assignment_list')
    cleaner = clean(dict, keys='int', values=clean(dict, values={
        'addr_type': 'int',
        'assign_id': 'int',
        'client_id': 'int',
        'created_ts': 'timestamp',
        'device_id': 'int',
        'group_client_id': 'int',
        'group_id': 'int',
        'num_ips': 'int',
        'portable': bool,
        'service_id': 'int',
        'updated_ts': 'timestamp',
        'vlan_num': 'int',
        'vlan_range_id': 'int',
        'vlan_type_id': 'int',
    }))


class ModuleGraphCall(BaseCall):
    method = _('module_graph')


class MonitorListCall(BaseCall):
    method = _('monitor_list')
    required_fields = ['protocol']
    cleaner = clean(dict, keys='int', values=clean(dict, values={
        'dev': 'int',
        'script_id': 'int',
        'last_change': 'timestamp',
        'last_notified': 'timestamp',
        'last_poll': 'timestamp',
    }))

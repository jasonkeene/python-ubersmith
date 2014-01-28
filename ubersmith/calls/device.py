"""Device call classes.

These classes implement any response cleaning and validation needed.  If a
call class isn't defined for a given method then one is created using
ubersmith.calls.BaseCall.

"""

from ubersmith.calls import BaseCall, GroupCall, FileCall
from ubersmith.utils import prepend_base

__all__ = [
    'GetCall',
    'ListCall',
    'ModuleGraphCall',
]

_ = prepend_base(__name__.split('.')[-1])


class GetCall(BaseCall):
    method = _('get')
    required_fields = ['device_id']
    int_fields = ['active', 'cage_id', 'clientid', 'dev', 'devtype_group_id',
                  'disabled', 'down', 'fac_id', 'owner', 'parent',
                  'rack_id', 'row_id', 'total', 'type_id', 'up', 'warn',
                  'zone_id']
    float_fields = ['depth', 'height', 'width']


class ListCall(GroupCall):
    method = _('list')
    int_fields = ['active', 'cage_id', 'clientid', 'dev', 'devtype_group_id',
                  'disabled', 'down', 'fac_id', 'owner', 'parent',
                  'rack_id', 'row_id', 'total', 'type_id', 'up', 'warn',
                  'zone_id']
    float_fields = ['depth', 'height', 'width']


class ModuleGraphCall(FileCall):
    method = _('module_graph')


class MonitorListCall(GroupCall):
    method = _('monitor_list')
    required_fields = ['protocol']
    int_fields = ['dev', 'script_id']
    timestamp_fields = ['last_change', 'last_notified', 'last_poll']

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


class ListCall(GroupCall):
    method = _('list')
    int_fields = ['client_id']


class ModuleGraphCall(FileCall):
    method = _('module_graph')

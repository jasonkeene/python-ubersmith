"""Support call classes.

These classes implement any response cleaning and validation needed.  If a
call class isn't defined for a given method then one is created using
ubersmith.calls.BaseCall.

"""

from ubersmith.calls import GroupCall
from ubersmith.utils import prepend_base

__all__ = [
    'DepartmentListCall',
]

_ = prepend_base(__name__.split('.')[-1])


class DepartmentListCall(GroupCall):
    method = _('department_list')
    int_fields = [
        'q_id',
        'q_order',
    ]

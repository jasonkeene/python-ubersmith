"""Order call classes.

These classes implement any response cleaning and validation needed.  If a
call class isn't defined for a given method then one is created using
ubersmith.calls.BaseCall.

"""

from ubersmith.calls import BaseCall, GroupCall, _rename_key
from ubersmith.utils import prepend_base

__all__ = [
    'GetCall',
    'ListCall',
]

_ = prepend_base(__name__.split('.')[-1])


class GetCall(BaseCall):
    method = _('get')
    required_fields = [('order_id', 'hash')]


class ListCall(GroupCall):
    method = _('list')


class QueueListCall(GroupCall):
    method = _('queue_list')
    required_fields = ['brand_id']

    def clean(self):
        super(QueueListCall, self).clean()
        # clean additional stuff that is nested in the response
        for value in self.cleaned.values():
            for k, v in value['steps'].items():
                _rename_key(value['steps'], k, int(k))
                # v['count'] = int(v['count'])

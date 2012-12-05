"""Order call classes.

These classes implement any response cleaning and validation needed.  If a
call class isn't defined for a given method then one is created using
ubersmith.calls.BaseCall.

"""

from ubersmith.calls import BaseCall, GroupCall, _rename_key, _CLEANERS
from ubersmith.utils import prepend_base

__all__ = [
    'GetCall',
    'ListCall',
    'QueueListCall',
]

_ = prepend_base(__name__.split('.')[-1])


class GetCall(BaseCall):
    method = _('get')
    required_fields = [('order_id', 'hash')]
    int_fields = ['order_id', 'priority', 'order_status', 'client_id',
                  'order_form_id', 'order_queue_id', 'opportunity_id']
    decimal_fields = ['total']
    timestamp_fields = ['activity', 'ts']

    def clean(self):
        super(GetCall, self).clean()
        # clean additional stuff that is nested in the response
        # need to test if there is value for progress cus it might be a list
        if self.cleaned.get('progress'):
            for k, v in self.cleaned['progress'].items():
                _rename_key(self.cleaned['progress'], k, int(k))
                v['ts'] = _CLEANERS['timestamp'](v['ts'])


class ListCall(GroupCall):
    method = _('list')
    int_fields = ['order_id', 'priority', 'order_status', 'client_id',
                  'order_form_id', 'order_queue_id', 'opportunity_id']
    decimal_fields = ['total']
    timestamp_fields = ['activity', 'ts']


class QueueListCall(GroupCall):
    method = _('queue_list')
    required_fields = ['brand_id']

    def clean(self):
        super(QueueListCall, self).clean()
        # clean additional stuff that is nested in the response
        for value in self.cleaned.values():
            for k, v in value['steps'].items():
                _rename_key(value['steps'], k, int(k))
                v['count'] = int(v['count'])

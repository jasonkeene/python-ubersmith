"""Order call classes.

These classes implement any response cleaning and validation needed.  If a
call class isn't defined for a given method then one is created using
ubersmith.calls.BaseCall.

"""

from ubersmith.calls import BaseCall
from ubersmith.clean import clean
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
    cleaner = clean(dict, values={
        'order_id': 'int',
        'order_status': 'int',
        'client_id': 'int',
        'order_form_id': 'int',
        'order_queue_id': 'int',
        'opportunity_id': 'int',
        'total': 'decimal',
        'activity': 'timestamp',
        'ts': 'timestamp',
        'progress': clean(dict, keys='int', values=clean(dict, values={
            'ts': 'timestamp',
        })),
    })


class ListCall(BaseCall):
    method = _('list')
    cleaner = clean(dict, keys='int', values=clean(dict, values={
        'order_id': 'int',
        'priority': 'int',
        'order_status': 'int',
        'client_id': 'int',
        'order_form_id': 'int',
        'order_queue_id': 'int',
        'opportunity_id': 'int',
        'total': 'decimal',
        'activity': 'timestamp',
        'ts': 'timestamp',
    }))


class QueueListCall(BaseCall):
    method = _('queue_list')
    required_fields = ['brand_id']
    cleaner = clean(dict, keys='int', values=clean(dict, values={
        'steps': clean(dict, keys='int', values=clean(dict, values={
            'count': 'int',
        })),
    }))

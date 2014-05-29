"""Client call classes.

These classes implement any response cleaning and validation needed.  If a
call class isn't defined for a given method then one is created using
ubersmith.calls.BaseCall.

"""

from collections import namedtuple
import datetime
import re

from ubersmith.calls import BaseCall, GroupCall
from ubersmith.utils import prepend_base

__all__ = [
    'GetCall',
    'ListCall',
    'PaymentMethodListCall',
    'InvoiceCountCall',
    'InvoicePaymentsCall',
    'InvoiceGet',
    'InvoiceList',
    'CreditListCall',
]

_ = prepend_base(__name__.split('.')[-1])


class _ClientCallMixin(object):
    bool_fields = ['active']
    int_fields = [
        'clientid',
        'class_id',
        'priority',
    ]
    decimal_fields = [
        'balance',
        'commission',
        'commission_rate',
        'discount',
        'inv_balance',
        'tier_commission',
        'tier_commission_rate',
    ]
    timestamp_fields = [
        'created',
        'latest_inv',
        'password_changed',
    ]
    php_serialized_fields = ['access']


class GetCall(_ClientCallMixin, BaseCall):
    method = _('get')
    required_fields = [('client_id', 'user_login', 'email')]


class ListCall(_ClientCallMixin, GroupCall):
    method = _('list')


class PaymentMethodListCall(GroupCall):
    method = _('payment_method_list')


class InvoiceCountCall(BaseCall):
    method = _('invoice_count')
    required_fields = ['client_id']

    def clean(self):
        super(InvoiceCountCall, self).clean()
        self.cleaned = int(self.cleaned)


class InvoicePaymentsCall(GroupCall):
    method = _('invoice_payments')
    required_fields = ['invoice_id']

    timestamp_fields = [
        'time',
    ]


class InvoiceGet(BaseCall):
    method = _('invoice_get')
    required_fields = ['invoice_id']
    int_fields = [
        'clientid',
        'invid',
    ]
    timestamp_fields = [
        'date',
        'datepaid',
        'due',
        'overdue',
    ]

    _UbersmithFile = namedtuple('UbersmithFile', ['filename', 'type',
                                                  'modified', 'data'])

    def process_request(self):
        """Processing the call and set response_data."""
        self.raw = self.request_data.get('format') not in [None, 'json']
        self.response_data = self.request_handler.process_request(self.method,
                                                            self.request_data,
                                                            raw=self.raw)

    def clean(self):
        if not self.raw:
            return super(InvoiceGet, self).clean()
        fname = None
        disposition = self.response_data[0].get('content-disposition')
        if disposition:
            fname = re.search(r'.*?filename=(.+)', disposition, re.I).group(1)
            fname = re.sub(r'[^a-z0-9-_\. ]', '-', fname, 0, re.I).lstrip('.')

        self.filename = fname
        self.type = self.response_data[0].get('content-type')
        last_modified = self.response_data[0].get('last-modified')
        if last_modified:
            self.modified = datetime.datetime(
                                      *parsedate_tz(last_modified)[:7])
        else:
            self.modified = datetime.datetime.now()
        self.data = buffer(self.response_data[1])

        self.cleaned = self._UbersmithFile(self.filename, self.type,
                                           self.modified, self.data)


class InvoiceList(GroupCall):
    method = _('invoice_list')
    int_fields = [
        'clientid',
        'invid',
    ]
    timestamp_fields = [
        'date',
        'datepaid',
        'due',
    ]


class CreditListCall(GroupCall):
    method = _('credit_list')
    required_fields = ['client_id']

    int_fields = [
        'clientid',
        'active',
        'credit_id',
        'order_id',
    ]

    timestamp_fields = [
        'date',
    ]

"""Client call classes.

These classes implement any response cleaning and validation needed.  If a
call class isn't defined for a given method then one is created using
ubersmith.calls.BaseCall.

"""

from collections import namedtuple

from ubersmith.calls import BaseCall
from ubersmith.clean import clean
from ubersmith.utils import prepend_base, get_filename

__all__ = [
    'GetCall',
    'ListCall',
    'PaymentMethodListCall',
    'InvoiceCountCall',
    'InvoicePaymentsCall',
    'InvoiceGet',
    'InvoiceList',
    'CreditListCall',
    'ServiceAddCall',
]

_ = prepend_base(__name__.split('.')[-1])


_CLIENT_CLEANER = clean(dict, values={
    'active': bool,
    'clientid': 'int',
    'class_id': 'int',
    'priority': 'int',
    'balance': 'decimal',
    'commission': 'decimal',
    'commission_rate': 'decimal',
    'discount': 'decimal',
    'tier_commission': 'decimal',
    'tier_commission_rate': 'decimal',
    'created': 'timestamp',
    'latest_inv': 'timestamp',
    'password_changed': 'timestamp',
    'access': 'php',
})


class GetCall(BaseCall):
    method = _('get')
    required_fields = [('client_id', 'user_login', 'email')]
    cleaner = _CLIENT_CLEANER


class ListCall(BaseCall):
    method = _('list')
    cleaner = clean(dict, keys='int', values=_CLIENT_CLEANER)


class PaymentMethodListCall(BaseCall):
    method = _('payment_method_list')
    cleaner = clean(dict, keys='int')


class InvoiceCountCall(BaseCall):
    method = _('invoice_count')
    required_fields = ['client_id']
    cleaner = int


class InvoicePaymentsCall(BaseCall):
    method = _('invoice_payments')
    required_fields = ['invoice_id']
    cleaner = clean(dict, keys='int', values=clean(dict, values={
        'time': 'timestamp',
    }))


class InvoiceGet(BaseCall):
    method = _('invoice_get')
    required_fields = ['invoice_id']
    cleaner = clean(dict, values={
        'clientid': 'int',
        'invid': 'int',
        'date': 'timestamp',
        'datepaid': 'timestamp',
        'due': 'timestamp',
        'overdue': 'timestamp',
    })


class InvoiceList(BaseCall):
    method = _('invoice_list')
    cleaner = clean(dict, keys='int', values=clean(dict, values={
        'clientid': 'int',
        'invid': 'int',
        'date': 'timestamp',
        'datepaid': 'timestamp',
        'due': 'timestamp',
    }))


class CreditListCall(BaseCall):
    method = _('credit_list')
    required_fields = ['client_id']
    cleaner = clean(dict, keys='int', values=clean(dict, values={
        'clientid': 'int',
        'active': 'int',
        'credit_id': 'int',
        'order_id': 'int',
        'date': 'timestamp',
    }))


class ServiceAddCall(BaseCall):
    method = _('service_add')
    required_fields = ['client_id']
    cleaner = clean(int)


class CCAddCall(BaseCall):
    method = _('cc_add')
    required_fields = ['client_id', 'cc_num']
    cleaner = clean(int)

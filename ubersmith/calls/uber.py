"""Uber call classes.

These classes implement any response cleaning and validation needed.  If a
call class isn't defined for a given method then one is created using
ubersmith.calls.BaseCall.

"""

from ubersmith.calls import BaseCall
from ubersmith.clean import clean
from ubersmith.utils import prepend_base

__all__ = [
    'ApiExportCall',
    'CheckLoginCall',
    'ClientWelcomeStatsCall',
    'MethodGetCall',
    'DocumentationCall',
]

_ = prepend_base(__name__.split('.')[-1])


class ApiExportCall(BaseCall):
    method = _('api_export')
    required_fields = ['table']


class CheckLoginCall(BaseCall):
    method = _('check_login')
    cleaner = clean(dict, values={
        'password_expired': 'int',
        'last_login': 'timestamp',
        'password_changed': 'timestamp',
    })


class ClientWelcomeStatsCall(BaseCall):
    method = _('client_welcome_stats')
    required_fields = ['client_id']
    cleaner = clean(dict, values={
        'client_activity_type': 'int',
        'closed_count': 'int',
        'inv_count': 'int',
        'pack_count': 'int',
        'ticket': 'int',
        'type': 'int',
        'client_activity': 'timestamp',
        'next_inv': 'date',
    })


class MethodGetCall(BaseCall):
    method = _('method_get')


class DocumentationCall(BaseCall):
    method = _('documentation')

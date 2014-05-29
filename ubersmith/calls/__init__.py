from collections import namedtuple
import copy
import datetime
from decimal import Decimal
import re
import rfc822
import time

import phpserialize

from ubersmith.api import METHODS, get_default_request_handler
from ubersmith.exceptions import ValidationError

__all__ = [
    # abstract call classes
    'BaseCall',
    'GroupCall',
    'FileCall',
    # generate generic calls
    'generate_generic_calls',
    # concrete call classes
    'client',
    'device',
    'order',
    'sales',
    'support',
    'uber',
]

_CLEANERS = {
    'bool': bool,
    'int': int,
    'decimal': lambda x: Decimal(x.replace(',', '')),
    'float': float,
    'timestamp': lambda x: datetime.datetime.fromtimestamp(float(x)),
    'date': lambda x: datetime.date(*time.strptime(x, '%b/%d/%Y')[:3]),
    'php_serialized': phpserialize.loads,
}


class BaseCall(object):
    """Abstract class to implement a call with validation/cleaning/etc."""

    method = ''  # ubersmith method name, should be defined on child classes
    required_fields = []  # field names that should be present in request_data
    bool_fields = []  # fields to convert to bools
    int_fields = []  # fields to convert to ints
    decimal_fields = []  # fields to convert to decimals
    float_fields = []   # fields to convert to floats
    timestamp_fields = []  # fields to convert from timestamps to datetime
    date_fields = []  # fields to convert to datetime.date
    php_serialized_fields = []  # fields to convert from php serialized format

    def __init__(self, request_data=None, request_handler=None):
        """Setup call with provided request data and handler."""
        self.request_data = request_data or {}  # data for the request
        self.request_handler = request_handler or \
            get_default_request_handler()  # handler to fullfil the request
        self.response_data = None  # response data is stored here
        self.cleaned = None  # cleaned response data is stored here

    def render(self):
        """Validate, process, clean and return the result of the call."""
        if not self.validate():
            raise ValidationError

        self.process_request()
        self.clean()

        return self.cleaned

    def validate(self):
        """Validate request data before sending it out. Return True/False."""
        # check if required_fields aren't present
        for field in set(self.required_fields) - set(self.request_data):
            if not isinstance(field, basestring):
                # field was a collection, iterate over it and check by OR
                return bool(set(field) & set(self.request_data))
            return False
        return True

    def process_request(self):
        """Processing the call and set response_data."""
        self.response_data = self.request_handler.process_request(self.method,
                                                            self.request_data)

    def clean(self):
        """Clean response data."""
        cleaned = copy.deepcopy(self.response_data)
        _clean_fields(self, cleaned)
        self.cleaned = cleaned


class GroupCall(BaseCall):
    """Abstract class to implement a call that returns a group of results."""

    def clean(self):
        cleaned = copy.deepcopy(self.response_data)

        # convert top level keys to ints
        for key in self.response_data.iterkeys():
            _rename_key(cleaned, key, int(key))

        # clean fields on each member of the group
        for member in cleaned.itervalues():
            _clean_fields(self, member)

        self.cleaned = cleaned


class FileCall(BaseCall):
    """Abstract class to implement a call that returns a file."""
    _UbersmithFile = namedtuple('UbersmithFile', ['filename', 'type',
                                                  'modified', 'data'])

    def process_request(self):
        """Processing the call and set response_data."""
        self.response_data = self.request_handler.process_request(self.method,
                                                            self.request_data,
                                                            raw=True)

    def clean(self):
        fname = None
        disposition = self.response_data[0].get('content-disposition')
        if disposition:
            fname = re.search(r'.*?filename="(.+?)"', disposition, re.I).group(1)
            fname = re.sub(r'[^a-z0-9-_\. ]', '-', fname, 0, re.I).lstrip('.')

        self.filename = fname
        self.type = self.response_data[0].get('content-type')
        last_modified = self.response_data[0].get('last-modified')
        if last_modified:
            self.modified = datetime.datetime(
                                      *rfc822.parsedate_tz(last_modified)[:7])
        else:
            self.modified = datetime.datetime.now()
        self.data = buffer(self.response_data[1])

        self.cleaned = self._UbersmithFile(self.filename, self.type,
                                           self.modified, self.data)


def _rename_key(d, old, new):
    """Rename a key on d from old to new."""
    if old in d and new not in d:
        d[new] = d[old]
        del d[old]


def _clean_fields(call, d):
    """Clean fields on d using info on call."""
    for name, func in _CLEANERS.iteritems():
        for field in getattr(call, '{0}_fields'.format(name), []):
            if field in d and isinstance(d[field], basestring):
                d[field] = func(d[field])


def _get_call_class(method):
    """Find the call class for method if it exists else create one."""
    call_base, call_name = method.split('.', 1)
    # import the call class's module
    mod = __import__('ubersmith.calls.{0}'.format(call_base), fromlist=[''])
    # grab all the public members of the module
    gen = (getattr(mod, x) for x in dir(mod) if not x.startswith('_'))
    # filter them down to subclasses of BaseCall
    gen = (x for x in gen if type(x) is type and issubclass(x, BaseCall))
    # return first one that matches our method
    for call_class in gen:
        if call_class.method == method:
            return call_class
    else:
        class GenericCall(BaseCall):
            method = '.'.join((call_base, call_name))
        return GenericCall


def _make_generic_call(call_class):
    """Create a call function that is lexically bound to use call_class."""
    def generic_call(request_handler=None, **kwargs):
        return call_class(kwargs, request_handler).render()
    return generic_call


def generate_generic_calls(base, ns):
    # get all valid methods with base
    methods = (m for m in METHODS if m.split('.', 1)[0] == base)
    for method in methods:
        call_name = method.split('.', 1)[1]
        if call_name not in ns:
            # find the appropriate class
            call_class = _get_call_class(method)
            # create a call function and stick it in the namespace
            generic_call = _make_generic_call(call_class)
            generic_call.__name__ = str(call_name)
            generic_call.__doc__ = METHODS[method]
            # TODO this may or may not be a good idea, see:
            # http://stackoverflow.com/questions/10113892/semantics-of-module
            # generic_call.__module__ = 'ubersmith.{0}'.format(base)
            ns[call_name] = generic_call
            # add call to __all__ if needed
            if '__all__' in ns and call_name not in ns['__all__']:
                ns['__all__'].append(call_name)
        else:
            if not ns[call_name].__doc__:
                ns[call_name].__doc__ = METHODS[method]

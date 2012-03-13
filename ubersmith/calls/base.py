"""Base classes for all other calls."""

from collections import namedtuple
import copy
import datetime
from decimal import Decimal
import re
import rfc822
import time

from decorator import decorator
import phpserialize

from ubersmith.api import get_default_request_handler
from ubersmith.exceptions import ValidationError, ValidationErrorDefault
from ubersmith.utils import signature_position

__all__ = [
    'BaseCall',
    'FlatCall',
    'GroupCall',
    'FileCall',
    'api_call',
]

_CLEANERS = {
    'int': int,
    'decimal': lambda x: Decimal(x.replace(',', '')),
    'float': float,
    'timestamp': lambda x: datetime.datetime.fromtimestamp(float(x)),
    'date': lambda x: datetime.date(*time.strptime(x, '%b/%d/%Y')[:3]),
    'php_serialized': phpserialize.loads,
}
_UbersmithFile = namedtuple('UbersmithFile', ['filename', 'type',
                                              'modified', 'data'])


class _AbstractCall(object):
    method = None  # this should be defined on child classes

    def __init__(self, request_handler):
        """Setup call with provided request_handler."""
        self.request_handler = request_handler  # processes the request
        self.request_data = None  # data for the request is stored here
        self.response_data = None  # response data is stored here
        self.cleaned = None  # cleaned response data is stored here

    def process_request(self):
        """Return result of processing call."""
        return self.request_handler.process_request(self.method, self.request_data)

    def render(self):
        """Validate, process, clean and return the result of the call."""
        try:
            valid = self.validate()
        except ValidationErrorDefault, exc:
            return exc.default
        else:
            if not valid:
                raise ValidationError

        self.build_request_data()
        self.request()
        self.clean()

        return self.cleaned

    def validate(self):
        """Validate request data before sending it out. Return True/False."""
        raise NotImplementedError(
            "No validate method defined for {0}".format(self.__class__))

    def build_request_data(self):
        """Setup request data as a dict ready to urlencode."""
        raise NotImplementedError(
            "No build_request_data method defined for {0}".format(
                self.__class__))

    def request(self):
        """Make the request, handle any exceptions."""
        raise NotImplementedError(
            "No request method defined for {0}".format(self.__class__))

    def clean(self):
        """Clean response data."""
        raise NotImplementedError(
            "No clean method defined for {0}".format(self.__class__))


class BaseCall(_AbstractCall):
    def validate(self):
        """Sensible default behavior for validation."""
        return True

    def build_request_data(self):
        """Sensible default behavior for building request data."""
        if not hasattr(self, 'request_data'):
            self.request_data = None

    def request(self):
        """Sensible default behavior for request."""
        self.response_data = self.process_request()

    def clean(self):
        """Sensible default behavior for clean."""
        self.cleaned = copy.deepcopy(self.response_data)


class _CleanFieldsCall(BaseCall):
    rename_fields = {}  # fields to rename
    int_fields = []  # fields to convert to ints
    decimal_fields = []  # fields to convert to decimals
    float_fields = []   # fields to convert to floats
    timestamp_fields = []  # fields to convert to timestamps
    date_fields = []  # fields to convert to datetime.date
    php_serialized_fields = []  # fields to convert from php serialized format

    def clean_fields(self, struct):
        for old, new in self.rename_fields.iteritems():
            _clean_rename(struct, old, unicode(new))

        for name, method in _CLEANERS.iteritems():
            fields = getattr(self, name + '_fields', [])
            for field in fields:
                _clean_field(struct, field, method)


class FlatCall(_CleanFieldsCall):
    def clean(self):
        super(FlatCall, self).clean()
        self.clean_fields(self.cleaned)


class GroupCall(_CleanFieldsCall):
    def clean(self):
        super(GroupCall, self).clean()

        for key in self.response_data.iterkeys():
            _clean_rename(self.cleaned, key, int(key))

        for struct in self.cleaned.itervalues():
            self.clean_fields(struct)


class FileCall(BaseCall):
    def process_request(self):
        """Return result of processing call."""
        return self.request_handler.process_request(self.method,
                                                    self.request_data,
                                                    raw=True)

    def clean(self):
        fname = None
        disposition = self.response_data[0].get('content-disposition')
        if disposition:
            fname = re.search(r'filename="(.+?)"', disposition, re.I).group(1)
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

        self.cleaned = _UbersmithFile(self.filename, self.type, self.modified,
                                      self.data)


def _clean_field(struct, field, clean_func):
    if field in struct and isinstance(struct[field], basestring):
        struct[field] = clean_func(struct[field])


def _clean_rename(struct, old_name, new_name):
    if old_name in struct and new_name not in struct:
        struct[new_name] = struct[old_name]
        del struct[old_name]


def _api_call_wrapper(call_func, *args):
    """If caller did not provide a request_handler, use the default."""
    index = signature_position(call_func, 'request_handler')
    args = list(args)  # convert tuple to a mutable type
    args[index] = args[index] or get_default_request_handler()


def api_call(call_func):
    """Decorate API call function."""
    return decorator(_api_call_wrapper, call_func)

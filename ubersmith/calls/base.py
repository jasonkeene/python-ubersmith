# the base classes for all other calls go here

import copy
from datetime import datetime
from decimal import Decimal

from decorator import decorator
import phpserialize

from ubersmith.api import get_default_request_handler
from ubersmith.exceptions import UbersmithRequestValidationError
from ubersmith.utils import signature_position

__all__ = [
    'BaseCall',
    'api_call',
]

# ways calls may differ:
#     method string - class / instance property
#     input signature - function / class __init__ method
#     input validation - class validate method
#     input encoding - actually handled in request_handler not call
#     response cleaning - class clean method
#     documentation - function docstring


class _AbstractCall(object):
    method = None  # this should be defined on child classes

    def __init__(self, request_handler):
        """Setup call with provided request_handler."""
        self.request_handler = request_handler  # processes the request
        self.request_data = None  # data for the request is stored here
        self.response_data = None  # response data is stored here
        self.cleaned = None  # cleaned response data is stored here

    def process(self):
        """Return result of processing call."""
        return self.request_handler.process(self.method, self.request_data)

    def render(self):
        """Validate, process, clean and return the result of the call."""
        if not self.validate():
            raise UbersmithRequestValidationError

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
    def request(self):
        """Sensible default behavior for request."""
        self.response_data = self.process()

    def clean(self):
        """Sensible default behavior for clean."""
        self.cleaned = copy.deepcopy(self.response_data)


class FlatCall(BaseCall):
    rename_fields = {}  # fields to rename
    int_fields = ()  # fields to convert to ints
    decimal_fields = ()  # fields to convert to decimals
    float_fields = ()   # fields to convert to floats
    timestamp_fields = ()  # fields to convert to timestamps
    php_serialized_fields = ()  # fields to convert from php serialized format

    def clean(self):
        super(FlatCall, self).clean()

        map(self.clean_unicode_key, self.cleaned.keys())
        map(self.clean_rename, self.rename_fields.items())
        map(self.clean_int, self.int_fields)
        map(self.clean_decimal, self.decimal_fields)
        map(self.clean_float, self.float_fields)
        map(self.clean_timestamp, self.timestamp_fields)
        map(self.clean_php_serialize, self.php_serialized_fields)

    def clean_unicode_key(self, key):
        if isinstance(key, unicode):
            tmp_ref = self.cleaned[key]
            del self.cleaned[key]
            self.cleaned[str(key)] = tmp_ref

    def clean_rename(self, key_pair):
        old_key, new_key = key_pair
        if old_key in self.cleaned and new_key not in self.cleaned:
            self.cleaned[new_key] = self.cleaned[old_key]
            del self.cleaned[old_key]

    def clean_field(self, field, func):
        if field in self.cleaned:
            self.cleaned[field] = func(self.cleaned[field])

    def clean_int(self, field):
        self.clean_field(field, int)

    def clean_decimal(self, field):
        self.clean_field(field, lambda x: Decimal(str(x).replace(',', '')))

    def clean_float(self, field):
        self.clean_field(field, float)

    def clean_timestamp(self, field):
        self.clean_field(field, lambda x: datetime.fromtimestamp(float(x)))

    def clean_php_serialize(self, field):
        self.clean_field(field, phpserialize.loads)


class FileCall(BaseCall):
    pass


def _api_call_wrapper(call_func, *args):
    """If caller did not provide a request_handler, use the default."""
    index = signature_position(call_func, 'request_handler')
    args = list(args)  # convert tuple to a mutable type
    args[index] = args[index] or get_default_request_handler()

    return call_func(*args)


def _api_call_definition_check(call_func):
    """Check that call_func accepts a request_handler argument."""
    try:
        signature_position(call_func, 'request_handler')
    except ValueError:
        raise Exception("API call '{0}' defined without a request_handler " \
                                      "argument.".format(call_func.func_name))


def api_call(call_func):
    """Decorate API call function."""
    _api_call_definition_check(call_func)

    return decorator(_api_call_wrapper, call_func)

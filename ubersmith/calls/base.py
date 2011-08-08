# the base classes for all other calls go here

import datetime as _datetime
import decimal as _decimal
import inspect as _inspect

import phpserialize as _phpserialize

import ubersmith.api as _api
from decorator import decorator as _wrap


# ways calls may differ:
#     method string - class / instance property
#     input signature - function / class __init__ method
#     input validation - class validate method
#     input encoding - actually handled in request_handler not call
#     response cleaning - class clean method
#     documentation - function docstring


class BaseCall(object):
    method = None  # this should be defined on child classes
    rename_fields = {}  # fields to rename
    int_fields = ()  # fields to convert to ints
    decimal_fields = ()  # fields to convert to decimals
    float_fields = ()   # fields to convert to floats
    timestamp_fields = ()  # fields to convert to timestamps
    php_serialized_fields = ()  # fields to convert from php serialized format

    def __init__(self, request_handler):
        self.request_handler = request_handler

    def validate(self):
        raise NotImplementedError(
            "No validate method defined for {0}".format(self.__class__))

    def build_request_data(self):
        raise NotImplementedError(
            "No build_request_data method defined for {0}".format(
                self.__class__))

    def request(self):
        raise NotImplementedError(
            "No request method defined for {0}".format(self.__class__))

    def clean(self, field_cleaning=False):
        self.clean_unicode_keys()

        if self.rename_fields:
            self.clean_rename()
            field_cleaning = True
        if self.int_fields:
            self.clean_ints()
            field_cleaning = True
        if self.decimal_fields:
            self.clean_decimals()
            field_cleaning = True
        if self.float_fields:
            self.clean_floats()
            field_cleaning = True
        if self.timestamp_fields:
            self.clean_timestamps()
            field_cleaning = True
        if self.php_serialized_fields:
            self.clean_php_serialize()
            field_cleaning = True

        if not field_cleaning:
            raise NotImplementedError(
                "No clean method defined for {0}".format(self.__class__))
        else:
            return self.process_result

    def clean_unicode_keys(self):
        for key in self.process_result.keys():
            if isinstance(key, unicode):
                tmp_value = self.process_result[key]
                del self.process_result[key]
                self.process_result[str(key)] = tmp_value

    def clean_rename(self):
        for old_key, new_key in self.rename_fields.items():
            if old_key in self.process_result and \
                                           new_key not in self.process_result:
                self.process_result[new_key] = self.process_result[old_key]
                del self.process_result[old_key]

    def clean_ints(self):
        for field in self.int_fields:
            if field in self.process_result:
                self.process_result[field] = int(self.process_result[field])

    def clean_decimals(self):
        for field in self.decimal_fields:
            if field in self.process_result:
                self.process_result[field] = _decimal.Decimal(
                            str(self.process_result[field]).replace(',', ''))

    def clean_floats(self):
        for field in self.float_fields:
            if field in self.process_result:
                self.process_result[field] = float(self.process_result[field])

    def clean_timestamps(self):
        for field in self.timestamp_fields:
            if field in self.process_result:
                self.process_result[field] = \
                    _datetime.datetime.fromtimestamp(
                        float(self.process_result[field]))

    def clean_php_serialize(self):
        for field in self.php_serialized_fields:
            if field in self.process_result:
                self.process_result[field] = \
                    _phpserialize.loads(self.process_result[field])

    def process(self):
        return self.request_handler.process(self.method, self.request_data)

    def render(self):
        if not self.validate():
            return False

        self.build_request_data()
        self.request()
        return self.clean()


def _signature_position(func, arg_name):
    """Look at func's signature and return the position of arg_name."""
    return _inspect.getargspec(func).args.index(arg_name)


def _api_call_wrapper(call_func, *args):
    """If caller did not provide a request_handler, use the default."""
    index = _signature_position(call_func, 'request_handler')
    args = list(args)  # convert tuple to a mutable type
    args[index] = args[index] or _api.get_default_request_handler()

    return call_func(*args)


def _api_call_definition_check(call_func):
    """Check that call_func accepts a request_handler argument."""
    try:
        _signature_position(call_func, 'request_handler')
    except ValueError:
        raise Exception("API call '{0}' defined without a request_handler " \
                                      "argument.".format(call_func.func_name))


def api_call(call_func):
    """Decorate API call function."""
    _api_call_definition_check(call_func)

    return _wrap(_api_call_wrapper, call_func)

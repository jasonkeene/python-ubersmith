import datetime
import six
import time
from decimal import Decimal
try:
    import __builtin__ as builtins
except ImportError:  # pragma: no cover
    import builtins

import phpserialize


_CLEANERS = {}


def cleaner(func):
    _CLEANERS[func.__name__] = func
    return func


@cleaner
def php(val):
    return phpserialize.loads(val.encode("utf-8"))


@cleaner
def timestamp(val):
    return datetime.datetime.fromtimestamp(float(val))


@cleaner
def date(val):
    return datetime.date(*time.strptime(val, '%b/%d/%Y')[:3])


@cleaner
def decimal(val):
    if val is None:
        return None
    if isinstance(val, six.string_types):
        val = val.replace(',', '')
        if val.strip() == '':
            return None
    return Decimal(val)


@cleaner
def int(val):
    if val is None:
        return None
    if isinstance(val, six.string_types):
        val = val.replace(',', '')
        if val.strip() == '':
            return None
    return builtins.int(val)


class clean(object):
    def __init__(self, cleaner, keys=None, values=None, raises=False):
        self.cleaner = cleaner if callable(cleaner) else _CLEANERS[cleaner]
        if keys is not None and not callable(keys):
            if type(keys) is dict:
                for k, v in keys.items():
                    keys[k] = v if callable(v) else _CLEANERS[v]
            else:
                keys = _CLEANERS[keys]
        self.keys = keys
        # TODO: write tighter tests to cover these branches
        if values is not None and not callable(values):
            if type(values) is dict:
                for k, v in values.items():
                    values[k] = v if callable(v) else _CLEANERS[v]
            else:
                values = _CLEANERS[values]
        self.values = values
        self.raises = raises

    def __call__(self, val):
        val = self.cleaner(val)
        if self.cleaner is list:
            val = self._clean_list(val)
        elif self.cleaner is dict:
            val = self._clean_dict(val)
        return val

    def _clean_list(self, val):
        # TODO: factor keys/values cleaning out to methods
        # clean values
        if self.values is not None:
            if callable(self.values):
                # apply cleaner to all elements
                cleaner = self.values
                for i, element in enumerate(val):
                    val[i] = cleaner(element)
            else:
                # apply cleaners to specific values
                for i, cleaner in self.values.items():
                    try:
                        val[i] = cleaner(val[i])
                    except IndexError as e:
                        if self.raises:
                            raise e
        return val

    def _clean_dict(self, val):
        # TODO: factor keys/values cleaning out to methods
        # clean keys
        if self.keys is not None:
            tmp = {}
            if callable(self.keys):
                # apply cleaner to all keys
                cleaner = self.keys
                for k, v in val.items():
                    tmp[cleaner(k)] = v
            else:
                # apply cleaners to specific keys
                for k, v in val.items():
                    cleaner = self.keys.get(k, lambda x: x)
                    tmp[cleaner(k)] = val[k]
            val = tmp

        # TODO: factor keys/values cleaning out to methods
        # clean values
        if self.values is not None:
            if callable(self.values):
                # apply cleaner to all elements
                cleaner = self.values
                for k, v in val.items():
                    val[k] = cleaner(val[k])
            else:
                # apply cleaners to specific values
                for k, cleaner in self.values.items():
                    try:
                        val[k] = cleaner(val[k])
                    except KeyError as e:
                        if self.raises:
                            raise e
        return val

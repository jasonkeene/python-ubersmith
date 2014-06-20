"""Utility functions used throughout ubersmith library."""
import inspect
try:
    from collections.abc import MutableSequence, MutableMapping
except ImportError:  # pragma: no cover
    from collections import MutableSequence, MutableMapping
try:
    from urllib import parse as urlparse
except ImportError:  # pragma: no cover
    import urlparse
try:
    from urllib.parse import urlencode
except ImportError:  # pragma: no cover
    from urllib import urlencode

from six import string_types, text_type

__all__ = [
    'append_qs',
    'urlencode_unicode',
    'to_nested_php_args',
    'prepend_base',
    'isdict',
    'islist',
    'isstr',
    'get_filename'
]


def append_qs(url, query_string):
    """Append query_string values to an existing URL and return it as a string.

    query_string can be:
        * an encoded string: 'test3=val1&test3=val2'
        * a dict of strings: {'test3': 'val'}
        * a dict of lists of strings: {'test3': ['val1', 'val2']}
        * a list of tuples: [('test3', 'val1'), ('test3', 'val2')]

    """
    parsed_url = urlparse.urlsplit(url)
    parsed_qs = urlparse.parse_qsl(parsed_url.query, True)

    if isstr(query_string):
        parsed_qs += urlparse.parse_qsl(query_string)
    elif isdict(query_string):
        for item in query_string.items():
            if islist(item[1]):
                for val in item[1]:
                    parsed_qs.append((item[0], val))
            else:
                parsed_qs.append(item)
    elif islist(query_string):
        parsed_qs += query_string
    else:
        raise TypeError('Unexpected query_string type')

    return urlparse.urlunsplit((
        parsed_url.scheme,
        parsed_url.netloc,
        parsed_url.path,
        urlencode_unicode(parsed_qs),
        parsed_url.fragment,
    ))


def urlencode_unicode(data, doseq=0):
    """urllib.urlencode can't handle unicode, this is a hack to fix it."""
    data_iter = None
    if isdict(data):
        data_iter = data.items()
    elif islist(data):
        data_iter = data

    if data_iter:
        for i, (key, value) in enumerate(data_iter):
            if isinstance(value, text_type):
                # try to convert to str
                try:
                    safe_val = str(value)
                except UnicodeEncodeError:
                    # try to encode as utf-8
                    # if an exception is raised here then idk what to do
                    safe_val = value.encode('utf-8')
                finally:
                    if isdict(data):
                        data[key] = safe_val
                    else:
                        data[i] = (key, safe_val)

    return urlencode(data, doseq=doseq)


def _is_leaf(value):
    """Return if a value is a leaf to an existing object"""
    return not (isdict(value) or islist(value))


def to_nested_php_args(data, prefix_key=None):
    """
    This function will take either a dict or list and will recursively loop
    through the values converting it into a format similar to a PHP array which
    Ubersmith requires for the info portion of the API's order.create method.
    """
    is_root = prefix_key is None
    prefix_key = prefix_key if prefix_key else ''

    if islist(data):
        data_iter = data if is_root else enumerate(data)
        new_data = [] if is_root else {}
    elif isdict(data):
        data_iter = data.items()
        new_data = {}
    else:
        raise TypeError('expected dict or list, got {0}'.format(type(data)))

    if islist(new_data):
        def data_set(k, v):
            new_data.append((k, v))
        def data_update(d):
            for k, v in d.items():
                new_data.append((k, v))
    else:
        def data_set(k, v):
            new_data[k] = v
        data_update = new_data.update

    for key, value in data_iter:
        end_key = prefix_key + (str(key) if is_root else '[{0}]'.format(key))
        if _is_leaf(value):
            data_set(end_key, value)
        else:
            nested_args = to_nested_php_args(value, end_key)
            data_update(nested_args)

    return new_data


def prepend_base(base):
    """Return a callable that will prepend the base of a method string."""
    return lambda call: '.'.join((base, call))


def isdict(value):
    """Return true if the value behaves like a dict, false if not."""
    return isinstance(value, MutableMapping)


def islist(value):
    """Return true if the value behaves like a list, false if not."""
    return isinstance(value, MutableSequence)


def isstr(value):
    """Return true if the value behaves like a string, false if not."""
    return isinstance(value, string_types)


def get_filename(disposition):
    """Parse Content-Disposition header to pull out the filename bit.

    See: http://tools.ietf.org/html/rfc2616#section-19.5.1

    """
    if disposition:
        params = [param.strip() for param in disposition.split(';')[1:]]
        for param in params:
            if '=' in param:
                name, value = param.split('=', 1)
                if name == 'filename':
                    return value.strip('"')

"""Utility functions used throughout ubersmith library."""

import inspect
import urllib
import urlparse

__all__ = [
    'append_qs',
    'urlencode_unicode',
    'prepend_base',
    'isdict',
    'islist',
    'isstr',
    'signature_position',
]


def append_qs(url, query_string):
    """Append query_string values to an existing URL and return it as a string.

    query_string can be:
        * an encoded string: 'test3=val1&test3=val2'
        * a dict of strings: {'test3': 'val'}
        * a dict of lists of strings: {'test3': ['val1', 'val2']}
        * a list of tuples: [('test3', 'val1'), ('test3', 'val2')]

    >>> url = 'http://domain.tld/path/?test1=val&test2#hash'
    >>> qs = {'test3': 'val'}
    >>> append_qs(url, qs)
    'http://domain.tld/path/?test1=val&test2=&test3=val#hash'

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
        raise ValueError('Unexpected query_string value')

    return urlparse.urlunsplit((
        parsed_url.scheme,
        parsed_url.netloc,
        parsed_url.path,
        urlencode_unicode(parsed_qs),
        parsed_url.fragment,
    ))


# TODO this should match the same input as urllib.urlencode so it can be used
# as a drop in replacement
def urlencode_unicode(data):
    """urllib.urlencode can't handle unicode, this is a hack to fix it."""
    data_iter = None
    if isdict(data):
        data_iter = data.iteritems()
    elif islist(data):
        data_iter = data

    if data_iter:
        for i, (key, value) in enumerate(data_iter):
            if isinstance(value, unicode):
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
                    elif islist(data):
                        data[i] = (key, safe_val)

    return urllib.urlencode(data)


def prepend_base(base):
    """Return a callable that will prepend the base of a method string."""
    return lambda call: '.'.join((base, call))


# TODO check against ABCs instead of hasattr
def isdict(value):
    """Return true if the value behaves like a dict, false if not."""
    return hasattr(value, 'keys') and hasattr(value, '__getitem__')


# TODO check against ABCs instead of hasattr
def islist(value):
    """Return true if the value behaves like a list, false if not."""
    return hasattr(value, 'append') and hasattr(value, '__getitem__')


def isstr(value):
    """Return true if the value behaves like a string, false if not."""
    return isinstance(value, basestring)


def signature_position(func, arg_name):
    """Look at func's signature and return the position of arg_name."""
    return inspect.getargspec(func).args.index(arg_name)

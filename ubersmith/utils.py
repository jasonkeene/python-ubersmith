# utility functions

import inspect
import urllib
import urlparse

__all__ = [
    'append_qs',
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
    >>> string_qs = 'test3=val1&test3=val2'
    >>> dict_qs = {'test3': 'val'}
    >>> nested_dict_qs = {'test3': ['val1', 'val2']}
    >>> list_qs = [('test3', 'val1'), ('test3', 'val2')]
    >>> append_qs(url, string_qs)
    'http://domain.tld/path/?test1=val&test2=&test3=val1&test3=val2#hash'
    >>> append_qs(url, dict_qs)
    'http://domain.tld/path/?test1=val&test2=&test3=val#hash'
    >>> append_qs(url, nested_dict_qs)
    'http://domain.tld/path/?test1=val&test2=&test3=val1&test3=val2#hash'
    >>> append_qs(url, list_qs)
    'http://domain.tld/path/?test1=val&test2=&test3=val1&test3=val2#hash'

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
        urllib.urlencode(parsed_qs),
        parsed_url.fragment,
    ))


def prepend_base(method, base):
    """Prepend a method call with a base."""
    return '.'.join((base, method))
prepend_base.init = lambda init: lambda method: prepend_base(method, init)


# TODO check against ABCs instead of hasattr

def isdict(value):
    """Return true if the value behaves like a dict, false if not."""
    return hasattr(value, 'keys') and hasattr(value, '__getitem__')


def islist(value):
    """Return true if the value behaves like a list, false if not."""
    return hasattr(value, 'append') and hasattr(value, '__getitem__')


def isstr(value):
    """Return true if the value behaves like a string, false if not."""
    return isinstance(value, basestring)


def signature_position(func, arg_name):
    """Look at func's signature and return the position of arg_name."""
    return inspect.getargspec(func).args.index(arg_name)

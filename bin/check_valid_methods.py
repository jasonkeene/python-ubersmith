#!/usr/bin/env python
"""Script to check for outdated VALID_METHODS."""

from ubersmith.api import (
    VALID_METHODS,
    TestRequestHandler,
    set_default_request_handler
)
from ubersmith import uber


def main():
    set_default_request_handler(TestRequestHandler())
    old = set(VALID_METHODS)
    new = set(uber.method_list().keys())

    if new - old:
        print
        print 'New Methods:'
        print
        print '['
        for method in new - old:
            print "    '{}',".format(method)
        print ']'

    if old - new:
        print
        print 'Outdated Methods:'
        print
        print '['
        for method in old - new:
            print "    '{}',".format(method)
        print ']'


if __name__ == '__main__':
    main()

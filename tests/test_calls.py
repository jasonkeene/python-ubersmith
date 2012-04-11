"""Generic tests for calls."""

import sys

from ubersmith.api import METHODS
from ubersmith.utils import signature_position


def setup():
    """Import all call modules."""
    bases = set(method.split('.', 1)[0] for method in METHODS)
    for base in bases:
        mod_name = u'ubersmith.{0}'.format(base)
        if not sys.modules.get(mod_name):
            __import__(mod_name)


def test_method_exists():
    """Check that call is implemented."""
    for base, call in (method.split('.', 1) for method in METHODS):
        mod_name = u'ubersmith.{0}'.format(base)
        def check(base, call):
            assert hasattr(sys.modules[mod_name], call)
        yield check, base, call


def test_method_signature():
    """Check that call accepts a request_handler."""
    for base, call in (method.split('.', 1) for method in METHODS):
        mod_name = u'ubersmith.{0}'.format(base)
        def check(base, call):
            call_func = getattr(sys.modules[mod_name], call)
            try:
                signature_position(call_func, 'request_handler')
            except ValueError:
                err_msg = u"API call '{}' defined without a request_handler."
                assert False, err_msg.format(call_func.func_name)
        yield check, base, call

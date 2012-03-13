"""Generic tests for calls."""

import sys

from nose.exc import SkipTest

from ubersmith.api import VALID_METHODS
from ubersmith.utils import signature_position


def test_methods():
    """Generator to create tests for all VALID_METHODS."""
    for module, call in (method.split('.', 1) for method in VALID_METHODS):
        yield check_implemented, module, call


def check_implemented(module, call):
    """Check that call is implemented and accepts a request_handler."""
    mod_name = 'ubersmith.' + module

    # import module if it isn't already
    if not sys.modules.get(mod_name):
        __import__(mod_name)

    # check if call is implemented
    if not hasattr(sys.modules[mod_name], call):
        raise SkipTest(u"{}.{} is not implemented.".format(module, call))

    # check that it accepts a request_handler
    call_func = getattr(sys.modules[mod_name], call)
    try:
        signature_position(call_func, 'request_handler')
    except ValueError:
        err_msg = u"API call '{}' defined without a request_handler."
        assert False, err_msg.format(call_func.func_name)

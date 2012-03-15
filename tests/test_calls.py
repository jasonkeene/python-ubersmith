"""Generic tests for calls."""

import sys

from ubersmith.api import VALID_METHODS
from ubersmith.utils import signature_position


def setup():
    """Import all call modules."""
    call_mods = {u'ubersmith.{}'.format(method.split('.', 1)[0]) for method in
                                                                VALID_METHODS}
    for mod_name in call_mods:
        if not sys.modules.get(mod_name):
            __import__(mod_name)


def test_method_exists():
    """Check that call is implemented."""
    for module, call in (method.split('.', 1) for method in VALID_METHODS):
        mod_name = u'ubersmith.{}'.format(module)
        def check(module, call):
            assert hasattr(sys.modules[mod_name], call)
        yield check, module, call


def test_method_signature():
    """Check that call accepts a request_handler."""
    for module, call in (method.split('.', 1) for method in VALID_METHODS):
        mod_name = u'ubersmith.{}'.format(module)
        def check(module, call):
            call_func = getattr(sys.modules[mod_name], call)
            try:
                signature_position(call_func, 'request_handler')
            except ValueError:
                err_msg = u"API call '{}' defined without a request_handler."
                assert False, err_msg.format(call_func.func_name)
        yield check, module, call

import sys

import pytest

from ubersmith.api import METHODS
from ubersmith.utils import signature_position


def setup_module(module):
    """Import all call modules."""
    bases = set(method.split('.', 1)[0] for method in METHODS)
    for base in bases:
        mod_name = '.'.join(['ubersmith', base])
        if not sys.modules.get(mod_name):
            __import__(mod_name)


@pytest.mark.parametrize('method', METHODS)
def test_method_exists(method):
    base, call = method.split('.', 1)
    mod_name = '.'.join(['ubersmith', base])
    assert hasattr(sys.modules[mod_name], call)


@pytest.mark.parametrize('method', METHODS)
def test_method_signature(method):
    base, call = method.split('.', 1)
    mod_name = '.'.join(['ubersmith', base])
    call_func = getattr(sys.modules[mod_name], call)
    assert signature_position(call_func, 'request_handler') == 0

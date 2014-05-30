import sys

import pytest

from ubersmith.api import METHODS
from ubersmith.utils import signature_position
from ubersmith.calls import generate_generic_calls


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


class DescribeGenerateGenericCalls:
    def it_creates_call_funcs(self):
        base = 'uber'
        namespace = {}
        generate_generic_calls(base, namespace)
        base_funcs = (m.split('.', 1)[1] for m in METHODS if m.startswith(base))
        assert sorted(namespace.keys()) == list(sorted(base_funcs))

    def it_adds_func_names_to_all(self):
        base = 'uber'
        namespace = {'__all__': []}
        generate_generic_calls(base, namespace)
        base_funcs = (m.split('.', 1)[1] for m in METHODS if m.startswith(base))
        assert sorted(namespace['__all__']) == list(sorted(base_funcs))

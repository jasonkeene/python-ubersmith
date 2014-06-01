import sys

from mock import Mock
import pytest

from ubersmith.api import METHODS
from ubersmith.utils import signature_position
from ubersmith.calls import generate_generic_calls
from ubersmith import uber, order


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

    def it_adds_doc_string_to_funcs_that_already_exist(self):
        func = lambda: None
        base = 'uber'
        namespace = {'method_list': func}
        generate_generic_calls(base, namespace)
        assert namespace['method_list'].__doc__ == METHODS['uber.method_list']

    def it_does_not_add_doc_string_to_funcs_that_already_have_them(self):
        func = lambda: None
        func.__doc__ = 'foobar'
        base = 'uber'
        namespace = {'method_list': func}
        generate_generic_calls(base, namespace)
        assert namespace['method_list'].__doc__ == 'foobar'


def test_json_call():
    handler = Mock()
    handler.process_request.return_value = {"test": "blah"}
    assert uber.method_list(request_handler=handler) == {"test": "blah"}


def test_group_call():
    handler = Mock()
    handler.process_request.return_value = {"1": {"test": "blah"}}
    assert order.list(request_handler=handler) == {1: {"test": "blah"}}


def test_file_call():
    handler = Mock()
    response = Mock()
    response.content = 'bytes here'
    response.headers = {}
    handler.process_request.return_value = response
    uber_file = uber.documentation(request_handler=handler)
    assert uber_file.data == 'bytes here'

import datetime
from decimal import Decimal
import json
import sys

from mock import Mock
import pytest

from ubersmith.api import METHODS, BaseResponse
from ubersmith.calls import generate_generic_calls
from ubersmith.clean import _CLEANERS
from ubersmith.exceptions import ValidationError
from ubersmith import uber, order


def setup_module(module):
    """Import all call modules."""
    bases = set(method.split('.', 1)[0] for method in METHODS)
    for base in bases:
        mod_name = '.'.join(['ubersmith', base])
        if not sys.modules.get(mod_name):
            __import__(mod_name)


def make_base_response(data):
    response = Mock()
    response.headers = {
        'content-type': 'application/json',
    }
    response.json.return_value = {
        "status": True,
        "error_code": None,
        "error_message": "",
        "data": data,
    }
    return BaseResponse(response)


@pytest.mark.parametrize('method', METHODS)
def test_method_exists(method):
    base, call = method.split('.', 1)
    mod_name = '.'.join(['ubersmith', base])
    assert hasattr(sys.modules[mod_name], call)


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
    data = {"test": "blah"}
    handler.process_request.return_value = make_base_response(data)
    assert dict(uber.method_list.handler(handler)()) == {"test": "blah"}


def test_group_call():
    handler = Mock()
    data = {"1": {"test": "blah"}}
    handler.process_request.return_value = make_base_response(data)
    assert dict(order.list.handler(handler)()) == {1: {"test": "blah"}}


def test_file_call():
    handler = Mock()
    response = Mock()
    response.content = 'bytes here'
    response.headers = {}
    handler.process_request.return_value = BaseResponse(response)
    uber_file = uber.documentation.handler(handler)()
    assert uber_file.data == 'bytes here'


def test_calls_validates_required_fields():
    with pytest.raises(ValidationError):
        order.queue_list.handler('bob')()


def test_calls_validates_or_required_fields():
    with pytest.raises(ValidationError):
        order.get.handler('bob')()


def dict_zip(*dicts):
    for key in set(dicts[0]).intersection(*dicts[1:]):
        yield tuple(d[key] for d in dicts)


# TODO: should bool cleaner clean '0' into False?
@pytest.mark.parametrize(['cleaner', 'value', 'result'], dict_zip(_CLEANERS, {
    'bool': '1',
    'int': '123',
    'decimal': '1,234.56',
    'float': '1.234',
    'timestamp': '123456789',
    'date': 'Aug/31/2011',
    'php_serialized': u'a:1:{s:4:"test";i:123;}',
}, {
    'bool': True,
    'int': 123,
    'decimal': Decimal('1234.56'),
    'float': 1.234,
    'timestamp': datetime.datetime.fromtimestamp(float('123456789')),
    'date': datetime.date(2011, 8, 31),
    'php_serialized': {b'test': 123},
}))
def test_cleaners(cleaner, value, result):
    assert cleaner(value) == result

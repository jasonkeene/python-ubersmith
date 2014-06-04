import json

import ubersmith
import ubersmith.api
import ubersmith.uber


def setup_module():
    ubersmith.init(**{
        'base_url': '',
        'username': '',
        'password': '',
    })


def teardown_module():
    ubersmith.api._DEFAULT_REQUEST_HANDLER = None


def test_responses_can_getitem(response):
    response.text = json.dumps({
        "status": True,
        "error_code": None,
        "error_message": "",
        "data": {
            "foo": "bar",
            "nested": {
                "baz": "qux",
            }
        },
    })
    result = ubersmith.uber.method_list()
    assert result["foo"] == "bar"
    assert result["nested"]["baz"] == "qux"


def test_responses_can_be_turned_into_dicts(response):
    response.text = json.dumps({
        "status": True,
        "error_code": None,
        "error_message": "",
        "data": {
            "foo": "bar",
        },
    })
    expected = {
        "foo": "bar",
    }
    assert dict(ubersmith.uber.method_list()) == expected

import json

from six import text_type

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
    resp_json = {
        "status": True,
        "error_code": None,
        "error_message": "",
        "data": {
            "foo": "bar",
            "nested": {
                "baz": "qux",
            }
        },
    }
    response.json.return_value = resp_json
    response.content = json.dumps(resp_json)
    response.text = text_type(response.content)
    result = ubersmith.uber.method_list()
    assert result["foo"] == "bar"
    assert result["nested"]["baz"] == "qux"


def test_responses_can_be_turned_into_dicts(response):
    resp_json = {
        "status": True,
        "error_code": None,
        "error_message": "",
        "data": {
            "foo": "bar",
        },
    }
    response.json.return_value = resp_json
    response.content = json.dumps(resp_json)
    response.text = text_type(response.content)
    expected = {
        "foo": "bar",
    }
    assert dict(ubersmith.uber.method_list()) == expected

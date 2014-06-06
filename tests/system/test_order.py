import datetime
from decimal import Decimal
import json

import ubersmith
import ubersmith.api


def setup_module():
    ubersmith.init(**{
        'base_url': '',
        'username': '',
        'password': '',
    })


def teardown_module():
    ubersmith.api._DEFAULT_REQUEST_HANDLER = None


def test_order_get(response):
    response.text = json.dumps({
        "status": True,
        "error_code": None,
        "error_message": "",
        "data": {
            "order_id": "60",
            "progress": {
                "1": {
                    "ts": "1272400333",
                },
                "2": {
                    "ts": "1272400333",
                },
                "3": {
                    "ts": "1272400333",
                },
            },
        },
    })
    expected = {
        u'order_id': 60,
        u'progress': {
            1: {
                "ts": datetime.datetime.fromtimestamp(float("1272400333")),
            },
            2: {
                "ts": datetime.datetime.fromtimestamp(float("1272400333")),
            },
            3: {
                "ts": datetime.datetime.fromtimestamp(float("1272400333")),
            },
        },
    }
    assert dict(ubersmith.order.get(order_id=60)) == expected


def test_order_list(response):
    response.text = json.dumps({
        "status": True,
        "error_code": None,
        "error_message": "",
        "data": {
            "60": {
                "order_id": "60",
                "client_id": "50",
                "activity": "1272400333",
                "ts": "1272400333",
                "total": "33.22",
            },
        },
    })
    expected = {
        60: {
            u'client_id': 50,
            u'activity': datetime.datetime.fromtimestamp(float("1272400333")),
            u'ts': datetime.datetime.fromtimestamp(float("1272400333")),
            u'total': Decimal('33.22'),
            u'order_id': 60,
        }
    }
    assert dict(ubersmith.order.list(client_id=50)) == expected

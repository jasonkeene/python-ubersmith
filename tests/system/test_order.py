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
            "order_status": "3",
            "client_id": "50",
            "order_form_id": "12",
            "order_queue_id": "4",
            "opportunity_id": "243",
            "total": "1,234.5",
            "activity": "1272400333",
            "ts": "1272400333",
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
        u'order_status': 3,
        u'client_id': 50,
        u'order_form_id': 12,
        u'order_queue_id': 4,
        u'opportunity_id': 243,
        u'total': Decimal('1234.5'),
        u'activity': datetime.datetime.fromtimestamp(float('1272400333')),
        u'ts': datetime.datetime.fromtimestamp(float('1272400333')),
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


def test_order_queue_list(response):
    response.text = json.dumps({
        "status": True,
        "error_code": None,
        "error_message": "",
        "data": {
            u'1': {
                u'name': u'Orders',
                u'steps': {
                    u'1': {u'count': u'10', u'name': u'foo'},
                    u'2': {u'count': u'20', u'name': u'bar'},
                    u'3': {u'count': u'30', u'name': u'baz'},
                },
            },
        },
    })
    expected = {
        1: {
            u'name': u'Orders',
            u'steps': {
                1: {u'count': 10, u'name': u'foo'},
                2: {u'count': 20, u'name': u'bar'},
                3: {u'count': 30, u'name': u'baz'},
            },
        },
    }
    assert dict(ubersmith.order.queue_list(brand_id=1)) == expected

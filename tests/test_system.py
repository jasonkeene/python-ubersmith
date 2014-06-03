import datetime
from decimal import Decimal
import json

from mock import Mock

import ubersmith
import ubersmith.api
import ubersmith.order


def setup_module():
    ubersmith.init(**{
        'base_url': '',
        'username': '',
        'password': '',
    })


def teardown_module():
    ubersmith.api._DEFAULT_REQUEST_HANDLER = None


def test_order_list(monkeypatch):
    requests = Mock()
    monkeypatch.setattr(ubersmith.api, 'requests', requests)
    response = Mock()
    response.headers = {
        'content-type': 'application/json',
    }
    response.text = json.dumps({
        "status": True,
        "error_code": None,
        "error_message": "",
        "data": {
            "60": {
                "client_id": "50",
                "activity": "1272400333",
                "ts": "1272400333",
                "total": "33.22",
                "order_id": "60",
            },
        },
    })
    requests.post.return_value = response
    expected = {
        60: {
            u'client_id': 50,
            u'activity': datetime.datetime.fromtimestamp(float("1272400333")),
            u'ts': datetime.datetime.fromtimestamp(float("1272400333")),
            u'total': Decimal('33.22'),
            u'order_id': 60,
        }
    }
    result = ubersmith.order.list(client_id=50)
    assert expected == result


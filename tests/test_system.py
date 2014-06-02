import datetime
from decimal import Decimal

from mock import Mock

import ubersmith.order

# TODO: setup/teardown module with default request handler
# TODO: mock out requests library vs mocking out request handler


def test_order_list():
    handler = Mock()
    response = {
        "60": {
            "client_id": "50",
            "activity": "1272400333",
            "ts": "1272400333",
            "total": "33.22",
            "order_id": "60",
        },
    }
    handler.process_request.return_value = response
    expected = {
        60: {
            u'client_id': 50,
            u'activity': datetime.datetime.fromtimestamp(float("1272400333")),
            u'ts': datetime.datetime.fromtimestamp(float("1272400333")),
            u'total': Decimal('33.22'),
            u'order_id': 60,
        }
    }
    result = ubersmith.order.list(client_id=50, request_handler=handler)
    assert expected == result

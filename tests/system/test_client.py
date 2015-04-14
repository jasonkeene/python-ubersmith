import datetime
from decimal import Decimal
import json

import pytest
from six import text_type

import ubersmith
import ubersmith.api
import ubersmith.client


def setup_module():
    ubersmith.init(**{
        'base_url': '',
        'username': '',
        'password': '',
    })


def teardown_module():
    ubersmith.api._DEFAULT_REQUEST_HANDLER = None


def test_get(response):
    resp_json = {
        "status": True,
        "error_code": None,
        "error_message": "",
        "data": {
            u'clientid': u'50',
            u'access': u'a:1:{s:4:"cbms";s:6:"client";}',
            u'active': u'1',
            u'balance': u'187559.67',
            u'class_id': u'1',
            u'created': u'1236056400',
            u'discount': u'100.00',
            u'latest_inv': u'1278014814',
            u'password_changed': u'1304603745',
            u'priority': u'1',
            u'tier_commission_rate': u'0.00',
            u'tier_commission': u'0.00',
            u'commission_rate': u'0.00',
            u'commission': u'0.00',
        },
    }
    response.json.return_value = resp_json
    response.content = json.dumps(resp_json)
    response.text = text_type(response.content)
    expected = {
        u'clientid': 50,
        u'access': {b'cbms': b'client'},
        u'active': True,
        u'balance': Decimal('187559.67'),
        u'class_id': 1,
        u'created': datetime.datetime.fromtimestamp(float('1236056400')),
        u'discount': Decimal('100.00'),
        u'latest_inv': datetime.datetime.fromtimestamp(float('1278014814')),
        u'password_changed': datetime.datetime.fromtimestamp(float('1304603745')),
        u'priority': 1,
        u'tier_commission_rate': Decimal('0.00'),
        u'tier_commission': Decimal('0.00'),
        u'commission_rate': Decimal('0.00'),
        u'commission': Decimal('0.00'),
    }
    assert dict(ubersmith.client.get(client_id=50)) == expected


def test_update(response):
    resp_json = {
        "status": True,
        "error_code": None,
        "error_message": "",
        "data": {},
    }
    response.json.return_value = resp_json
    response.content = json.dumps(resp_json)
    response.text = text_type(response.content)
    expected = {}
    result = ubersmith.client.get(client_id=50, email="bob@example.com")
    assert dict(result) == expected


def test_cc_add(response):
    resp_json = {
        "status": True,
        "error_code": None,
        "error_message": "",
        "data": u'123',
    }
    response.json.return_value = resp_json
    response.content = json.dumps(resp_json)
    response.text = text_type(response.content)
    expected = 123
    result = ubersmith.client.cc_add(cc_num='5454'*4, client_id=50)
    assert result == expected


def test_invoice_list(response):
    resp_json = {
        "status": True,
        "error_code": None,
        "error_message": "",
        "data": {
            "60": {
                u'invid': u'60',
                u'clientid': u'50',
                u'amount': u'50.00',
                u'amount_unpaid': u'0.00',
                u'date': u'1272400333',
                u'datepaid': u'1272400333',
                u'due': u'1272400333',
            },
        },
    }
    response.json.return_value = resp_json
    response.content = json.dumps(resp_json)
    response.text = text_type(response.content)
    expected = {
        60: {
            u'invid': 60,
            u'clientid': 50,
            u'amount': u'50.00',
            u'amount_unpaid': u'0.00',
            u'date': datetime.datetime.fromtimestamp(float("1272400333")),
            u'datepaid': datetime.datetime.fromtimestamp(float("1272400333")),
            u'due': datetime.datetime.fromtimestamp(float("1272400333")),
        }
    }
    assert dict(ubersmith.client.invoice_list(client_id=50)) == expected


def test_invoice_count(response):
    resp_json = {
        "status": True,
        "error_code": None,
        "error_message": "",
        "data": "42",
    }
    response.json.return_value = resp_json
    response.content = json.dumps(resp_json)
    response.text = text_type(response.content)
    assert int(ubersmith.client.invoice_count(client_id=50)) == 42


def test_invoice_get(response):
    resp_json = {
        "status": True,
        "error_code": None,
        "error_message": "",
        "data": {
            u'invid': u'60',
            u'clientid': u'50',
            u'date': u'1272400333',
            u'datepaid': u'1272400333',
            u'due': u'1272400333',
            u'overdue': u'1272400333',
        },
    }
    response.json.return_value = resp_json
    response.content = json.dumps(resp_json)
    response.text = text_type(response.content)
    expected = {
        u'invid': 60,
        u'clientid': 50,
        u'date': datetime.datetime.fromtimestamp(float("1272400333")),
        u'datepaid': datetime.datetime.fromtimestamp(float("1272400333")),
        u'due': datetime.datetime.fromtimestamp(float("1272400333")),
        u'overdue': datetime.datetime.fromtimestamp(float("1272400333")),
    }
    assert dict(ubersmith.client.invoice_get(invoice_id=60)) == expected


def test_invoice_get_pdf(response):
    response.headers = {
        'content-type': 'application/pdf',
        'content-disposition': 'inline; filename=Invoice-60.pdf'
    }
    response.text = u"Some PDF data."
    response.content = str(response.text)
    uberfile = ubersmith.client.invoice_get(invoice_id=60, format="pdf")
    assert uberfile.type == 'application/pdf'
    assert uberfile.filename == "Invoice-60.pdf"
    assert str(uberfile.data) == response.text


def test_invoice_get_pdf_without_disposition(response):
    response.headers = {
        'content-type': 'application/pdf',
    }
    response.text = u"Some PDF data."
    response.content = str(response.text)
    uberfile = ubersmith.client.invoice_get(invoice_id=60, format="pdf")
    assert uberfile.type == 'application/pdf'
    assert uberfile.filename is None
    assert str(uberfile.data) == response.text

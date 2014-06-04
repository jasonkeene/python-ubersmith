import datetime
import json

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


def test_invoice_list(response):
    response.text = json.dumps({
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
    })
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

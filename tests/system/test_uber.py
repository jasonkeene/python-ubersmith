import pytest

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


def test_uber_documentation(response):
    response.headers = {
        'content-type': 'application/pdf',
        'content-disposition': 'inline; filename="doc.pdf";'
    }
    response.text = u"Some PDF data."
    response.content = str(response.text)
    uberfile = ubersmith.uber.documentation()
    assert uberfile.type == 'application/pdf'
    assert uberfile.filename == "doc.pdf"
    assert str(uberfile.data) == response.text

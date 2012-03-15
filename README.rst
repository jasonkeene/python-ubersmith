
Installation
============

::

    pip install -e git+ssh://git@github.com/jasonkeene/python-ubersmith.git#egg=ubersmith

Example Use
===========

First you'll need to setup a request handler with your login credentials::

    from ubersmith.api import HttpRequestHandler, set_default_request_handler
    api_credentials = {
        'base_url': 'http://ubersmith/api/2.0/',
        'username': 'username',
        'password': 'password',
    }
    handler = HttpRequestHandler(**api_credentials)
    set_default_request_handler(handler)

Then you can make API calls::

    from ubersmith import uber
    uber.method_list()

These modules match the methods as documented in the `Ubersmith API 2.0 docs`_.

.. _Ubersmith API 2.0 docs: https://github.com/jasonkeene/python-ubersmith/raw/master/docs/ubersmith_api_docs.pdf

Running Tests
=============

::

    # cd to repository
    pip install -r test-requirements.txt
    nosetests

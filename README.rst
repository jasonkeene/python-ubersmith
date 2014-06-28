.. image:: https://img.shields.io/travis/jasonkeene/python-ubersmith.svg?style=flat
   :target: https://travis-ci.org/jasonkeene/python-ubersmith

.. image:: https://img.shields.io/coveralls/jasonkeene/python-ubersmith.svg?style=flat
   :target: https://coveralls.io/r/jasonkeene/python-ubersmith?branch=master

.. image:: https://img.shields.io/pypi/v/ubersmith.svg?style=flat
   :target: https://pypi.python.org/pypi/ubersmith

Installation
============

::

    pip install ubersmith

Example Use
===========

First you'll need to initialize the ubersmith package with your login credentials::

    import ubersmith
    ubersmith.init('http://ubersmith/api/2.0/', 'username', 'password')

Then you can make API calls::

    from ubersmith import uber, client
    uber.method_list()
    client.get(email='g.freeman@combineresearch.com')

These modules match the methods as documented in the `Ubersmith API 2.0 docs`_.

.. _Ubersmith API 2.0 docs: https://github.com/jasonkeene/python-ubersmith/raw/master/docs/ubersmith_api_docs.pdf

Without Module State
--------------------

ubersmith.init creates and stores a request handler with your login credentials.
If for some reason you'd prefer to not have this module state then you can
instantiate the request handler manually::

    from ubersmith.api import RequestHandler
    h = RequestHandler('http://ubersmith/api/2.0/', 'username', 'password')

and then explicitly pass it into any call function::

    from ubersmith import uber, client
    uber.method_list.handler(h)()
    client.get.handler(h)(email='g.freeman@combineresearch.com')

or you can access the call function directly on the handler and the handler
will be implicitly passed into the call function for you::

    h.uber.method_list()
    h.client.get(email='g.freeman@combineresearch.com')

Raw Processing
--------------

Alternatively you can process the request directly on the handler::

    h.process_request('uber.method_list')
    h.process_request('client.get', data={'email': 'g.freeman@combineresearch.com'})

although this will bypass any validation logic and response cleaning provided
by the call function and just return the BaseResponse from ubersmith.

Development
===========

You'll need to install the development dependencies::

    pip install -r requirements-dev.txt

Running Tests
-------------

To run the tests::

    py.test

To run the tests on multiple interpreters::

    tox

To run the tests and generate a coverage report::

    bin/coverage.sh

Console
-------

To run the dev console copy over the example config file::

    cp bin/config.py.example bin/config.py

Edit it with your credentials then run the console::

    python -i bin/console.py

From here you can run commands against your dev instance::

    >>> uber.method_list()

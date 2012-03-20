
Installation
============

::

    pip install -e git+ssh://git@github.com/jasonkeene/python-ubersmith.git#egg=ubersmith

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

    from ubersmith.api import HttpRequestHandler
    h = HttpRequestHandler('http://ubersmith/api/2.0/', 'username', 'password')

and then explicitly pass it into any call function::

    from ubersmith import uber, client
    uber.method_list(request_handler=h)
    client.get(email='g.freeman@combineresearch.com', request_handler=h)

or you can process the request directly on the handler::

    h.process_request('uber.method_list')
    h.process_request('client.get', data={'email': 'g.freeman@combineresearch.com'})

although this will bypass any validation logic and response cleaning and just
return the JSON data from the ubersmith response as a dict.

Running Tests
=============

::

    # cd to repository
    pip install -r test-requirements.txt
    ./runtests.py

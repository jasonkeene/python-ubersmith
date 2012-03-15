
Installation
============

::

    pip install -e git+ssh://git@github.com/jasonkeene/python-ubersmith.git#egg=ubersmith

Example Use
===========

First you'll need to setup a request handler with your login credentials::

    import ubersmith
    ubersmith.init('http://ubersmith/api/2.0/', 'username', 'password')

Then you can make API calls::

    from ubersmith import uber, client
    uber.method_list()
    client.get(email='g.freeman@combineresearch.com')

These modules match the methods as documented in the `Ubersmith API 2.0 docs`_.

.. _Ubersmith API 2.0 docs: https://github.com/jasonkeene/python-ubersmith/raw/master/docs/ubersmith_api_docs.pdf

Running Tests
=============

::

    # cd to repository
    pip install -r test-requirements.txt
    ./runtests.py

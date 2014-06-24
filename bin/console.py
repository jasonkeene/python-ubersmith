#!/usr/bin/env python

import os
from pprint import pprint
import sys

repo_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
docs_path = os.path.join(repo_path, 'docs/ubersmith_api_docs.pdf')
sys.path.append(repo_path)

import config
from ubersmith import *
handler = init(**config.API)


def check_methods():
    old = set(api.METHODS)
    new = set(uber.method_list().keys())

    if new - old:
        print
        print 'New Methods:'
        print
        print '['
        for method in new - old:
            print "    '{}',".format(method)
        print ']'

    if old - new:
        print
        print 'Outdated Methods:'
        print
        print '['
        for method in old - new:
            print "    '{}',".format(method)
        print ']'


def update_docs():
    with open(docs_path, 'wb') as f:
        f.write(uber.documentation().data)

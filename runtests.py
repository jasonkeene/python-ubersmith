#!/usr/bin/env python

import sys

import nose


if __name__ == '__main__':
    nose_args = sys.argv + [
        '--with-doctest',
        '--with-coverage',
        '--cover-package=ubersmith',
    ]
    nose.run(argv=nose_args)

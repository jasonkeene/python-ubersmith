#!/usr/bin/env python

import sys

import nose


if __name__ == '__main__':
    nose_args = sys.argv + ['--with-doctest']
    nose.run(argv=nose_args)

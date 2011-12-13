#!/usr/bin/env python
"""Script to merge several JSON fixture files together."""

import json
import os
import sys


_MASTER_JSON = {}

def main():
    files = sys.argv[1:]
    for f in files:
        if not os.path.exists(f):
            sys.stderr.write("File '{}' doesn't exist!\n".format(f))
            sys.exit(1)

    for f in files:
        file_json = {}
        with open(f, 'r') as f:
            file_json = json.load(f)

        for k, v in file_json.iteritems():
            if k not in _MASTER_JSON:
                _MASTER_JSON[k] = {}
            _MASTER_JSON[k].update(v)

    print json.dumps(_MASTER_JSON, sort_keys=True, indent=4)

if __name__ == '__main__':
    main()

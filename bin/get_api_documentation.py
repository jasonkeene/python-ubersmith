#!/usr/bin/env python
"""Script to check for outdated VALID_METHODS."""

import os
import sys

from tests.handlers import TestRequestHandler
from ubersmith.api import set_default_request_handler
from ubersmith import uber


REPO_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DOCS_FILE = os.path.join(REPO_PATH, 'docs/ubersmith_api_docs.pdf')
INPUT_MSG = u"Please provide an output file [{}]: ".format(DEFAULT_DOCS_FILE)


def main():
    set_default_request_handler(TestRequestHandler())
    try:
        out = sys.argv[1]
    except IndexError:
        out = raw_input(INPUT_MSG).strip() or DEFAULT_DOCS_FILE
    finally:
        # make sure output file path is absolute
        out = os.path.abspath(out)

    def get_overwrite():
        return raw_input("File exists, overwrite? (y/n) [y]: ").strip().lower()

    if os.path.exists(out):
        # ask for permission to overwrite
        while True:
            overwrite = get_overwrite()
            if not overwrite or overwrite.startswith('y'):
                break
            elif overwrite.startswith('n'):
                sys.stderr.write("File exists, will not overwrite!\n")
                sys.exit(1)
            else:
                print "Invalid response, please try again..."

    with open(out, 'wb') as f:
        f.write(uber.documentation().data)


if __name__ == '__main__':
    main()

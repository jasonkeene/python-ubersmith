"""
This module contains request handlers that log responses to disk and replay
them for tests.  I've found that simply mocking out dependencies and providing
test data in the test case seems to be saner but I figured I'd keep these
around for now.

"""

import json
import base64

from ubersmith import api

__all__ = [
    'LogHttpRequestHandler',
    'TestRequestHandler',
]


class LogHttpRequestHandler(api.HttpRequestHandler):
    """Logs responses to disk as JSON.

        Log Format:
            {
                "ubersmith.method": {
                    "request_data": {
                        "status": 200,
                        "content-type": "application/json",
                        "content": <decoded json>
                    },
                    "request_data": {
                        "status": 200,
                        "content-type": "application/pdf",
                        "content-disposition": "inline; filename=\"doc.pdf\";",
                        "last-modified": "Tue, 13 Mar 2012 03:05:36 GMT",
                        "content": <base64 encoded string>
                    }
                }
            }

    """
    _log_file_path = 'tests/fixtures/logged_call_responses.json'

    def __init__(self, base_url, username=None, password=None,
                 log_file_path=None):
        """Initialize logging HTTP request handler w/ optional authentication.

            base_url: URL to send API requests
            username: Username for API access
            password: Password for API access
            log_file_path: Path to log file

        """
        if log_file_path:
            self._log_file_path = log_file_path

        super(LogHttpRequestHandler, self).__init__(base_url, username,
                                                    password)

    def process_request(self, method, data=None, raw=False):
        """Process request over HTTP to ubersmith while logging response.

            method: Ubersmith API method string
            data: dict of method arguments
            raw: Set to True to return the raw response vs the default
                 behavior of returning JSON data

        """
        # make sure request method is valid
        self._validate_request_method(method)

        # make the request
        response, content = self._send_request(method, data)

        # log the request
        self._log_response(method, data, response, content)

        # render the response as python object
        return self._render_response(response, content, raw)

    def _log_response(self, method, data, response, content):
        body = self._encode_data(data)
        response_dict = {}

        # read in existing logged data to json_obj
        try:
            with open(self._log_file_path, 'r') as f:
                json_obj = json.load(f)
        except IOError:
            json_obj = {}

        # if there are no logged responses for current method create them
        if method not in json_obj:
            json_obj[method] = {}

        if response.get('content-type') == 'application/json':
            # response is encoded json, decode
            content = json.loads(content)
        else:
            # response is not json (probably binary file), base64 encode
            content = base64.b64encode(content)
            if response.get('content-disposition'):
                response_dict['content-disposition'] = response.get(
                                                        'content-disposition')

        # response info for all requests
        response_dict.update({
            'status': response.status,
            'content-type': response.get('content-type'),
            'content': content,
        })
        if response.get('last-modified'):
            response_dict['last-modified'] = response.get('last-modified')

        # update existing logged responses with current response
        json_obj[method].update({
            body: response_dict
        })

        # write log out to disk
        with open(self._log_file_path, 'w') as f:
            json.dump(json_obj, f, sort_keys=True, indent=4)


class TestRequestHandler(api._AbstractRequestHandler):
    """Loads responses from fixtures vs making HTTP requests."""
    _fixture_file_path = 'tests/fixtures/call_responses.json'

    def __init__(self, fixture_file_path=None):
        if fixture_file_path:
            self._fixture_file_path = fixture_file_path

    def process_request(self, method, data=None, raw=False):
        """Process request from fixtures.

            method: Ubersmith API method string
            data: dict of method arguments
            raw: Set to True to return the raw response vs the default
                 behavior of returning JSON data

        """
        # make sure requested method is valid
        self._validate_request_method(method)

        # load the response from fixtures
        response, content = self._load_response(method, data)

        # render the response as python object
        return self._render_response(response, content, raw)

    def _load_response(self, method, data):
        body = self._encode_data(data)

        # read in existing fixture data to json_obj
        with open(self._fixture_file_path, 'r') as f:
            json_obj = json.load(f)

        try:
            json_resp = json_obj[method][body]
        except KeyError:
            raise Exception('Unable to find fixture for provided method/data.')

        response = dict((k, v) for k, v in json_resp.items() if k != 'content')
        content = json_resp['content']

        if response.get('content-type') == 'application/json':
            # response is decoded json, encode
            content = json.dumps(content)
        else:
            # response is not json (probably binary file), base64 decode
            content = base64.b64decode(content)

        return response, content

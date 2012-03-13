"""Lower level API, configuration, and HTTP stuff."""

import base64
import json
import urllib
import urlparse

import httplib2

from ubersmith.exceptions import RequestError, ResponseError
from ubersmith.utils import append_qs

__all__ = [
    'VALID_METHODS',
    'HttpRequestHandler',
    'LogHttpRequestHandler',
    'TestRequestHandler',
    'get_default_request_handler',
    'set_default_request_handler',
]

_DEFAULT_REQUEST_HANDLER = None

"""A list of all methods returned from uber.method_list()"""
VALID_METHODS = [
    'client.ach_add',
    'client.ach_delete',
    'client.ach_update',
    'client.add',
    'client.cc_add',
    'client.cc_delete',
    'client.cc_update',
    'client.comment_list',
    'client.contact_add',
    'client.contact_delete',
    'client.contact_get',
    'client.contact_list',
    'client.contact_update',
    'client.count',
    'client.credit_add',
    'client.credit_comment_list',
    'client.credit_deactivate',
    'client.credit_list',
    'client.deactivate',
    'client.domain_add',
    'client.domain_list',
    'client.domain_lookup',
    'client.domain_register',
    'client.domain_transfer',
    'client.get',
    'client.invoice_charge',
    'client.invoice_count',
    'client.invoice_disregard',
    'client.invoice_generate',
    'client.invoice_get',
    'client.invoice_list',
    'client.invoice_payments',
    'client.invoice_post_gw_payment',
    'client.latest_client',
    'client.list',
    'client.lookup',
    'client.metadata_get',
    'client.metadata_single',
    'client.payment_method_list',
    'client.payment_refund',
    'client.reactivate',
    'client.renewal_list',
    'client.send_welcome',
    'client.service_add',
    'client.service_comment_list',
    'client.service_deactivate',
    'client.service_get',
    'client.service_list',
    'client.service_metadata_get',
    'client.service_metadata_single',
    'client.service_module_call',
    'client.service_prorate',
    'client.service_update',
    'client.set_login',
    'client.update',
    'device.add',
    'device.comment_list',
    'device.cpanel_add',
    'device.delete',
    'device.event_list',
    'device.facility_list',
    'device.get',
    'device.hostname_get',
    'device.ip_assign',
    'device.ip_assignment_add',
    'device.ip_assignment_delete',
    'device.ip_assignment_list',
    'device.ip_assignment_update',
    'device.ip_get_available',
    'device.ip_get_unassigned',
    'device.ip_group_add',
    'device.ip_group_delete',
    'device.ip_group_list',
    'device.ip_group_update',
    'device.ip_lookup',
    'device.ip_unassign',
    'device.list',
    'device.module_call',
    'device.module_call_aggregate',
    'device.module_graph',
    'device.monitor_add',
    'device.monitor_delete',
    'device.monitor_disable',
    'device.monitor_enable',
    'device.monitor_list',
    'device.monitor_update',
    'device.reboot',
    'device.reboot_graph',
    'device.tag',
    'device.type_list',
    'device.untag',
    'device.update',
    'device.vlan_get_available',
    'order.cancel',
    'order.client_respond',
    'order.coupon_get',
    'order.create',
    'order.get',
    'order.list',
    'order.process',
    'order.queue_list',
    'order.respond',
    'order.submit',
    'order.update',
    'sales.opportunity_add',
    'sales.opportunity_list',
    'sales.opportunity_stage_list',
    'sales.opportunity_status_list',
    'sales.opportunity_type_list',
    'sales.opportunity_update',
    'support.department_get',
    'support.department_list',
    'support.ticket_count',
    'support.ticket_get',
    'support.ticket_list',
    'support.ticket_merge',
    'support.ticket_post_client_response',
    'support.ticket_post_list',
    'support.ticket_post_staff_response',
    'support.ticket_submit',
    'support.ticket_submit_outgoing',
    'support.ticket_update',
    'uber.api_export',
    'uber.attachment_get',
    'uber.attachment_list',
    'uber.check_login',
    'uber.client_welcome_stats',
    'uber.comment_add',
    'uber.comment_delete',
    'uber.comment_get',
    'uber.comment_list',
    'uber.comment_update',
    'uber.documentation',
    'uber.event_list',
    'uber.forgot_pass',
    'uber.login_list',
    'uber.mail_get',
    'uber.mail_list',
    'uber.message_list',
    'uber.metadata_bulk_get',
    'uber.metadata_get',
    'uber.method_get',
    'uber.method_list',
    'uber.quick_stats',
    'uber.quick_stats_detail',
    'uber.service_plan_get',
    'uber.service_plan_list',
    'uber.user_exists',
    'uber.username_exists',
]


class _AbstractRequestHandler(object):
    def process_request(self, method, data=None, raw=False):
        """Process request.

            method: Ubersmith API method string
            data: dict of method arguments ready to urllib.urlencode
            raw: Set to True to return the raw response vs the default
                 behavior of returning JSON data

        """
        raise NotImplementedError

    def _render_response(self, response, content, raw):
        """Render response as python object.

            response: dict like object with headers
            content: raw response string from ubersmith
            raw: Set to True to return the raw response vs the default
                 behavior of returning JSON data

        """
        # just return the raw response
        if raw:
            return response, content

        # response isn't json
        if response.get('content-type') != 'application/json':
            ResponseError("Response wasn't application/json")

        # response is json
        response_dict = json.loads(content)

        # test for error in json response
        if not response_dict.get('status'):
            raise ResponseError(response=response_dict)

        return response_dict['data']

    def _validate_request_method(self, method):
        """Make sure requested method is valid."""
        if method not in VALID_METHODS:
            raise RequestError("Requested method is not valid.")

    def _encode_data(self, data):
        """URL encode data."""
        return urllib.urlencode(data if data is not None else {})


class HttpRequestHandler(_AbstractRequestHandler):
    """Handles HTTP requests and authentication."""

    def __init__(self, base_url, username=None, password=None):
        """Initialize HTTP request handler with optional authentication.

            base_url: URL to send API requests
            username: Username for API access
            password: Password for API access

        >>> handler = HttpRequestHandler('http://127.0.0.1:8088/')
        >>> handler.base_url
        'http://127.0.0.1:8088/'
        >>> config = {
        ...     'base_url': 'http://127.0.0.1/api/',
        ...     'username': 'admin',
        ...     'password': 'test_pass',
        ... }
        >>> handler = HttpRequestHandler(**config)
        >>> handler.base_url
        'http://127.0.0.1/api/'
        >>> handler.username
        'admin'
        >>> handler.password
        'test_pass'

        """
        self.base_url = base_url
        self.username = username
        self.password = password

        self._http = httplib2.Http(".cache")
        self._http.add_credentials(self.username, self.password,
                                   urlparse.urlparse(self.base_url)[1])

    def process_request(self, method, data=None, raw=False):
        """Process request over HTTP to ubersmith instance.

            method: Ubersmith API method string
            data: dict of method arguments ready to urllib.urlencode
            raw: Set to True to return the raw response vs the default
                 behavior of returning JSON data

        """
        # make sure requested method is valid
        self._validate_request_method(method)

        # make the request
        response, content = self._send_request(method, data)

        # render the response as python object
        return self._render_response(response, content, raw)

    def _send_request(self, method, data):
        url = self._construct_url(method)
        body = self._encode_data(data)
        # httplib2 requires that you manually send Content-Type on POSTs :/
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return self._http.request(url, "POST", body, headers)

    def _construct_url(self, method):
        return append_qs(self.base_url, {'method': method})


class LogHttpRequestHandler(HttpRequestHandler):
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

        >>> handler = LogHttpRequestHandler('http://127.0.0.1:8088/')
        >>> handler.base_url
        'http://127.0.0.1:8088/'
        >>> handler._log_file_path
        'tests/fixtures/logged_call_responses.json'
        >>> config = {
        ...     'base_url': 'http://127.0.0.1/api/',
        ...     'username': 'admin',
        ...     'password': 'test_pass',
        ...     'log_file_path': 'log_file.json',
        ... }
        >>> handler = LogHttpRequestHandler(**config)
        >>> handler.base_url
        'http://127.0.0.1/api/'
        >>> handler.username
        'admin'
        >>> handler.password
        'test_pass'
        >>> handler._log_file_path
        'log_file.json'

        """
        if log_file_path:
            self._log_file_path = log_file_path

        super(LogHttpRequestHandler, self).__init__(base_url, username,
                                                    password)

    def process_request(self, method, data=None, raw=False):
        """Process request over HTTP to ubersmith while logging response.

            method: Ubersmith API method string
            data: dict of method arguments ready to urllib.urlencode
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


class TestRequestHandler(_AbstractRequestHandler):
    """Loads responses from fixtures vs making HTTP requests."""
    _fixture_file_path = 'tests/fixtures/call_responses.json'

    def __init__(self, fixture_file_path=None):
        if fixture_file_path:
            self._fixture_file_path = fixture_file_path

    def process_request(self, method, data=None, raw=False):
        """Process request from fixtures.

            method: Ubersmith API method string
            data: dict of method arguments ready to urllib.urlencode
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

        response = {k: v for k, v in json_resp.iteritems() if k != 'content'}
        content = json_resp['content']

        if response.get('content-type') == 'application/json':
            # response is decoded json, encode
            content = json.dumps(content)
        else:
            # response is not json (probably binary file), base64 decode
            content = base64.b64decode(content)

        return response, content


def get_default_request_handler():
    """Return the default request handler."""
    if not _DEFAULT_REQUEST_HANDLER:
        raise Exception("Request handler required but no default was found.")
    return _DEFAULT_REQUEST_HANDLER


def set_default_request_handler(request_handler):
    """Set the default request handler."""
    if not isinstance(request_handler, _AbstractRequestHandler):
        raise TypeError(
            "Attempted to set an invalid request handler as default.")
    global _DEFAULT_REQUEST_HANDLER
    _DEFAULT_REQUEST_HANDLER = request_handler

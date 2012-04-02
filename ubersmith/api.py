"""Lower level API, configuration, and HTTP stuff."""

import json
import urlparse
import time
from functools import partial

import httplib2

from ubersmith.exceptions import (
    RequestError,
    ResponseError,
    UpdatingTokenResponse,
)
from ubersmith.utils import append_qs, urlencode_unicode

__all__ = [
    'VALID_METHODS',
    'HttpRequestHandler',
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


class _ProxyModule(object):
    def __init__(self, handler, module):
        self.handler = handler
        self.module = module

    def __getattr__(self, name):
        """Return the call with request_handler prefilled."""
        call_func = getattr(self.module, name)
        if callable(call_func):
            call_p = partial(call_func, request_handler=self.handler)
            # store partial on proxy so it doesn't have to be created again
            setattr(self, name, call_p)
            return call_p
        raise AttributeError("'{0}' object has no attribute '{1}'".format(
                                                   type(self).__name__, name))


class _AbstractRequestHandler(object):
    def process_request(self, method, data=None, raw=False):
        """Process request.

            method: Ubersmith API method string
            data: dict of method arguments
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
            if response.get('content-type') == 'text/html' and \
                'Updating Token' in content:
                raise UpdatingTokenResponse
            raise ResponseError("Response wasn't application/json")

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
        return urlencode_unicode(data if data is not None else {})

    def __getattr__(self, name):
        """If attribute accessed is a call module, return a proxy."""
        if name in set(m.split('.')[0] for m in VALID_METHODS):
            module_name = 'ubersmith.{0}'.format(name)
            module = __import__(module_name, fromlist=[''])
            proxy = _ProxyModule(self, module)
            # store proxy on handler so it doesn't have to be created again
            setattr(self, name, proxy)
            return proxy
        raise AttributeError("'{0}' object has no attribute '{1}'".format(
                                                   type(self).__name__, name))


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
            data: dict of method arguments
            raw: Set to True to return the raw response vs the default
                 behavior of returning JSON data

        """
        # make sure requested method is valid
        self._validate_request_method(method)

        # try request 3 times
        for i in range(3):
            # make the request
            response, content = self._send_request(method, data)
            try:
                # render the response as python object
                return self._render_response(response, content, raw)
            except UpdatingTokenResponse:
                # wait 4 secs before retrying request
                time.sleep(4)
        # if last attempt still threw an exception, reraise it
        raise

    def _send_request(self, method, data):
        url = append_qs(self.base_url, {'method': method})
        body = self._encode_data(data)
        # httplib2 requires that you manually send Content-Type on POSTs :/
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return self._http.request(url, "POST", body, headers)


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

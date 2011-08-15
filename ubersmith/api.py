"""Lower level API, configuration, and HTTP stuff."""

import json as json
from threading import local
import urllib
import urlparse

import httplib2

from ubersmith.exceptions import RequestError, ResponseError
from ubersmith.utils import append_qs

__all__ = [
    'VALID_METHODS',
    'RequestHandler',
    'get_default_request_handler',
    'set_default_request_handler',
]

_DEFAULT_REQUEST_HANDLER = local()
_DEFAULT_REQUEST_HANDLER.value = None

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
    'client.renewal_list',
    'client.send_welcome',
    'client.service_add',
    'client.service_comment_list',
    'client.service_deactivate',
    'client.service_get',
    'client.service_list',
    'client.service_metadata_get',
    'client.service_metadata_single',
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
    'device.untag',
    'device.update',
    'order.cancel',
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


class RequestHandler(object):
    """Handles all the HTTP requests and authentication."""

    def __init__(self, base_url, username=None, password=None):
        """Initialize request handler with authentication.

            base_url: URL to send API requests
            username: Username for API access
            password: Password for API access

        >>> handler = RequestHandler('http://127.0.0.1:8088/')
        >>> 'http' in urlparse.urlparse(handler.base_url).scheme
        True
        >>> config = {
        ...     'base_url': 'test1',
        ...     'username': 'test2',
        ...     'password': 'test3',
        ... }
        >>> handler = RequestHandler(**config)
        >>> # test that all config values were set as instance members
        >>> [False for k, v in config.items()
        ...     if getattr(handler, k, None) is not config[k]]
        []

        """
        self.base_url = base_url
        self.username = username
        self.password = password

        self._http = httplib2.Http(".cache")
        self._http.add_credentials(self.username, self.password,
                                   urlparse.urlparse(self.base_url)[1])

    def process(self, method, data=None, raw=False):
        """Send request to ubersmith instance.

            method: Ubersmith API method string
            data: dict of method arguments ready to urllib.urlencode
            raw: Set to True to return the raw response vs the default
                 behavior of returning JSON data

        """
        if method not in VALID_METHODS:
            raise RequestError("Requested method is not valid.")

        url = append_qs(self.base_url, {'method': method})
        data = data if data is not None else {}
        body = urllib.urlencode(data)
        # httplib2 requires that you manually send Content-Type on POSTs :/
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response, content = self._http.request(url, "POST", body, headers)

        # just return the raw response
        if raw:
            return response, content

        # response isn't json
        if response.get('content-type') != 'application/json':
            ResponseError("Response wasn't application/json")

        # response is json
        response_dict = json.loads(content)

        # test for error in json response
        if not response_dict['status']:
            raise ResponseError(response=response_dict)

        return response_dict['data']


def get_default_request_handler():
    """Return the local default request handler."""
    if not _DEFAULT_REQUEST_HANDLER.value:
        raise Exception("Request handler required but no default was found.")
    return _DEFAULT_REQUEST_HANDLER.value


def set_default_request_handler(request_handler):
    """Set the local default request handler."""
    if not isinstance(request_handler, RequestHandler):
        raise TypeError(
            "Attempted to set an invalid request handler as default.")
    _DEFAULT_REQUEST_HANDLER.value = request_handler

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
    u'client.ach_add',
    u'client.ach_delete',
    u'client.ach_update',
    u'client.add',
    u'client.cc_add',
    u'client.cc_delete',
    u'client.cc_update',
    u'client.comment_list',
    u'client.contact_add',
    u'client.contact_delete',
    u'client.contact_get',
    u'client.contact_list',
    u'client.contact_update',
    u'client.count',
    u'client.credit_add',
    u'client.credit_comment_list',
    u'client.credit_deactivate',
    u'client.credit_list',
    u'client.deactivate',
    u'client.domain_add',
    u'client.domain_list',
    u'client.domain_lookup',
    u'client.domain_register',
    u'client.domain_transfer',
    u'client.get',
    u'client.invoice_charge',
    u'client.invoice_count',
    u'client.invoice_disregard',
    u'client.invoice_generate',
    u'client.invoice_get',
    u'client.invoice_list',
    u'client.invoice_payments',
    u'client.invoice_post_gw_payment',
    u'client.latest_client',
    u'client.list',
    u'client.lookup',
    u'client.metadata_get',
    u'client.metadata_single',
    u'client.payment_method_list',
    u'client.renewal_list',
    u'client.send_welcome',
    u'client.service_add',
    u'client.service_comment_list',
    u'client.service_deactivate',
    u'client.service_get',
    u'client.service_list',
    u'client.service_metadata_get',
    u'client.service_metadata_single',
    u'client.service_prorate',
    u'client.service_update',
    u'client.set_login',
    u'client.update',
    u'device.add',
    u'device.comment_list',
    u'device.cpanel_add',
    u'device.delete',
    u'device.event_list',
    u'device.facility_list',
    u'device.get',
    u'device.hostname_get',
    u'device.ip_assign',
    u'device.ip_assignment_add',
    u'device.ip_assignment_delete',
    u'device.ip_assignment_list',
    u'device.ip_assignment_update',
    u'device.ip_get_available',
    u'device.ip_get_unassigned',
    u'device.ip_group_add',
    u'device.ip_group_delete',
    u'device.ip_group_list',
    u'device.ip_group_update',
    u'device.ip_lookup',
    u'device.ip_unassign',
    u'device.list',
    u'device.module_call',
    u'device.module_call_aggregate',
    u'device.module_graph',
    u'device.monitor_add',
    u'device.monitor_delete',
    u'device.monitor_disable',
    u'device.monitor_enable',
    u'device.monitor_list',
    u'device.monitor_update',
    u'device.reboot',
    u'device.reboot_graph',
    u'device.tag',
    u'device.untag',
    u'device.update',
    u'order.cancel',
    u'order.coupon_get',
    u'order.create',
    u'order.get',
    u'order.list',
    u'order.process',
    u'order.queue_list',
    u'order.respond',
    u'order.submit',
    u'order.update',
    u'sales.opportunity_add',
    u'sales.opportunity_list',
    u'sales.opportunity_stage_list',
    u'sales.opportunity_status_list',
    u'sales.opportunity_type_list',
    u'sales.opportunity_update',
    u'support.department_get',
    u'support.department_list',
    u'support.ticket_count',
    u'support.ticket_get',
    u'support.ticket_list',
    u'support.ticket_post_client_response',
    u'support.ticket_post_list',
    u'support.ticket_post_staff_response',
    u'support.ticket_submit',
    u'support.ticket_submit_outgoing',
    u'support.ticket_update',
    u'uber.api_export',
    u'uber.attachment_get',
    u'uber.attachment_list',
    u'uber.check_login',
    u'uber.client_welcome_stats',
    u'uber.comment_add',
    u'uber.comment_delete',
    u'uber.comment_get',
    u'uber.comment_list',
    u'uber.comment_update',
    u'uber.documentation',
    u'uber.event_list',
    u'uber.forgot_pass',
    u'uber.login_list',
    u'uber.mail_get',
    u'uber.mail_list',
    u'uber.message_list',
    u'uber.metadata_bulk_get',
    u'uber.metadata_get',
    u'uber.method_get',
    u'uber.method_list',
    u'uber.quick_stats',
    u'uber.quick_stats_detail',
    u'uber.service_plan_get',
    u'uber.service_plan_list',
    u'uber.user_exists',
    u'uber.username_exists',
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

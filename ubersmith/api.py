"""Lower level API, configuration, and HTTP stuff."""
import six
import time
from ubersmith.compat import total_ordering, file_type

import requests

from ubersmith.exceptions import (
    RequestError,
    ResponseError,
    UpdatingTokenResponse,
    MaintenanceResponse,
)
from ubersmith.utils import (
    append_qs,
    to_nested_php_args,
    get_filename,
)

__all__ = [
    'METHODS',
    'RequestHandler',
    'get_default_request_handler',
    'set_default_request_handler',
]

_DEFAULT_REQUEST_HANDLER = None

"""A dict of all methods returned by uber.method_list()"""
METHODS = {
    u'client.ach_add': u'Add a New Bank Account',
    u'client.ach_delete': u'Delete a Bank Account',
    u'client.ach_update': u'Update a Bank Account',
    u'client.add': u'Add a New Client',
    u'client.avatar_get': u"Retrieve a Client Avatar",
    u'client.avatar_set': u"Set a Client Avatar",
    u'client.cc_add': u'Add a New Credit Card',
    u'client.cc_delete': u'Delete a Credit Card',
    u'client.cc_info': u"List a Client's Credit Card Details",
    u'client.cc_update': u'Update a Credit Card',
    u'client.comment_list': u"List a Client's Comments",
    u'client.contact_add': u'Add a New Contact',
    u'client.contact_delete': u'Delete a Contact',
    u'client.contact_get': u'Get Contact Details',
    u'client.contact_list': u"List a Client's Contacts",
    u'client.contact_metadata_get': u"Get a Contact's Metadata",
    u'client.contact_metadata_single': u"Get a Contact's Metadata Value",
    u'client.contact_update': u'Update a Contact',
    u'client.count': u'Count Active Clients',
    u'client.credit_add': u'Add an Account Credit',
    u'client.credit_apply': u"Apply a Credit to an Invoice",
    u'client.credit_comment_list': u"List a Credit's Comments",
    u'client.credit_deactivate': u'Deactivate an Account Credit',
    u'client.credit_list': u"List a Client's Credits",
    u'client.deactivate': u'Deactivate a Client',
    u'client.domain_add': u'Add a Domain',
    u'client.domain_list': u"List a Client's Domains",
    u'client.domain_lookup': u'Look Up a Domain',
    u'client.domain_register': u'Register a Domain',
    u'client.domain_transfer': u'Transfer a Domain',
    u'client.get': u'Get Client Details',
    u'client.invoice_charge': u'Charge an Invoice',
    u'client.invoice_count': u'Count Invoices',
    u'client.invoice_disregard': u'Disregard an Invoice',
    u'client.invoice_generate': u'Generate an Invoice',
    u'client.invoice_get': u'Get an Invoice',
    u'client.invoice_list': u"List a Client's Invoices",
    u'client.invoice_payments': u"List an Invoice's Payments",
    u'client.invoice_post_gw_payment': u'Record a Payment',
    u'client.latest_client': u'Get the Latest Client',
    u'client.list': u'List Clients',
    u'client.lookup': u'Look Up a Client',
    u'client.metadata_get': u"Get a Client's Metadata",
    u'client.metadata_single': u"Get a Client's Metadata Value",
    u'client.payment_method_list': u"List a Client's Payment Methods",
    u'client.payment_refund': u'Refund a payment.',
    u'client.reactivate': u'Reactivate a Client',
    u'client.renewal_list': u'List Services for Renewal',
    u'client.send_welcome': u'Send a Welcome Letter',
    u'client.service_add': u'Add a New Service',
    u'client.service_comment_list': u"List a Service's Comments",
    u'client.service_deactivate': u'Deactivate a Service',
    u'client.service_get': u'Get a Service',
    u'client.service_list': u"List a Client's Services",
    u'client.service_metadata_get': u"Get a Service's Metadata",
    u'client.service_metadata_single': u"Get a Service's Metadata Value",
    u'client.service_module_call': u'Call a Service Module Function',
    u'client.service_prorate': u'Prorate a Service',
    u'client.service_update': u'Update a Service',
    u'client.set_login': u"Set a Client's Login",
    u'client.tax_exemption_add': u"Add a new Tax Exemption",
    u'client.tax_exemption_get': u"Get a Client's Tax Exemption",
    u'client.tax_exemption_list': u"List a Client's Tax Exemptions",
    u'client.tax_exemption_update': u"Update a Client's Tax Exemption",
    u'client.update': u'Update a Client',
    u'device.add': u'Add a New Device',
    u'device.comment_list': u"List a Device's Comments",
    u'device.connection_list': u"List a Device's Connections",
    u'device.cpanel_add': u'Add a cPanel Account',
    u'device.delete': u'Delete a Device',
    u'device.event_list': u'List Device Events',
    u'device.facility_list': u'List Device Facilities',
    u'device.get': u'Get a Device',
    u'device.hostname_get': u'Get a Device Hostname',
    u'device.ip_assign': u'Assign an IP to a Device',
    u'device.ip_assignment_add': u'Create a New IP Assignment',
    u'device.ip_assignment_delete': u'Delete a Device IP Assignment',
    u'device.ip_assignment_list': u'List Device IP Assignments',
    u'device.ip_assignment_update': u'Update a Device IP Assignment',
    u'device.ip_block_list': u"List IP Blocks",
    u'device.ip_get_available': u'List Available IP Addresses',
    u'device.ip_get_unassigned': u'Get Unassigned IP Addresses',
    u'device.ip_group_add': u'Add a Device IP Group',
    u'device.ip_group_delete': u'Delete a Device IP Group',
    u'device.ip_group_list': u'List a Device IP Group',
    u'device.ip_group_update': u'Update a Device IP Group',
    u'device.ip_lookup': u'Look Up a Device IP',
    u'device.ip_pool_list': u"List IP Pools",
    u'device.ip_unassign': u'Unassign a Device IP',
    u'device.list': u'List Devices',
    u'device.module_call': u'Call a Device Module Function',
    u'device.module_call_aggregate': u'Call an Aggregate Device Module Function',
    u'device.module_graph': u'Generate Device Module Graph',
    u'device.monitor_add': u'Add a New Device Monitor',
    u'device.monitor_delete': u'Delete a Device Monitor',
    u'device.monitor_disable': u'Disable a Device Monitor',
    u'device.monitor_enable': u'Enable a Device Monitor',
    u'device.monitor_list': u'List Device Monitors',
    u'device.monitor_update': u'Update a Device Monitor',
    u'device.reboot': u"Set a Device's Power State",
    u'device.reboot_graph': u'Get a Reboot Graph',
    u'device.tag': u'Tag a Device',
    u'device.type_list': u'List Device Types',
    u'device.untag': u'Untag a Device',
    u'device.update': u'Update a Device',
    u'device.vlan_get_available': u'List Available VLANs',
    u'order.cancel': u'Cancel an Order',
    u'order.client_respond': u'Post a Client/Lead Order Response',
    u'order.coupon_get': u'Get Order Coupon Details',
    u'order.create': u'Create a New Order',
    u'order.get': u'Get Order Details',
    u'order.list': u'List Orders',
    u'order.process': u'Process an Order',
    u'order.queue_list': u'List Order Queues',
    u'order.respond': u'Post an Order Response',
    u'order.submit': u'Submit An Order',
    u'order.update': u'Update an Order',
    u'sales.opportunity_add': u'Add an Opportunity',
    u'sales.opportunity_list': u'List Opportunities',
    u'sales.opportunity_stage_list': u'List Opportunity Stages',
    u'sales.opportunity_status_list': u'List Opportunity Statuses',
    u'sales.opportunity_type_list': u'List Opportunity Types',
    u'sales.opportunity_update': u'Update an Opportunity',
    u'support.department_get': u'Get Ticket Departments',
    u'support.department_list': u'List Ticket Departments',
    u'support.ticket_count': u'Count Support Tickets',
    u'support.ticket_get': u'Get Support Ticket Details',
    u'support.ticket_list': u'Get a List of Tickets',
    u'support.ticket_merge': u'Merge Tickets',
    u'support.ticket_post_client_response': u'Post a Client Response to a Ticket',
    u'support.ticket_post_list': u'Get all Posts for a Ticket',
    u'support.ticket_post_staff_response': u'Post a Staff Response to a Ticket',
    u'support.ticket_submit': u'Submit a New Ticket',
    u'support.ticket_submit_outgoing': u'Create a New Outgoing Ticket',
    u'support.ticket_type_list': u"Get a List of Ticket Types",
    u'support.ticket_update': u'Update a Ticket',
    u'uber.admin_avatar_get': u"Retrieve an Admin Avatar",
    u'uber.admin_avatar_set': u"Set an Admin Avatar",
    u'uber.admin_get': u"User Information",
    u'uber.admin_list': u"List User Logins",
    u'uber.api_export': u'Export Data',
    u'uber.attachment_get': u'Get an attachment',
    u'uber.attachment_list': u'List Attachments',
    u'uber.check_login': u'Verify a login and password',
    u'uber.client_permission_list': u"List available permissions",
    u'uber.client_welcome_stats': u'Display Client Statistics',
    u'uber.comment_add': u'Add Comment',
    u'uber.comment_delete': u'Delete Comment',
    u'uber.comment_get': u'Get Comments',
    u'uber.comment_list': u'List Comments',
    u'uber.comment_update': u'Update Comment',
    u'uber.documentation': u'Download API Documentation',
    u'uber.event_list': u'Access the Event Log',
    u'uber.file_add': u"Add a file",
    u'uber.file_delete': u"Delete a file",
    u'uber.file_get': u"Get a File",
    u'uber.file_list': u"Get a List of Files",
    u'uber.file_update': u"Update a file",
    u'uber.forgot_pass': u'Send a Password Reminder',
    u'uber.login_list': u'List User Logins',
    u'uber.mail_get': u'Get an Email From the Log',
    u'uber.mail_list': u'Access the Mail Log',
    u'uber.message_list': u'List Message Board Messages',
    u'uber.metadata_bulk_get': u'Bulk Get Metadata Values',
    u'uber.metadata_get': u'Get Metadata Values',
    u'uber.method_get': u'Get API Method Details',
    u'uber.method_list': u'List Available API Methods',
    u'uber.quick_stats': u'Get Quick System Stats',
    u'uber.quick_stats_detail': u'Get Detailed System Stats',
    u'uber.service_plan_get': u'Get Service Plan Details',
    u'uber.service_plan_list': u'List Service Plans',
    u'uber.tax_exemption_type_get': u"Get a Tax Exemption Type",
    u'uber.tax_exemption_type_list': u"List Tax Exemption Types",
    u'uber.user_exists': u'Check whether a Client Exists',
    u'uber.username_exists': u'Check Whether a Username Exists',
}


class _ProxyModule(object):
    def __init__(self, handler, module):
        self.handler = handler
        self.module = module

    def __getattr__(self, name):
        """Return the call with request_handler prefilled."""
        call_func = getattr(self.module, name)
        if callable(call_func):
            call_p = call_func.handler(self.handler)
            # store partial on proxy so it doesn't have to be created again
            setattr(self, name, call_p)
            return call_p
        raise AttributeError("'{0}' object has no attribute '{1}'".format(
            type(self).__name__, name))


class RequestHandler(object):
    """Handles HTTP requests and authentication."""

    def __init__(self, base_url, username=None, password=None, verify=True):
        """Initialize HTTP request handler with optional authentication.

            base_url: URL to send API requests
            username: Username for API access
            password: Password for API access
            verify: Verify HTTPS certificate

        """
        self.base_url = base_url
        self.username = username
        self.password = password
        self.verify = verify

    def process_request(self, method, data=None):
        """Process request over HTTP to ubersmith instance.

            method: Ubersmith API method string
            data: dict of method arguments

        """
        # make sure requested method is valid
        self._validate_request_method(method)

        # attempt the request multiple times
        attempts = 3
        for i in range(attempts):
            response = self._send_request(method, data)

            # handle case where ubersmith is 'updating token'
            # see: https://github.com/jasonkeene/python-ubersmith/issues/1
            if self._is_token_response(response):
                if i < attempts - 1:
                    # wait 2 secs before retrying request
                    time.sleep(2)
                    continue
                else:
                    raise UpdatingTokenResponse
            break

        resp = BaseResponse(response)

        # test for error in json response
        if response.headers.get('content-type') == 'application/json':
            if not resp.json.get('status'):
                if all([
                    resp.json.get('error_code') == 1,
                    resp.json.get('error_message') == u"We are currently "
                        "undergoing maintenance, please check back shortly.",
                ]):
                    raise MaintenanceResponse(response=resp.json)
                else:
                    raise ResponseError(response=resp.json)
        return resp

    @staticmethod
    def _is_token_response(response):
        return ('text/html' in response.headers.get('content-type', '') and
                'Updating Token' in response.content)

    def _send_request(self, method, data):
        url = append_qs(self.base_url, {'method': method})
        data, files, headers = self._encode_data(data)
        return requests.post(url, data=data, files=files, headers=headers,
                             auth=(self.username, self.password),
                             verify=self.verify)

    @staticmethod
    def _validate_request_method(method):
        """Make sure requested method is valid."""
        if method not in METHODS:
            raise RequestError("Requested method is not valid.")

    @staticmethod
    def _encode_data(data):
        """URL encode data."""
        data = data if data is not None else {}
        data = to_nested_php_args(data)
        files = dict([
            (key, value) for key, value in
            data.items() if isinstance(value, file_type)])
        for fname in files:
            del data[fname]
        return data, files or None, None

    def __getattr__(self, name):
        """If attribute accessed is a call module, return a proxy."""
        if name in set(m.split('.')[0] for m in METHODS):
            module_name = 'ubersmith.{0}'.format(name)
            module = __import__(module_name, fromlist=[''])
            proxy = _ProxyModule(self, module)
            # store proxy on handler so it doesn't have to be created again
            setattr(self, name, proxy)
            return proxy
        raise AttributeError("'{0}' object has no attribute '{1}'".format(
            type(self).__name__, name))


class BaseResponse(object):
    """Wraps response object and emulates different types."""
    def __init__(self, response):
        self.response = response  # requests' response object

    @classmethod
    def from_cleaned(cls, response, cleaned):
        resp = cls(response.response)
        resp.cleaned = cleaned
        return resp

    @property
    def json(self):
        return self.response.json()

    @property
    def data(self):
        if hasattr(self, "cleaned"):
            return self.cleaned
        else:
            return self.json['data']

    @property
    def type(self):
        return self.response.headers.get('content-type')

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return repr(self.data)

    def __nonzero__(self):
        return bool(self.data)

    def __json__(self):
        """This method returns the JSON-serializable representation of the
        Response. To utilize this, create a JSONEncoder which calls the
        __json__ methods of supporting objects. e.g.::

            import json
            class MyJSONEncoder(json.JSONEncoder):
                def default(self, o):
                    if hasattr(obj, '__json__') and callable(obj.__json__):
                        return obj.__json__()
                    else:
                        return super(MyJSONEncoder, self).default(o)

            json.dumps(my_response, cls=MyJSONEncoder)
        """
        return self.data


@total_ordering
class DictResponse(BaseResponse):
    __marker = object()

    def keys(self):
        return self.data.keys()

    def iterkeys(self):
        return six.iterkeys(self.data)

    def values(self):
        return self.data.values()

    def itervalues(self):
        return six.itervalues(self.data)

    def items(self):
        return self.data.items()

    def iteritems(self):
        return six.iteritems(self.data)

    def get(self, key, default=None):
        return self.data.get(key, default)

    def update(self, d):
        self.data.update(d)

    def setdefault(self, key, value):
        self.data.setdefault(key, value)

    def pop(self, key, default=__marker):
        if default is self.__marker:
            return self.data.pop(key)
        else:
            return self.data.pop(key, default)

    def popitem(self):
        return self.data.popitem()

    def clear(self):
        self.data.clear()

    def __setitem__(self, key, value):
        self.data[key] = value

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, key):
        return self.data[key]

    def __len__(self):
        return len(self.data)

    def __eq__(self, other):
        return self.data == other

    def __lt__(self, other):
        return self.data < other

    def __contains__(self, item):
        return item in self.data


@total_ordering
class IntResponse(BaseResponse):
    @property
    def numerator(self):
        return self.data

    @property
    def denominator(self):
        return 1

    @property
    def real(self):
        return self.data

    @property
    def imag(self):
        return 0

    def bit_length(self):
        if hasattr(self.data, 'bit_length'):
            return self.data.bit_length()
        else:
            return len(bin(abs(self.data))) - 2

    def conjugate(self):
        return self.data

    def __int__(self):
        return self.data
    __index__ = __long__ = __trunc__ = __int__

    def __float__(self):
        return float(self.data)

    def __oct__(self):
        return oct(self.data)

    def __hex__(self):
        return hex(self.data)

    def __eq__(self, other):
        return self.data == other

    def __lt__(self, other):
        return self.data < other

    def __add__(self, other):
        return int(self) + other
    __radd__ = __add__

    def __sub__(self, other):
        return int(self) - other

    def __rsub__(self, other):
        return other - int(self)

    def __mul__(self, other):
        return int(self) * other
    __rmul__ = __mul__

    def __div__(self, other):
        return int(self) / other

    def __rdiv__(self, other):
        return other / int(self)

    def __floordiv__(self, other):
        return int(self) // other

    def __rfloordiv__(self, other):
        return other // int(self)

    def __truediv__(self, other):
        return float(self) / other

    def __rtruediv__(self, other):
        return other / float(self)

    def __mod__(self, other):
        return int(self) % other

    def __rmod__(self, other):
        return other % int(self)

    def __pow__(self, other):
        return int(self) ** other

    def __rpow__(self, other):
        return other ** int(self)

    def __abs__(self):
        return abs(self.data)

    def __neg__(self):
        return -self.data

    def __pos__(self):
        return self.data

    def __divmod__(self, other):
        return self // other, self % other

    def __rdivmod__(self, other):
        return other // self, other % self

    def __and__(self, other):
        return self.data & other
    __rand__ = __and__

    def __or__(self, other):
        return self.data | other
    __ror__ = __or__

    def __xor__(self, other):
        return self.data ^ other
    __rxor__ = __xor__

    def __lshift__(self, other):
        return self.data << other

    def __rlshift__(self, other):
        return other << self.data

    def __rshift__(self, other):
        return self.data >> other

    def __rrshift__(self, other):
        return other >> self.data

    def __invert__(self):
        return ~self.data

    def __nonzero__(self):
        return bool(self.data)


class FileResponse(BaseResponse):
    @property
    def json(self):
        raise NotImplementedError

    @property
    def data(self):
        return self.response.content

    @property
    def filename(self):
        disposition = self.response.headers.get('content-disposition')
        return get_filename(disposition)


def get_default_request_handler():
    """Return the default request handler."""
    if not _DEFAULT_REQUEST_HANDLER:
        raise Exception("Request handler required but no default was found.")
    return _DEFAULT_REQUEST_HANDLER


def set_default_request_handler(request_handler):
    """Set the default request handler."""
    if not isinstance(request_handler, RequestHandler):
        raise TypeError(
            "Attempted to set an invalid request handler as default.")
    global _DEFAULT_REQUEST_HANDLER
    _DEFAULT_REQUEST_HANDLER = request_handler

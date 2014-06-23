import json

from mock import Mock, patch
import pytest
from six import text_type

import ubersmith.uber
import ubersmith.api
from ubersmith.api import (
    RequestHandler,
    METHODS,
    get_default_request_handler,
    set_default_request_handler,
)
from ubersmith.exceptions import (
    RequestError,
    ResponseError,
    UpdatingTokenResponse,
    MaintenanceResponse,
)


class DescribeRequestHandler:
    test_data = 'this is some data'

    @pytest.fixture
    def response(self):
        response = Mock()
        response.headers = {
            'status': '200',
            'content-type': 'application/json',
        }
        resp_json = {
            'status': True,
            'error_code': None,
            'error_message': '',
            'data': self.test_data,
        }
        response.json.return_value = resp_json
        response.content = json.dumps(resp_json)
        response.text = text_type(response.content)
        return response

    @pytest.fixture
    @pytest.fixture
    def maintenance_response(self):
        response = Mock()
        response.headers = {
            'status': '200',
            'content-type': 'application/json',
        }
        resp_json = {
            'status': False,
            'data': '',
            'error_message': 'We are currently undergoing maintenance, please check back shortly.',
            'error_code': 1,
        }
        response.json.return_value = resp_json
        response.content = json.dumps(resp_json)
        response.text = text_type(response.content)
        return response

    @pytest.fixture
    def token_response(self):
        response = Mock()
        response.headers = {
            'status': '200',
            'content-type': 'text/html',
        }
        response.content = '\n<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n<html>\n<head>\n\t<title>Updating Token...</title>\n\t<link rel="shortcut icon" type="image/x-icon" href="/ubericon.ico">\n\t<meta http-equiv="Refresh" content="4">\n\t<link href="/locale/en_US/css/stylesheet.css" rel="stylesheet" type="text/css">\n\t<style type="text/css">\n\t<!--\n.config-box-4 {height:auto !important;height:400px;min-height:400px;}\n\t-->\n\t</style>\n\t<script type="text/javascript" src="/js/jquery.js"></script>\n\t<script language="javascript">\n\t\tif (top.location != location) {\n\t\t\ttop.location.href = document.location.href;\n\t\t}\n\t\t$(function() {\t\n\t\t\t$("body").delegate("div.notification a.close","click",function(e) {\n\t\t\t\te.preventDefault();\n\t\t\t\t$(this).closest(\'div.notification-wrapper\').hide();\n\t\t\t});\n\t\t});\n\t\t\n\t</script>\n</head>\n<body>\n\t<div style="background: #ccccff url(\'/images/background_pagebar.png\') repeat-x top left;padding:0 10px;border-bottom:1px solid #999999;">\n\t\t<div style="padding:6px 0;">\n\t\t\t<img src="/images/logo_ubersmith.png" width="126" height="24" border="0" />\n\t\t</div>\n\t</div>\n\t\n\t<div class="config-box-1" style="margin:15px;"><div class="config-box-2"><div class="config-box-3"><div class="config-box-4">\n<table border="0" cellpadding="10" cellspacing="0">\n\t\t\t\t\t<tr valign="top">\n\t\t\t\t\t\t<td rowspan="2"><img src="/images/uber-anim.gif" /></td>\n\t\t\t\t\t\t<td class="CellText"><span style="font-size:150%;font-weight:bold;">Ubersmith Token Update</span></td>\n\t\t\t\t\t</tr>\n\t\t\t\t\t<tr>\n\t\t\t\t\t\t<td class="CellText">Please wait while your token is updated.</td>\n\t\t\t\t\t</tr>\n\t\t\t\t</table>\n\t</div></div></div></div>\n</body>\n</html>\n'
        response.text = text_type(response.content)
        return response

    def it_handles_normal_responses(self, response):
        h = RequestHandler('')
        h._send_request = Mock(return_value=response)
        assert self.test_data == h.process_request('uber.method_list').data

    def it_handles_updating_token(self, response, token_response):
        returns = [
            token_response,
            token_response,
            response,
        ]
        h = RequestHandler('')
        h._send_request = Mock(side_effect=lambda *args: returns.pop(0))
        with patch('ubersmith.api.time') as time:
            time.sleep = lambda x: None
            assert self.test_data == h.process_request('uber.method_list').data

    def it_raises_updating_token_after_3_tries(self, response, token_response):
        returns = [
            token_response,
            token_response,
            token_response,
            response,
        ]
        h = RequestHandler('')
        h._send_request = Mock(side_effect=lambda *args: returns.pop(0))
        with patch('ubersmith.api.time') as time:
            time.sleep = lambda x: None
            with pytest.raises(UpdatingTokenResponse):
                h.process_request('uber.method_list')

    def it_raises_maintenance_response(self, maintenance_response):
        h = RequestHandler('')
        h._send_request = Mock(return_value=maintenance_response)
        with pytest.raises(MaintenanceResponse):
            h.process_request('uber.method_list')

    def it_is_able_to_proxy_calls_to_modules(self):
        h = RequestHandler('')
        for call_base, call_name in (m.split('.') for m in METHODS):
            assert hasattr(h, call_base)
            proxy = getattr(h, call_base)
            partial = getattr(proxy, call_name)
            assert callable(partial)
            assert partial.request_handler == h

    def it_does_not_proxy_calls_to_modules_that_do_not_exist(self):
        h = RequestHandler('')
        with pytest.raises(AttributeError):
            h.invalid_module

    def it_does_not_proxy_calls_to_methods_that_do_not_exist(self):
        h = RequestHandler('')
        with pytest.raises(AttributeError):
            h.uber.invalid_method

    def it_does_not_proxy_calls_to_methods_that_are_not_callable(self):
        h = RequestHandler('')
        ubersmith.uber.rando = 'X-rando'
        with pytest.raises(AttributeError):
            h.uber.rando

    def it_validates_ssl(self, response):
        h = RequestHandler('')
        with patch('ubersmith.api.requests') as requests:
            requests.post.return_value = response
            h.process_request('uber.method_list')
            assert requests.post.call_args[1]['verify'] is True

    def it_can_disable_ssl_validation(self, response):
        h = RequestHandler('', verify=False)
        with patch('ubersmith.api.requests') as requests:
            requests.post.return_value = response
            h.process_request('uber.method_list')
            assert requests.post.call_args[1]['verify'] is False

    def it_validates_bad_methods(self):
        h = RequestHandler('')
        with pytest.raises(RequestError) as e:
            h.process_request('boop')
        assert str(e.value) == "Requested method is not valid."


def test_get_set_default_handler():
    h = RequestHandler('')
    set_default_request_handler(h)
    assert get_default_request_handler() == h
    ubersmith.api._DEFAULT_REQUEST_HANDLER = None


def test_raise_exception_if_no_default_handler_is_set():
    with pytest.raises(Exception) as e:
        get_default_request_handler()
    assert str(e.value) == "Request handler required but no default was found."


def test_raise_exception_if_trying_to_set_non_handler():
    with pytest.raises(TypeError) as e:
        set_default_request_handler("not a handler")
    assert str(e.value) == "Attempted to set an invalid request handler as default."

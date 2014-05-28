from mock import Mock

import ubersmith


def it_sets_default_request_handler(monkeypatch):
    set_handler_mock = Mock()
    monkeypatch.setattr(ubersmith, 'set_default_request_handler',
                        set_handler_mock)
    ubersmith.init('X-base_url', 'X-username', 'X-password', 'X-verify')
    handler = set_handler_mock.call_args[0][0]
    assert handler.base_url == 'X-base_url'
    assert handler.username == 'X-username'
    assert handler.password == 'X-password'
    assert handler.verify == 'X-verify'

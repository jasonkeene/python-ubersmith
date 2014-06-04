from mock import Mock
import pytest

import ubersmith.api


@pytest.fixture
def requests(monkeypatch):
    requests = Mock()
    monkeypatch.setattr(ubersmith.api, 'requests', requests)
    return requests


@pytest.fixture
def response(requests):
    response = Mock()
    response.headers = {
        'content-type': 'application/json',
    }
    response.text = u""
    requests.post.return_value = response
    return response

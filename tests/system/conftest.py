from mock import Mock
import pytest

import ubersmith.api


@pytest.fixture
def session(monkeypatch):
    session = Mock()
    monkeypatch.setattr(ubersmith.api.RequestHandler, 'session', session)
    return session


@pytest.fixture
def response(session):
    response = Mock()
    response.headers = {
        'content-type': 'application/json',
    }
    response.text = u""
    session.post.return_value = response
    return response

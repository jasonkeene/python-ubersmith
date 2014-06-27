from mock import Mock
import pytest

from ubersmith.api import IntResponse


class DescribeIntResponse:
    @pytest.fixture
    def response(self):
        resp = Mock()
        resp.json.return_value = {'data': 12}
        return IntResponse(resp)

    def it_adds(self, response):
        assert response + 2 == 14
        assert 2 + response == 14

    def it_subtracts(self, response):
        assert response - 2 == 10
        assert 2 - response == 10

    def it_multiplies(self, response):
        assert response * 2 == 24
        assert 2 * response == 24

    def it_divides(self, response):
        assert response / 2 == 6
        assert 2 / response == 0

    def it_mods(self, response):
        assert response % 5 == 2
        assert 15 % response == 3

    def it_pows(self, response):
        assert response ** 2 == 144
        assert 2 ** response == 4096

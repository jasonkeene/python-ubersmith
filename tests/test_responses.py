from mock import Mock
import pytest

from ubersmith.api import DictResponse, IntResponse


class DescribeDictResponse:
    @pytest.fixture
    def response(self):
        resp = Mock()
        resp.json.return_value = {'data': {
            'key1': 'value1',
            'key2': 'value2',
            'key3': 'value3',
        }}
        return DictResponse(resp)

    def it_returns_keys(self, response):
        assert sorted(response.keys()) == [
            'key1',
            'key2',
            'key3',
        ]

    def it_returns_values(self, response):
        assert sorted(response.values()) == [
            'value1',
            'value2',
            'value3',
        ]

    def it_returns_items(self, response):
        assert sorted(response.items()) == [
            ('key1', 'value1'),
            ('key2', 'value2'),
            ('key3', 'value3'),
        ]

    def it_gets(self, response):
        assert response.get("key1") == "value1"
        assert response.get("bad-key", "default") == "default"

    def it_iterates(self, response):
        result = {}
        for key in response:
            result[key] = response[key]
        assert result == {
            'key1': 'value1',
            'key2': 'value2',
            'key3': 'value3',
        }

    class ContextFromCleaned:
        """Allows mutations"""

        @pytest.fixture
        def response(self):
            resp = Mock()
            return DictResponse.from_cleaned(resp, {'data': {
                'key1': 'value1',
                'key2': 'value2',
                'key3': 'value3',
            }})

        def it_mutates_like_a_dict(self, response):
            response.update({'key4': 'value4'})
            assert response['key4'] == 'value4'

            response['key5'] = 'value5'
            assert response['key5'] == 'value5'

            response.setdefault('key6', 'value6')
            assert response['key6'] == 'value6'

            value = response.pop('key6')
            assert value == 'value6'
            assert 'key6' not in response

            value = response.pop('key6', 'default')
            assert value == 'default'

            length = len(response)
            response.popitem()
            assert len(response) == length - 1

            response.clear()
            assert not response


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
        assert response - 3 == 9
        assert 15 - response == 3

    def it_multiplies(self, response):
        assert response * 2 == 24
        assert 2 * response == 24

    def it_divides(self, response):
        assert response / 5 == 12 / 5
        assert 15 / response == 15 / 12

    def it_floor_divides(self, response):
        assert response // 5 == 2
        assert 15 // response == 1

    def it_mods(self, response):
        assert response % 5 == 2
        assert 15 % response == 3

    def it_pows(self, response):
        assert response ** 2 == 144
        assert 2 ** response == 4096

    def it_converts_to_int(self, response):
        result = int(response)
        assert type(result) is int
        assert result == 12

    def it_converts_to_float(self, response):
        result = float(response)
        assert type(result) is float
        assert result == 12.0

    def it_converts_to_octal(self, response):
        assert oct(response) in ['0o14', '014']

    def it_converts_to_hex(self, response):
        assert hex(response) == '0xc'

    def it_abs(self, response):
        resp = Mock()
        resp.json.return_value = {'data': -12}
        response2 = IntResponse(resp)
        assert abs(response) == 12
        assert abs(response2) == 12

    def it_negates(self, response):
        resp = Mock()
        resp.json.return_value = {'data': -12}
        response2 = IntResponse(resp)
        assert -response == -12
        assert -response2 == 12

    def it_positives(self, response):
        resp = Mock()
        resp.json.return_value = {'data': -12}
        response2 = IntResponse(resp)
        assert +response == 12
        assert +response2 == -12

    def it_divmods(self, response):
        assert divmod(response, 5) == (2, 2)
        assert divmod(50, response) == (4, 2)

    def it_ands(self, response):
        assert response & 4 == 4
        assert 8 & response == 8

    def it_ors(self, response):
        assert response | 40 == 44
        assert 18 | response == 30

    def it_xors(self, response):
        assert response ^ 4 == 8
        assert 8 ^ response == 4

    def it_lshifts(self, response):
        assert response << 3 == 96
        assert 1 << response == 4096

    def it_rshifts(self, response):
        assert response >> 2 == 3
        assert 8192 >> response == 2

    def it_has_numerator(self, response):
        assert response.numerator == 12

    def it_has_denomerator(self, response):
        assert response.denominator == 1

    def it_has_real(self, response):
        assert response.real == 12

    def it_has_imag(self, response):
        assert response.imag == 0

    def it_has_bit_length(self, response):
        assert response.bit_length() == 4

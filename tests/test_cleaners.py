import datetime
from decimal import Decimal

import pytest

from ubersmith.clean import clean


class DescribeClean:
    def it_cleans_ints(self):
        assert clean(int)('123') == 123

    def it_cleans_list(self):
        assert clean(list)([1, 2, 3, 4]) == [1, 2, 3, 4]

    def it_cleans_list_values(self):
        cleaner = clean(list, values=str)
        assert cleaner([1, 2, 3, 4]) == ['1', '2', '3', '4']

    def it_cleans_specific_values_in_list(self):
        cleaner = clean(list, values={
            1: str,
            3: int,
            5: Decimal,
        })
        result = cleaner(range(6))
        assert result == [0, '1', 2, 3, 4, Decimal(5)]
        assert type(result[1]) is str
        assert type(result[3]) is int
        assert type(result[5]) is Decimal

    def it_silences_index_errors(self):
        cleaner = clean(list, values={
            1: str,
            3: int,
            5: Decimal,
        })
        result = cleaner(range(2))
        assert result == [0, '1']
        assert type(result[1]) is str

    def it_raises_index_errors_if_asked(self):
        cleaner = clean(list, values={
            1: str,
            3: int,
            5: Decimal,
        }, raises=True)
        with pytest.raises(IndexError):
            cleaner(range(2))

    def it_cleans_recursive_lists(self):
        cleaner = clean(list, values={
            1: str,
            3: int,
            5: clean(list, values=int),
        })
        result = cleaner([0, 1, 2, 3, 4, ['10', '20', '30']])
        assert result == [0, '1', 2, 3, 4, [10, 20, 30]]

    def it_cleans_dicts(self):
        assert clean(dict)({'key': 'value'}) == {'key': 'value'}

    def it_cleans_dict_keys(self):
        assert clean(dict, keys=int)({
            '10': 'a',
            '20': 'b',
            '30': 'c',
        }) == {
            10: 'a',
            20: 'b',
            30: 'c',
        }

    def it_cleans_dict_with_specific_keys(self):
        assert clean(dict, keys={
            '200': int,
            300: str,
        })({
            100: 'foo',
            '200': 'bar',
            300: 'baz',
        }) == {
            100: 'foo',
            200: 'bar',
            '300': 'baz',
        }

    def it_cleans_keys_and_nested_values(self):
        assert clean(dict, keys=int, values=clean(dict, values={
            'amount': Decimal,
            'object_id': int,
            'info': clean(dict, values={
                'pack_id': int,
                'amount': Decimal,
            })
        }))({
            '1234': {
                'amount': '123.45',
                'object_id': '123',
                'info': {
                    'pack_id': '1234',
                    'amount': '123.45',
                },
            },
        }) == {
            1234: {
                'amount': Decimal('123.45'),
                'object_id': 123,
                'info': {
                    'pack_id': 1234,
                    'amount': Decimal('123.45'),
                },
            },
        }

    def it_silences_key_errors(self):
        assert clean(dict, keys={
            'not_there': int
        }, values={
            'not_there': int
        })({}) == {}

    def it_raises_key_errors_if_asked(self):
        with pytest.raises(KeyError):
            clean(dict, keys={
                'not_there': int
            }, values={
                'not_there': int
            }, raises=True)({})

    def it_cleans_php(self):
        assert clean('php')(u'a:1:{s:3:"foo";s:3:"bar";}') == {b"foo": b"bar"}

    def it_cleans_timestamps(self):
        assert clean('timestamp')(u'1234567') == \
            datetime.datetime.fromtimestamp(float(1234567))

    def it_cleans_dates(self):
        assert clean('date')(u'Apr/01/2014') == datetime.date(2014, 4, 1)

    def it_cleans_decimals_with_commas(self):
        assert clean('decimal')(u'1,200.21') == Decimal('1200.21')

    def it_cleans_ints_with_commas(self):
        assert clean('int')(u'1,221') == 1221

    def it_cleans_ints_as_int_type(self):
        assert clean('int')(1) == 1

    def it_cleans_decimal_as_decimal_type(self):
        assert clean('decimal')(Decimal('1')) == Decimal('1')

    def it_cleans_numerical_values_with_empty_string_as_none(self):
        assert clean('int')('') is None
        assert clean('decimal')('') is None

    def it_cleans_numerical_values_with_none_as_none(self):
        assert clean('int')(None) is None
        assert clean('decimal')(None) is None

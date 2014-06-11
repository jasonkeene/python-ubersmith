from decimal import Decimal

import pytest

from ubersmith.clean import clean


class DescribeClean:
    def it_cleans_ints(self):
        assert clean(int).apply('123') == 123

    def it_cleans_list(self):
        assert clean(list).apply([1, 2, 3, 4]) == [1, 2, 3, 4]

    def it_cleans_list_values(self):
        cleaner = clean(list, values=str)
        assert cleaner.apply([1, 2, 3, 4]) == ['1', '2', '3', '4']

    def it_cleans_specific_values_in_list(self):
        cleaner = clean(list, values=[
            (1, str),
            (3, int),
            (5, Decimal),
        ])
        result = cleaner.apply(range(6))
        assert result == [0, '1', 2, 3, 4, Decimal(5)]
        assert type(result[1]) is str
        assert type(result[3]) is int
        assert type(result[5]) is Decimal

    def it_silences_index_errors_in_cleaners(self):
        cleaner = clean(list, values=[
            (1, str),
            (3, int),
            (5, Decimal),
        ])
        result = cleaner.apply(range(2))
        assert result == [0, '1']
        assert type(result[1]) is str

    def it_raises_idex_errors_if_asked(self):
        cleaner = clean(list, values=[
            (1, str),
            (3, int),
            (5, Decimal),
        ], raises=True)
        with pytest.raises(IndexError):
            cleaner.apply(range(2))

    def it_cleans_recursive_lists(self):
        cleaner = clean(list, values=[
            (1, str),
            (3, int),
            (5, clean(list, values=int)),
        ])
        result = cleaner.apply([0, 1, 2, 3, 4, ['10', '20', '30']])
        assert result == [0, '1', 2, 3, 4, [10, 20, 30]]

    def it_cleans_dicts(self):
        assert clean(dict).apply({'key': 'value'}) == {'key': 'value'}

    def it_cleans_dict_keys(self):
        assert clean(dict, keys=int).apply({
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
        }).apply({
            '200': 'foo',
            300: 'bar',
        }) == {
            200: 'foo',
            '300': 'bar',
        }

    def it_cleans_keys_and_nested_values(self):
        assert clean(dict, keys=int, values=clean(dict, values={
            'amount': Decimal,
            'object_id': int,
            'info': clean(dict, values={
                'pack_id': int,
                'amount': Decimal,
            })
        })).apply({
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

from ubersmith.utils import append_qs, to_nested_php_args


UNICODE_STRING = u'\u0bb8\u0bcd\u0bb1\u0bc0\u0ba9\u0bbf\u0bb5\u0bbe\u0bb8 ' \
                 u'\u0bb0\u0bbe\u0bae\u0bbe\u0ba9\u0bc1\u0b9c\u0ba9\u0bcd ' \
                 u'\u0b90\u0baf\u0b99\u0bcd\u0b95\u0bbe\u0bb0\u0bcd'

URL_FMT = 'http://domain.tld/path/?test1=val&test2{0}#hash'
URL = URL_FMT.format('')


class DescribeAppendQS:
    def it_appends_string(self):
        qs = 'test3=val1&test3=val2'
        assert append_qs(URL, qs) == URL_FMT.format('=&' + qs)

    def it_appends_dict(self):
        qs = {'test3': 'val'}
        assert append_qs(URL, qs) == URL_FMT.format('=&test3=val')

    def it_appends_dict_with_nested_list(self):
        qs = {'test3': ['val1', 'val2']}
        assert append_qs(URL, qs) == URL_FMT.format('=&test3=val1&test3=val2')

    def it_appends_list_of_tuples(self):
        qs = [('test3', 'val1'), ('test3', 'val2')]
        assert append_qs(URL, qs) == URL_FMT.format('=&test3=val1&test3=val2')

    def it_appends_unicode(self):
        qs = {'test3': UNICODE_STRING}
        assert append_qs(URL, qs) == URL_FMT.format(''.join([
            '=&test3=%E0%AE%B8%E0%AF%8D%E0%AE%B1%E0%AF%80%E0%AE%A9%E0%AE%BF',
            '%E0%AE%B5%E0%AE%BE%E0%AE%B8+%E0%AE%B0%E0%AE%BE%E0%AE%AE%E0%AE',
            '%BE%E0%AE%A9%E0%AF%81%E0%AE%9C%E0%AE%A9%E0%AF%8D+%E0%AE%90%E0',
            '%AE%AF%E0%AE%99%E0%AF%8D%E0%AE%95%E0%AE%BE%E0%AE%B0%E0%AF%8D',
        ]))


class DescribeToNestedPHPArgs:
    def it_flattens_nested_dict(self):
        data = {'dict': {'key': 'value'}}
        assert to_nested_php_args(data) == {'dict[key]': 'value'}

    def it_flattens_multiple_levels_of_nested_dicts(self):
        data = {
            'dict': {
                'muffin': {
                    'taco': {
                        'puffin': 'value',
                    },
                },
            },
        }
        assert to_nested_php_args(data) == {
            'dict[muffin][taco][puffin]': 'value',
        }

    def it_flattens_nested_dicts_with_lists(self):
        data = {'top': {'list': ['a', 'b', 'c']}}
        assert to_nested_php_args(data) == {
            'top[list][0]': 'a',
            'top[list][1]': 'b',
            'top[list][2]': 'c',
        }

    def it_flattens_list_of_tuples(self):
        data = [('top', {'list': ['a', 'b', 'c']})]
        assert to_nested_php_args(data) == [
            ('top[list][2]', 'c'),
            ('top[list][0]', 'a'),
            ('top[list][1]', 'b'),
        ]

import pytest

from ubersmith.utils import (
    append_qs,
    urlencode_unicode,
    to_nested_php_args,
    get_filename,
)


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

    def it_raises_type_error_for_bad_query_string_type(self):
        with pytest.raises(TypeError) as e:
            append_qs(URL, object())
        assert str(e.value) == 'Unexpected query_string type'

    def it_appends_unicode(self):
        qs = {'test3': UNICODE_STRING}
        assert append_qs(URL, qs) == URL_FMT.format(''.join([
            '=&test3=%E0%AE%B8%E0%AF%8D%E0%AE%B1%E0%AF%80%E0%AE%A9%E0%AE%BF',
            '%E0%AE%B5%E0%AE%BE%E0%AE%B8+%E0%AE%B0%E0%AE%BE%E0%AE%AE%E0%AE',
            '%BE%E0%AE%A9%E0%AF%81%E0%AE%9C%E0%AE%A9%E0%AF%8D+%E0%AE%90%E0',
            '%AE%AF%E0%AE%99%E0%AF%8D%E0%AE%95%E0%AE%BE%E0%AE%B0%E0%AF%8D',
        ]))


class DescribeUrlencodeUnicode:
    def it_encodes_dicts(self):
        assert urlencode_unicode({'test': 'asdf'}) == 'test=asdf'

    def it_encodes_lists(self):
        assert urlencode_unicode([('test', 'asdf')]) == 'test=asdf'

    def it_encodes_unicode(self):
        assert urlencode_unicode({"test": UNICODE_STRING}) == ''.join([
            'test=%E0%AE%B8%E0%AF%8D%E0%AE%B1%E0%AF%80%E0%AE%A9%E0%AE%BF',
            '%E0%AE%B5%E0%AE%BE%E0%AE%B8+%E0%AE%B0%E0%AE%BE%E0%AE%AE%E0%AE',
            '%BE%E0%AE%A9%E0%AF%81%E0%AE%9C%E0%AE%A9%E0%AF%8D+%E0%AE%90%E0',
            '%AE%AF%E0%AE%99%E0%AF%8D%E0%AE%95%E0%AE%BE%E0%AE%B0%E0%AF%8D',
        ])

    def it_raises_type_error_on_bad_data_types(self):
        with pytest.raises(TypeError) as e:
            urlencode_unicode(object())
        assert str(e.value) == 'not a valid non-string sequence or mapping object'


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

    @pytest.mark.parametrize(['data', 'result'], [
        ([
            ('x', 'y'),
        ], [
            ('x', 'y'),
        ]),
        ([
            ('x', [1, 2, 3]),
        ], [
            ('x[0]', 1),
            ('x[1]', 2),
            ('x[2]', 3),
        ]),
        ([
            ('top', {
                'list': ['a', 'b', 'c'],
            }),
        ], [
            ('top[list][0]', 'a'),
            ('top[list][1]', 'b'),
            ('top[list][2]', 'c'),
        ]),
    ])
    def it_flattens_nested_lists_of_tuples(self, data, result):
        assert sorted(to_nested_php_args(data)) == result

    def it_raises_type_error_on_bad_data_types(self):
        x = object()
        with pytest.raises(TypeError) as e:
            to_nested_php_args(x)
        assert str(e.value) == "expected dict or list, got {0}".format(type(x))


class DescribeGetFilename:
    def it_gets_filename(self):
        assert get_filename('attachment; filename="fname.ext"') == "fname.ext"

    def it_handles_unquoted_filenames(self):
        assert get_filename('inline; filename=fname.ext') == "fname.ext"

    def it_returns_none_if_none_was_passed_in(self):
        assert get_filename(None) is None

    @pytest.mark.parametrize('disposition', [
        'no-params'
        'inline; no-filename'
        'inline; param-that-is-not-filename="foobar"'
    ])
    def it_returns_none_if_disposition_is_malformed(self, disposition):
        assert get_filename(disposition) is None

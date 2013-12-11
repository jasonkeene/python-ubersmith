"""Tests for utils."""

from unittest import TestCase

from ubersmith import utils


UNICODE_STRING = u'\u0bb8\u0bcd\u0bb1\u0bc0\u0ba9\u0bbf\u0bb5\u0bbe\u0bb8 ' \
                 u'\u0bb0\u0bbe\u0bae\u0bbe\u0ba9\u0bc1\u0b9c\u0ba9\u0bcd ' \
                 u'\u0b90\u0baf\u0b99\u0bcd\u0b95\u0bbe\u0bb0\u0bcd'


class AppendQsTestCase(TestCase):
    def setUp(self):
        self.url = 'http://domain.tld/path/?test1=val&test2#hash'
        self.result = 'http://domain.tld/path/?test1=val&test2{0}#hash'

    def test_string_qs(self):
        qs = 'test3=val1&test3=val2'
        result = self.result.format('=&test3=val1&test3=val2')
        self.assertEqual(utils.append_qs(self.url, qs), result)

    def test_dict_qs(self):
        qs = {'test3': 'val'}
        result = self.result.format('=&test3=val')
        self.assertEqual(utils.append_qs(self.url, qs), result)

    def test_nested_qs(self):
        qs = {'test3': ['val1', 'val2']}
        result = self.result.format('=&test3=val1&test3=val2')
        self.assertEqual(utils.append_qs(self.url, qs), result)

    def test_list_qs(self):
        qs = [('test3', 'val1'), ('test3', 'val2')]
        result = self.result.format('=&test3=val1&test3=val2')
        self.assertEqual(utils.append_qs(self.url, qs), result)

    def test_unicode_qs(self):
        qs = {'test3': UNICODE_STRING}
        utils.append_qs(self.url, qs)
        result = self.result.format('=&test3=%E0%AE%B8%E0%AF%8D%E0%AE%B1%E0%AF%80%E0%AE%A9%E0%AE%BF%E0%AE%B5%E0%AE%BE%E0%AE%B8+%E0%AE%B0%E0%AE%BE%E0%AE%AE%E0%AE%BE%E0%AE%A9%E0%AF%81%E0%AE%9C%E0%AE%A9%E0%AF%8D+%E0%AE%90%E0%AE%AF%E0%AE%99%E0%AF%8D%E0%AE%95%E0%AE%BE%E0%AE%B0%E0%AF%8D')
        self.assertEqual(utils.append_qs(self.url, qs), result)


class FlattenDictPhpArrayTestCase(TestCase):
    def test_single_level_dict(self):
        data = {'dict': {'key': 'value'}}
        result = utils.convert_to_php_post(data)
        self.assertEqual(result, {'dict[key]': 'value'})

    def test_nested_dicts(self):
        data = {
            'dict': {
                'muffin': {
                    'taco': {
                        'puffin': 'value'
                    }
                }
            }
        }
        result = utils.convert_to_php_post(data)
        self.assertEqual(result, {'dict[muffin][taco][puffin]': 'value'})

    def test_lists(self):
        data = {'top': {'list': ['a', 'b', 'c']}}
        result = utils.convert_to_php_post(data)
        self.assertEqual(result, {
            'top[list][0]': 'a',
            'top[list][1]': 'b',
            'top[list][2]': 'c',
        })

    def test_accepts_list_of_tuples(self):
        data = [('top', {'list': ['a', 'b', 'c']})]
        result = utils.convert_to_php_post(data)
        self.assertEqual(result, [
            ('top[list][2]', 'c'),
            ('top[list][0]', 'a'),
            ('top[list][1]', 'b'),
        ])

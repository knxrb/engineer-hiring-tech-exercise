import unittest

from src.urlhelper import is_valid_url, is_same_domain, get_domain, get_clean_url, is_scrapeable_url, from_relative_url


class UrlHelperTests(unittest.TestCase):
    _test_domain: str = 'www.google.com'
    _test_ip: str = '192.168.1.10:6000'

    def test_is_valid_url__returns_true__with_valid_url(self):
        url_to_test = 'https://www.google.com'

        is_valid = is_valid_url(url_to_test)

        self.assertTrue(is_valid)

    def test_is_valid_url__returns_false__with_invalid_url(self):
        url_to_test = 'www.google.com'

        is_valid = is_valid_url(url_to_test)

        self.assertFalse(is_valid)

    def test_is_same_domain__returns_true__with_matching_url(self):

        url_to_test = 'https://www.google.com'

        matches = is_same_domain(url_to_test, self._test_domain)

        self.assertTrue(matches)

    def test_is_same_domain__returns_false__with_non_matching_url(self):
        url_to_test = 'https://www.yahoo.com'

        matches = is_same_domain(url_to_test, self._test_domain)

        self.assertFalse(matches)

    def test_is_same_domain__returns_false__with_non_matching_url_subdomain(self):
        url_to_test = 'https://analytics.google.com'

        matches = is_same_domain(url_to_test, self._test_domain)

        self.assertFalse(matches)

    def test_get_domain__returns_hostname_value__with_subdomain(self):
        url_to_test = 'https://www.yahoo.com'

        domain = get_domain(url_to_test)

        self.assertEqual(domain, 'www.yahoo.com')

    def test_get_domain__returns_hostname_value__without_subdomain(self):
        url_to_test = 'https://yahoo.com'

        domain = get_domain(url_to_test)

        self.assertEqual(domain, 'yahoo.com')

    def test_get_clean_url__returns_cleaned_url__for_basic_url(self):
        url_to_test = 'https://www.google.co.uk'

        cleaned_url = get_clean_url(url_to_test)

        self.assertEqual(cleaned_url, 'https://www.google.co.uk')

    def test_get_clean_url__returns_cleaned_url__for_basic_url_with_trailing_slash(self):
        url_to_test = 'https://www.google.co.uk/'

        cleaned_url = get_clean_url(url_to_test)

        self.assertEqual(cleaned_url, 'https://www.google.co.uk')

    def test_get_clean_url__returns_cleaned_url__for_basic_url_with_path(self):
        url_to_test = 'https://www.google.co.uk/a/path/goes/here/'

        cleaned_url = get_clean_url(url_to_test)

        self.assertEqual(cleaned_url, 'https://www.google.co.uk/a/path/goes/here')

    def test_get_clean_url__returns_cleaned_url__for_basic_url_with_query_params(self):
        url_to_test = 'https://www.google.co.uk/a/path/goes/here/?id=ABC&something=else'

        cleaned_url = get_clean_url(url_to_test)

        self.assertEqual(cleaned_url, 'https://www.google.co.uk/a/path/goes/here')

    def test_is_scrapeable_url__returns_true__for_valid_url_in_same_domain(self):
        url_to_test = 'https://www.google.com/a/path/goes/here/?id=ABC&something=else'

        is_scrapeable = is_scrapeable_url(url_to_test, self._test_domain)

        self.assertTrue(is_scrapeable)

    def test_is_scrapeable_url__returns_false__for_valid_url_in_different_domain(self):
        url_to_test = 'https://www.yahoo.com/a/path/goes/here/?id=ABC&something=else'

        is_scrapeable = is_scrapeable_url(url_to_test, self._test_domain)

        self.assertFalse(is_scrapeable)

    def test_is_scrapeable_url__returns_false__for_valid_url_in_different_subdomain(self):
        url_to_test = 'https://analytics.google.com/a/path/goes/here/?id=ABC&something=else'

        is_scrapeable = is_scrapeable_url(url_to_test, self._test_domain)

        self.assertFalse(is_scrapeable)

    def test_is_scrapeable_url__returns_false__for_no_url(self):
        url_to_test = None

        is_scrapeable = is_scrapeable_url(url_to_test, self._test_domain)

        self.assertFalse(is_scrapeable)

    def test_from_relative_url__returns_full_url__for_path(self):
        origin_url = 'https://www.google.com/a/path/here'
        relative_url_to_test = '/relative/path'

        full_url = from_relative_url(origin_url, relative_url_to_test)

        self.assertEqual(full_url, 'https://www.google.com/relative/path')

    def test_from_relative_url__returns_full_url__without_query_params(self):
        origin_url = 'https://www.google.com/a/path/here?query=value&something=written'
        relative_url_to_test = '/relative/path/b?query=false'

        full_url = from_relative_url(origin_url, relative_url_to_test)

        self.assertEqual(full_url, 'https://www.google.com/relative/path/b')

    def test_from_relative_url__returns_full_url__if_relative_url_is_root(self):
        origin_url = 'https://www.google.com'
        relative_url_to_test = '/'

        full_url = from_relative_url(origin_url, relative_url_to_test)

        self.assertEqual(full_url, 'https://www.google.com')

import unittest
from crawl import get_urls_from_html

class TestCrawl(unittest.TestCase):
    def test_get_urls_1_from_html(self):
        base_url = "http://example.com"
        html = "<html><head><title>Test</title></head><body><a href='/files'>Link</a></body></html>"
        actual = get_urls_from_html(html, base_url)
        expected = ["http://example.com/files"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)

    def test_get_no_urls_2_from_html(self):
        base_url = "https://example.com"
        html = '<html><body><a href="/base/deeper"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(html, base_url)
        expected = ["https://example.com/base/deeper"]
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()
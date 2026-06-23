import unittest
from crawl import get_images_from_html

class TestCrawl(unittest.TestCase):
    def test_get_images_from_html(self):
        base_url = "https://example.com"
        html = "<html><head><title>Test</title></head><body><img src='/images/logo.png' alt='Logo'></body></html>"
        actual = get_images_from_html(html, base_url)
        expected = ["https://example.com/images/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_2_from_html(self):
        base_url = "https://example.com"
        html = "<html><head><title>Test</title></head><body><img src='/images/test.png' alt='Logo'></body></html>"
        actual = get_images_from_html(html, base_url)
        expected = ["https://example.com/images/test.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html(self):
        base_url = "https://crawler-test.com"
        html = "<html><head><title>Test</title></head><body><img src='/images/logo/final.png' alt='Logo'></body></html>"
        actual = get_images_from_html(html, base_url)
        expected = ["https://crawler-test.com/images/logo/final.png"]
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()
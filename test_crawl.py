import unittest
from crawl import normalize_url

class TestCrawl(unittest.TestCase):
    def test_normalize_url_basic(self):
        self.assertEqual(normalize_url("https://www.boot.dev/blog/path"), "www.boot.dev/blog/path")

    def test_normalize_url_1(self):
        self.assertEqual(normalize_url("http://www.boot.dev/blog/path/"), "www.boot.dev/blog/path")

    def test_normalize_url_2(self):
        self.assertEqual(normalize_url("https://www.boot.dev/blog/path/"), "www.boot.dev/blog/path")

    def test_normalize_url_3(self):
        self.assertEqual(normalize_url("http://www.boot.dev/blog/path"), "www.boot.dev/blog/path")

    def test_normalize_url_4(self):
        self.assertEqual(normalize_url("https://www.boot.dev/blog/path"), "www.boot.dev/blog/path")

    def test_normalize_url_5(self):
        self.assertEqual(normalize_url("www.boot.dev/blog/path/"), "www.boot.dev/blog/path")

    def test_normalize_url_6(self):
        self.assertEqual(normalize_url("www.boot.dev/blog/path"), "www.boot.dev/blog/path")

    def test_normalize_url_7(self):
        self.assertEqual(normalize_url("https://www.boot.dev/blog/path/test"), "www.boot.dev/blog/path/test")

if __name__ == "__main__":
    unittest.main()
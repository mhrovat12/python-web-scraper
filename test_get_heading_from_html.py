import unittest
from crawl import get_heading_from_html

class TestCrawl(unittest.TestCase):
    def test_get_heading1_from_html(self):
        html = "<html><head><title>Test</title></head><body><h1>Heading 1</h1><h2>Heading 2</h2><main><p>Content</p></main></body></html>"
        actual = get_heading_from_html(html)
        expected = "Heading 1"
        self.assertEqual(actual, expected)
    
    def test_get_heading2_from_html(self):
        html = "<html><head><title>Test</title></head><body><h2>Heading 2</h2><main><p>Content</p></main></body></html>"
        actual = get_heading_from_html(html)
        expected = "Heading 2"
        self.assertEqual(actual, expected)

    def test_get_no_heading_from_html(self):
        html = "<html><head><title>Test</title></head><body><main><p>Content</p></main></body></html>"
        actual = get_heading_from_html(html)
        expected = ""
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()
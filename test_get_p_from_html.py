import unittest
from crawl import get_heading_from_html, get_first_paragraph_from_html as get_p_from_html

class TestCrawl(unittest.TestCase):
    def test_get_p_1_from_html(self):
        html = "<html><head><title>Test</title></head><body><h1>Heading 1</h1><h2>Heading 2</h2><main><p>Content</p></main></body></html>"
        actual = get_p_from_html(html)
        expected = "Content"
        self.assertEqual(actual, expected)

    def test_get_p_2_from_html(self):
        html = '''<html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
            </main>
        </body></html>'''
        actual = get_p_from_html(html)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)

    def test_get_no_heading_from_html(self):
        html = "<html><head><title>Test</title></head><body></body></html>"
        actual = get_heading_from_html(html)
        expected = ""
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()
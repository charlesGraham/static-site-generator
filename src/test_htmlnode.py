import unittest

from htmlnode import HtmlNode


class TestHtmlNode(unittest.TestCase):
    # def test_to_html(self):
    #     node = HtmlNode(tag="div", value="Hello, world!", children=[], props={})
    #     self.assertEqual(node.to_html(), "<div>Hello, world!</div>")

    def test_props_to_html(self):
        node = HtmlNode(
            tag="div", value="Hello, world!", children=[], props={"class": "test"}
        )
        self.assertEqual(node.props_to_html(), "class=test")

    def test_repr(self):
        node = HtmlNode(
            tag="div", value="Hello, world!", children=[], props={"class": "test"}
        )
        self.assertEqual(
            repr(node),
            "HtmlNode(tag=div, value=Hello, world!, children=[], props={'class': 'test'})",
        )

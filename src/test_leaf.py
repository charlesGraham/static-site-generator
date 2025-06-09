import unittest

from leaf import Leaf
from textnode import TextNode, TextType


class TestLeaf(unittest.TestCase):
    def test_leaf_to_html(self):
        node = Leaf("p", "Hello World!")
        self.assertEqual(node.to_html(), "<p>Hello World!</p>")

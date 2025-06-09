import unittest

from parentnode import ParentNode
from leaf import Leaf


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = Leaf("span", "child")
        print(f"child_node from test: {child_node.to_html()}")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


def test_to_html_with_grandchildren(self):
    grandchild_node = Leaf("b", "grandchild")
    child_node = ParentNode("span", [grandchild_node])
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(
        parent_node.to_html(),
        "<div><span><b>grandchild</b></span></div>",
    )

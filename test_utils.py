import unittest

from textnode import TextNode, TextType
from utils import extract_markdown_images, split_nodes_delimiter, text_node_to_html_node


class TestUtils(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_split_nodes_delimiter(self):
        nodes = [
            TextNode("This is a text node", TextType.NORMAL_TEXT),
            TextNode("This is a text node", TextType.NORMAL_TEXT),
        ]
        delimiter = " "
        text_type = TextType.NORMAL_TEXT
        new_nodes = split_nodes_delimiter(nodes, delimiter, text_type)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This", TextType.NORMAL_TEXT),
                TextNode("is", TextType.NORMAL_TEXT),
                TextNode("a", TextType.NORMAL_TEXT),
                TextNode("text", TextType.NORMAL_TEXT),
                TextNode("node", TextType.NORMAL_TEXT),
            ],
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

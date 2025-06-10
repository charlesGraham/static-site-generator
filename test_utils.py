import unittest

from textnode import TextNode, TextType
from utils import (
    extract_markdown_images,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_node_to_html_node,
    text_to_textnodes,
    markdown_to_blocks,
)


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

    def test_split_nodes_image(self):
        nodes = [
            TextNode("This is a text node", TextType.NORMAL_TEXT),
            TextNode("This is a text node", TextType.IMAGE),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertEqual(new_nodes, [TextNode("This is a text node", TextType.IMAGE)])

    def test_split_nodes_link(self):
        nodes = [
            TextNode("This is a text node", TextType.NORMAL_TEXT),
            TextNode("This is a text node", TextType.LINK),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertEqual(new_nodes, [TextNode("This is a text node", TextType.LINK)])

    def test_text_to_textnodes(self):
        text = "This is a text node with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://www.google.com)"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("This is a text node with an image", TextType.NORMAL_TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("and a link", TextType.NORMAL_TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com"),
            ],
        )

    def test_markdown_to_blocks(self):
        md = """# This is a heading\n\nThis is a paragraph of text. It has some **bold** and _italic_ words inside of it.\n\n- This is the first list item in a list block\n- This is a list item\n- This is another list item\n\n"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )

        md2 = """\n\n# Heading\n\n\nParagraph\n\n\n\n- List item\n\n"""
        blocks2 = markdown_to_blocks(md2)
        self.assertEqual(
            blocks2,
            [
                "# Heading",
                "Paragraph",
                "- List item",
            ],
        )

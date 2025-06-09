import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)
        self.assertNotEqual(node, TextNode("This is a text node", TextType.ITALIC_TEXT))
        self.assertNotEqual(node, TextNode("This is a text node", TextType.CODE_TEXT))
        self.assertNotEqual(node, TextNode("This is a text node", TextType.LINK))
        self.assertNotEqual(node, TextNode("This is a text node", TextType.IMAGE))
        self.assertNotEqual(
            node,
            TextNode(
                "This is a text node",
                TextType.BOLD_TEXT,
                url="https://www.test-url.com",
            ),
        )


if __name__ == "__main__":
    unittest.main()

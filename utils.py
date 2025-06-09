from leaf import Leaf
from textnode import TextNode, TextType


def text_node_to_html_node(text_node):
    if text_node.text_type not in [
        TextType.NORMAL_TEXT,
        TextType.BOLD_TEXT,
        TextType.ITALIC_TEXT,
        TextType.CODE_TEXT,
        TextType.LINK,
        TextType.IMAGE,
    ]:
        raise ValueError(f"Invalid text type: {text_node.text_type}")

    if text_node.text_type == TextType.NORMAL_TEXT:
        return Leaf(tag=None, value=text_node.text)
    elif text_node.text_type == TextType.BOLD_TEXT:
        return Leaf(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC_TEXT:
        return Leaf(tag="i", value=text_node.text)
    elif text_node.text_type == TextType.CODE_TEXT:
        return Leaf(tag="code", value=text_node.text)
    elif text_node.text_type == TextType.LINK:
        return Leaf(tag="a", value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return Leaf(
            tag="img", value="", props={"src": text_node.url, "alt": text_node.text}
        )


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == text_type:
            new_nodes.extend(node.split(delimiter))
        else:
            new_nodes.append(node)
    return new_nodes

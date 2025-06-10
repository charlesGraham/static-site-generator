import re
from leaf import Leaf
from textnode import TextNode, TextType
from enum import Enum
from parentnode import ParentNode


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


def extract_markdown_images(text):
    # returns a list of tuples: (alt_text, url)
    pattern = r"!\[([^\]]*)\]\(([^)]+)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    # returns a list of tuples: (text, url)
    pattern = r"\[([^\]]+)\]\(([^)]+)\)"
    matches = re.findall(pattern, text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == TextType.IMAGE:
            new_nodes.append(node)
        else:
            new_nodes.append(node)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == TextType.LINK:
            new_nodes.append(node)
        else:
            new_nodes.append(node)
    return new_nodes


def text_to_textnodes(text):
    images = extract_markdown_images(text)
    links = extract_markdown_links(text)
    placeholder_map = {}
    temp_text = text

    for i, (alt, url) in enumerate(images):
        placeholder = f"__IMAGE_PLACEHOLDER_{i}__"
        temp_text = temp_text.replace(f"![{alt}]({url})", placeholder, 1)
        placeholder_map[placeholder] = ("IMAGE", alt, url)

    for i, (label, url) in enumerate(links):
        placeholder = f"__LINK_PLACEHOLDER_{i}__"
        temp_text = temp_text.replace(f"[{label}]({url})", placeholder, 1)
        placeholder_map[placeholder] = ("LINK", label, url)

    combined_pattern = (
        r"(__IMAGE_PLACEHOLDER_\d+__)"  # image placeholder
        r"|(__LINK_PLACEHOLDER_\d+__)"  # link placeholder
        r"|\*\*([^*]+)\*\*"  # bold
        r"|_([^_]+)_"  # italic
        r"|`([^`]+)`"  # code
    )
    nodes = []
    pos = 0
    for match in re.finditer(combined_pattern, temp_text):
        start, end = match.span()

        if start > pos:
            normal_text = temp_text[pos:start]
            if normal_text:
                nodes.append(TextNode(normal_text, TextType.NORMAL_TEXT))
        if match.group(1):  # image placeholder
            _, alt, url = placeholder_map[match.group(1)]
            nodes.append(TextNode(alt, TextType.IMAGE, url))
        elif match.group(2):  # link placeholder
            _, label, url = placeholder_map[match.group(2)]
            nodes.append(TextNode(label, TextType.LINK, url))
        elif match.group(3):  # bold
            nodes.append(TextNode(match.group(3), TextType.BOLD_TEXT))
        elif match.group(4):  # italic
            nodes.append(TextNode(match.group(4), TextType.ITALIC_TEXT))
        elif match.group(5):  # code
            nodes.append(TextNode(match.group(5), TextType.CODE_TEXT))
        pos = end

    if pos < len(temp_text):
        trailing_text = temp_text[pos:]
        if trailing_text:
            nodes.append(TextNode(trailing_text, TextType.NORMAL_TEXT))
    return nodes


def markdown_to_blocks(markdown):
    blocks = [block.strip() for block in markdown.split("\n\n")]
    return [block for block in blocks if block]


class BlockType(Enum):
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    PARAGRAPH = "paragraph"


def block_to_block_type(block):
    lines = block.split("\n")
    if len(lines) == 1 and re.match(r"^#{1,6} ", lines[0]):
        return BlockType.HEADING
    if lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if all(line.strip().startswith(">") for line in lines if line.strip()):
        return BlockType.QUOTE
    if all(line.strip().startswith("- ") for line in lines if line.strip()):
        return BlockType.UNORDERED_LIST
    ordered = True
    for idx, line in enumerate([l for l in lines if l.strip()]):
        if not re.match(rf"{idx+1}\. ", line.strip()):
            ordered = False
            break
    if ordered and len(lines) > 0 and lines[0].strip().startswith("1. "):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def text_to_children(text):
    nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in nodes]


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            level = len(block.split(" ")[0])
            text = block[level + 1 :] if block[level] == " " else block[level:]
            tag = f"h{level}"
            children.append(Leaf(tag, block[level + 1 :].strip()))
        elif block_type == BlockType.CODE:
            code_content = "\n".join(block.split("\n")[1:-1])
            code_node = text_node_to_html_node(
                TextNode(code_content, TextType.CODE_TEXT)
            )
            children.append(Leaf("pre", code_node.value))
        elif block_type == BlockType.QUOTE:
            quote_lines = [line.lstrip("> ").rstrip() for line in block.split("\n")]
            quote_text = " ".join(quote_lines)
            quote_children = text_to_children(quote_text)
            children.append(ParentNode("blockquote", quote_children))
        elif block_type == BlockType.UNORDERED_LIST:
            items = [line[2:].strip() for line in block.split("\n") if line.strip()]
            li_nodes = [ParentNode("li", text_to_children(item)) for item in items]
            children.append(ParentNode("ul", li_nodes))
        elif block_type == BlockType.ORDERED_LIST:
            items = [
                line[line.find(" ") + 1 :].strip()
                for line in block.split("\n")
                if line.strip()
            ]
            li_nodes = [ParentNode("li", text_to_children(item)) for item in items]
            children.append(ParentNode("ol", li_nodes))
        else:
            para_children = text_to_children(block)
            children.append(ParentNode("p", para_children))
    return ParentNode("div", children)


def extract_title(markdown):
    for line in markdown.splitlines():
        if line.strip().startswith("# "):
            return line.strip()[2:].strip()
    raise Exception("No h1 header found in markdown")

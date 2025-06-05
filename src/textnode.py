from enum import Enum


class TextType(Enum):
    NORMAL_TEXT = "Normal_text"
    BOLD_TEXT = "Bold text"
    ITALIC_TEXT = "Italic text"
    CODE_TEXT = "Code text"
    LINK = "https://www.example.com"
    IMAGE = "https://www.example.com/image.png"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

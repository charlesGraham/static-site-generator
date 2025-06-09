from htmlnode import HtmlNode


class ParentNode(HtmlNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        print(f"children: {self.children}")
        if self.tag is None:
            raise ValueError("tag is a required property")
        if self.children is None:
            raise ValueError("children is a required property")
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

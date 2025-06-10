import os
import shutil
from textnode import TextNode, TextType
from utils import markdown_to_html_node, extract_title


def copy_static_to_public():
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")

    src_css = os.path.join("static", "index.css")
    if os.path.exists(src_css):
        shutil.copy(src_css, os.path.join("public", "index.css"))
        print(f"Copied CSS: public/index.css")

    src_images = os.path.join("static", "images")
    dst_images = os.path.join("public", "images")
    os.mkdir(dst_images)
    for item in os.listdir(src_images):
        src_path = os.path.join(src_images, item)
        if os.path.isfile(src_path) and item.lower().endswith(
            (".png", ".jpg", ".jpeg", ".gif", ".svg")
        ):
            shutil.copy(src_path, dst_images)
            print(f"Copied image: {os.path.join(dst_images, item)}")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r", encoding="utf-8") as f:
        markdown = f.read()
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()
    html_content = markdown_to_html_node(markdown).to_html()
    print(html_content)
    title = extract_title(markdown)
    result = template.replace("{{ Title }}", title).replace(
        "{{ Content }}", html_content
    )
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(result)


def main():
    copy_static_to_public()
    generate_page("content/index.md", "template.html", "public/index.html")
    text_node = TextNode("Hello, World!", TextType.BOLD_TEXT)
    print(text_node)


if __name__ == "__main__":
    main()

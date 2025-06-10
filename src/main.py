import os
import shutil
from textnode import TextNode, TextType


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


def main():
    copy_static_to_public()
    text_node = TextNode("Hello, World!", TextType.BOLD_TEXT)
    print(text_node)


if __name__ == "__main__":
    main()

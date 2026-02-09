import os
import sys
from files import copy_static_files
from markdownhtml import extract_title, markdown_to_html_node


def main(argv=None):
    basepath = argv[1] if argv and len(argv) > 1 else "/"

    copy_static_files()
    generate_page_recursive("content", "template.html", "docs", basepath)


def generate_page(
    from_path: str, template_path: str, dest_path: str, basepath: str
) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    if not os.path.exists(from_path):
        raise FileNotFoundError(f"from_path {from_path} does not exist")
    with open(from_path, "r") as from_file:
        content = from_file.read()
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"template_path {template_path} does not exist")
    with open(template_path, "r") as template_file:
        template = template_file.read()
    html_nodes = markdown_to_html_node(content)
    page_title = extract_title(content)
    final_html = template.replace("{{ Title }}", page_title if page_title else "")
    final_html = final_html.replace("{{ Content }}", html_nodes.to_html())
    final_html = final_html.replace("href=/", f"href={basepath}")
    final_html = final_html.replace("src=/", f"src={basepath}")
    dirname = os.path.dirname(dest_path)
    if dirname and not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(dest_path, "w") as dest_file:
        dest_file.write(final_html)


def generate_page_recursive(
    from_path: str, template_path: str, dest_path: str, basepath: str
) -> None:
    if os.path.isdir(from_path):
        for item in os.listdir(from_path):
            if item.endswith(".md"):
                item_from_path = os.path.join(from_path, item)
                item_dest_path = os.path.join(dest_path, item.replace(".md", ".html"))
                generate_page(item_from_path, template_path, item_dest_path, basepath)
            else:
                if os.path.isdir(os.path.join(from_path, item)):
                    item_dest_path = os.path.join(dest_path, item)
                    generate_page_recursive(
                        os.path.join(from_path, item),
                        template_path,
                        item_dest_path,
                        basepath,
                    )


if __name__ == "__main__":
    main()

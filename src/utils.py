import re
from htmlnode import LeafNode
from textnode import TextNode, TextType

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"invalid text type: {text_node.text_type}")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type:
            new_nodes.append(node)
            continue
        delimiter_count = node.text.count(delimiter)
        if delimiter_count % 2 == 1:
            raise Exception("Unmatched delimiter in text")
        parts = node.text.split(delimiter)
        for i, part in enumerate(parts, start=0):
            if part == "":
                continue
            if i % 2 != 0:
                match delimiter:
                    case "**":
                        new_nodes.append(TextNode(part, TextType.BOLD))
                    case "_":
                        new_nodes.append(TextNode(part, TextType.ITALIC))
                    case "`":
                        new_nodes.append(TextNode(part, TextType.CODE))
            else:
                new_nodes.append(TextNode(part, TextType.TEXT))
    return new_nodes

def extract_markdown_images(text):
    extracted_tuples = []
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    for match in matches:
        extracted_tuples.append((match[0], match[1]))
    return extracted_tuples

def extract_markdown_links(text):
    extracted_tuples = []
    matches = re.findall(r"\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    for match in matches:
        extracted_tuples.append((match[0], match[1]))
    return extracted_tuples

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        parts = extract_markdown_images(node.text)
        if not parts:
            new_nodes.append(node)
            continue
        last_index = 0
        for alt_text, url in parts:
            start_index = node.text.find(f"![{alt_text}]({url})", last_index)
            if start_index > last_index:
                preceding_text = node.text[last_index:start_index]
                new_nodes.append(TextNode(preceding_text, TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            last_index = start_index + len(f"![{alt_text}]({url})")
        if last_index < len(node.text):
            remaining_text = node.text[last_index:]
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        parts = extract_markdown_links(node.text)
        if not parts:
            new_nodes.append(node)
            continue
        last_index = 0
        for link_text, url in parts:
            start_index = node.text.find(f"[{link_text}]({url})", last_index)
            if start_index > last_index:
                preceding_text = node.text[last_index:start_index]
                new_nodes.append(TextNode(preceding_text, TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, url))
            last_index = start_index + len(f"[{link_text}]({url})")
        if last_index < len(node.text):
            remaining_text = node.text[last_index:]
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes
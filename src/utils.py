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



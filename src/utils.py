import re
from htmlnode import LeafNode
from textnode import TextNode, TextType

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    """Convert a TextNode to an HTML LeafNode.
    
    Translates inline text formatting (bold, italic, etc.) into appropriate HTML tags.
    
    Args:
        text_node: A TextNode with a specific TextType.
        
    Returns:
        LeafNode: An HTML leaf node with the appropriate tag and attributes.
        
    Raises:
        ValueError: If text_node has an invalid or unrecognized TextType.
    """
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


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, 
                          text_type: TextType) -> list[TextNode]:
    """Split text nodes on a specific delimiter and apply formatting.
    
    Finds occurrences of a delimiter in TEXT type nodes and creates new nodes
    with the specified text_type for delimited content.
    
    Args:
        old_nodes: List of TextNodes to process.
        delimiter: The delimiter string to search for (**,  _, `).
        text_type: The TextType to apply to delimited content.
        
    Returns:
        list[TextNode]: New list of TextNodes with delimited content formatted.
        
    Raises:
        Exception: If an odd number of delimiters is found (unmatched).
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
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

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    """Extract markdown image links from text.
    
    Finds all markdown image syntax ![alt](url) in text.
    
    Args:
        text: Text potentially containing markdown image links.
        
    Returns:
        list[tuple[str, str]]: List of (alt_text, url) tuples.
    """
    extracted_tuples = []
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    for match in matches:
        extracted_tuples.append((match[0], match[1]))
    return extracted_tuples

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    """Extract markdown links from text.
    
    Finds all markdown link syntax [text](url) in text (excludes images).
    
    Args:
        text: Text potentially containing markdown links.
        
    Returns:
        list[tuple[str, str]]: List of (link_text, url) tuples.
    """
    extracted_tuples = []
    matches = re.findall(r"\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    for match in matches:
        extracted_tuples.append((match[0], match[1]))
    return extracted_tuples

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    """Split text nodes on markdown image links.
    
    Extracts image links from TEXT nodes and creates IMAGE type nodes for them,
    preserving surrounding text content.
    
    Args:
        old_nodes: List of TextNodes to process.
        
    Returns:
        list[TextNode]: New list with IMAGE nodes extracted.
    """
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

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    """Split text nodes on markdown links.
    
    Extracts hyperlinks from TEXT nodes and creates LINK type nodes for them,
    preserving surrounding text content.
    
    Args:
        old_nodes: List of TextNodes to process.
        
    Returns:
        list[TextNode]: New list with LINK nodes extracted.
    """
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

def text_to_textnodes(text: str) -> list[TextNode]:
    """Convert raw markdown text to a list of formatted TextNodes.
    
    Parses markdown syntax and creates appropriately typed TextNodes for
    bold, italic, code, links, and images in the text.
    
    Args:
        text: Raw markdown text to parse.
        
    Returns:
        list[TextNode]: List of TextNodes with proper formatting applied.
    """
    node_list = [TextNode(text, TextType.TEXT)]
    node_list = split_nodes_delimiter(node_list, "**", TextType.TEXT)
    node_list = split_nodes_delimiter(node_list, "_", TextType.TEXT)
    node_list = split_nodes_delimiter(node_list, "`", TextType.TEXT)
    node_list = split_nodes_image(node_list)
    node_list = split_nodes_link(node_list)
    return node_list
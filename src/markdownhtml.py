from blocktypes import BlockType, markdown_to_blocks, block_to_block_type
from htmlnode import HTMLNode, LeafNode, ParentNode
from utils import text_node_to_html_node, text_to_textnodes
import re


def markdown_to_html_node(markdown: str) -> ParentNode:
    """Convert markdown text to an HTML node tree.

    Parses markdown blocks and converts them to appropriate HTML elements,
    including paragraphs, headings, code blocks, quotes, and lists.

    Args:
        markdown: Raw markdown text to convert.

    Returns:
        ParentNode: A div node containing the converted HTML structure.
    """

    blocks: list[str] = markdown_to_blocks(markdown)
    child_nodes: list[HTMLNode] = []
    for block in blocks:
        if block.strip() == "":
            continue
        block_type: BlockType = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                stripped_paragraph: str = re.sub(r"\s+", " ", block).strip()
                text_nodes = text_to_textnodes(stripped_paragraph)
                paragraph_nodes: list[HTMLNode] = []
                for node in text_nodes:
                    paragraph_nodes.append(text_node_to_html_node(node))
                child_nodes.append(
                    ParentNode("p", children=paragraph_nodes, props=None)
                )
            case BlockType.HEADING:
                left_stripped_heading: str = block.lstrip()
                heading_count: int = 0
                for ch in left_stripped_heading:
                    if ch == "#":
                        heading_count += 1
                    else:
                        break
                stripped_heading: str = left_stripped_heading[heading_count:].lstrip()
                text_nodes = text_to_textnodes(stripped_heading)
                heading_nodes: list[HTMLNode] = []
                for node in text_nodes:
                    leaf_heading = text_node_to_html_node(node)
                    heading_nodes.append(leaf_heading)
                child_nodes.append(
                    ParentNode(f"h{heading_count}", children=heading_nodes, props=None)
                )
            case BlockType.CODE:
                lines: list[str] = block.split("\n")
                inner_lines: list[str] = [line.lstrip() for line in lines[1:-1]]
                raw_code: str = "\n".join(inner_lines) + "\n"
                child_nodes.append(
                    ParentNode(
                        "pre",
                        children=[
                            ParentNode(
                                "code",
                                children=[LeafNode(None, raw_code, None)],
                                props=None,
                            )
                        ],
                        props=None,
                    )
                )
            case BlockType.QUOTE:
                left_stripped_quote: str = block.lstrip()
                # remove leading ">" and any whitespace after it
                split_quote: list[str] = left_stripped_quote.split("\n")
                clean_lines: list[str] = []
                for line in split_quote:
                    line = line.lstrip()
                    if line.startswith(">"):
                        line = line.replace("> ", "", 1)
                    clean_lines.append(line)
                joined_quote: str = " ".join(clean_lines).strip()
                text_nodes = text_to_textnodes(joined_quote)
                leaf_nodes: list[HTMLNode] = [
                    text_node_to_html_node(node) for node in text_nodes
                ]
                child_nodes.append(
                    ParentNode("blockquote", children=leaf_nodes, props=None)
                )
            case BlockType.UNORDERED_LIST:
                split_list: list[str] = block.split("\n")
                list_items: list[HTMLNode] = []
                for item in split_list:
                    stripped_item: str = item.replace("- ", "", 1).lstrip().strip()
                    text_nodes = text_to_textnodes(stripped_item)
                    item_nodes: list[HTMLNode] = []
                    for node in text_nodes:
                        item_nodes.append(text_node_to_html_node(node))
                    list_items.append(ParentNode("li", children=item_nodes, props=None))
                child_nodes.append(ParentNode("ul", children=list_items, props=None))
            case BlockType.ORDERED_LIST:
                split_list: list[str] = block.split("\n")
                list_items: list[HTMLNode] = []
                for item in split_list:
                    stripped_item: str = item.split(". ", 1)[1]
                    text_nodes = text_to_textnodes(stripped_item)
                    item_nodes: list[HTMLNode] = []
                    for node in text_nodes:
                        item_nodes.append(text_node_to_html_node(node))
                    list_items.append(ParentNode("li", children=item_nodes, props=None))
                child_nodes.append(ParentNode("ol", children=list_items, props=None))
    return ParentNode("div", children=child_nodes, props=None)


def extract_title(markdown):
    """Extract the title from markdown text.

    The title is defined as the first line that starts with a heading marker (#).
    If no such line exists, raises a ValueError.

    Args:
        markdown: Raw markdown text to extract the title from.

    Returns:
        str | ValueError: The extracted title text, or ValueError if no title is found.
    """
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("no title found")

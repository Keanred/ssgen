from enum import Enum
import re

class BlockType(Enum):
    """Enumeration of block-level markdown element types.
    
    Values:
        PARAGRAPH: Regular paragraph text
        HEADING: Heading (# to ######)
        CODE: Code block (``` ... ```)
        QUOTE: Block quote (> ...)
        UNORDERED_LIST: Unordered list (- items)
        ORDERED_LIST: Ordered list (1. 2. 3. items)
    """
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    """Split markdown text into blocks separated by blank lines.
    
    Blocks are separated by double newlines. Leading/trailing whitespace
    is stripped from each block.
    
    Args:
        markdown: Raw markdown text.
        
    Returns:
        list[str]: List of markdown blocks, each as a string.
    """
    split_markdown = markdown.split("\n\n")
    stripped_markdown = list(map(str.strip, split_markdown))
    for block in stripped_markdown:
        if block == "":
            del block
    return stripped_markdown
   
def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].strip().startswith("```") and lines[-1].strip().startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.lstrip().startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.lstrip().startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.lstrip().startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

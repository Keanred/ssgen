from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    split_markdown = markdown.split("\n\n")
    stripped_markdown = list(map(str.strip, split_markdown))
    for block in stripped_markdown:
        if block == "":
            del block
    return stripped_markdown
   
def block_to_block_type(block):
    if re.match(r"^#{1,6}\s+", block):
        return BlockType.HEADING
    elif re.match(r"^```[\r\n]+[\s\S]*?[\r\n]+```$", block, re.DOTALL):
        return BlockType.CODE
    elif re.match(r"^(?:>\s?.+(?:\r?\n|$))+", block, re.MULTILINE):
        return BlockType.QUOTE
    elif re.match(r"^(?:-\s.+(?:\r?\n|$))+", block, re.MULTILINE):
        return BlockType.UNORDERED_LIST
    elif re.match(r"^(?:\d+\.\s.+(?:\r?\n|$))+", block, re.MULTILINE):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
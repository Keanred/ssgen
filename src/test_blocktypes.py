import unittest
from blocktypes import BlockType, markdown_to_blocks, block_to_block_type

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_single_block(self):
        md = "Just a single paragraph with no separation"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just a single paragraph with no separation"])

    def test_multiple_blocks_with_extra_whitespace(self):
        md = """Block one


Block two


Block three"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block one", "Block two", "Block three"])

    def test_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [""])

    def test_blocks_with_internal_newlines(self):
        md = """First paragraph
with multiple lines
inside it

Second paragraph
also with multiple
lines"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 2)
        self.assertIn("First paragraph", blocks[0])
        self.assertIn("Second paragraph", blocks[1])

    def test_whitespace_only_blocks(self):
        md = """Content


   

More content"""
        blocks = markdown_to_blocks(md)
        self.assertTrue(any("Content" in b for b in blocks))
        self.assertTrue(any("More content" in b for b in blocks))


class TestBlockToBlockType(unittest.TestCase):
    def test_heading_block(self):
        block = "# This is a heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_code_block(self):
        block = """```
def hello():
    print("world")
```"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_quote_block(self):
        block = """> This is a quote
> with multiple lines
> of quoted text"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_unordered_list_block(self):
        block = """- Item one
- Item two
- Item three"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_ordered_list_block(self):
        block = """1. First item
2. Second item
3. Third item"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_paragraph_block(self):
        block = "This is just a regular paragraph of text"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

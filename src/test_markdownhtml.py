import unittest
from markdownhtml import markdown_to_html_node

class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = "# This is a heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>This is a heading</h1></div>")

    def test_heading_with_inline_formatting(self):
        md = "## Heading with **bold** and _italic_"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h2>Heading with <b>bold</b> and <i>italic</i></h2></div>")

    def test_multiple_headings(self):
        md = """# Heading 1

## Heading 2

### Heading 3"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3></div>",
        )

    def test_unordered_list(self):
        md = """- Item one
- Item two
- Item three"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        # Adjust expected output based on actual implementation
        self.assertIn("<ul>", html)
        self.assertIn("</ul>", html)

    def test_ordered_list(self):
        md = """1. First item
2. Second item
3. Third item"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        # Adjust expected output based on actual implementation
        self.assertIn("<ol>", html)
        self.assertIn("</ol>", html)

    def test_quote_block(self):
        md = """> This is a quote
> with multiple lines
> of quoted text"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        # Adjust expected output based on actual implementation
        self.assertIn("<blockquote>", html)
        self.assertIn("</blockquote>", html)

    def test_mixed_blocks(self):
        md = """# Title

This is a paragraph with **bold** text.

- List item 1
- List item 2

```
code block
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        # Verify all block types are present
        self.assertIn("<h1>", html)
        self.assertIn("<p>", html)
        self.assertIn("<ul>", html)
        self.assertIn("<pre>", html)

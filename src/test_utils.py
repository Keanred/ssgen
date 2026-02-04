from utils import text_node_to_html_node, split_nodes_delimiter
from textnode import TextNode, TextType
import unittest

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_bold(self):
        """Test splitting nodes with bold delimiter (**) in the middle"""
        input_nodes = [TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)]
        result = split_nodes_delimiter(input_nodes, "**", TextType.TEXT)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_italic(self):
        """Test splitting nodes with italic delimiter (_)"""
        input_nodes = [TextNode("This is _italic text_ here", TextType.TEXT)]
        result = split_nodes_delimiter(input_nodes, "_", TextType.TEXT)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_code(self):
        """Test splitting nodes with code delimiter (`)"""
        input_nodes = [TextNode("Use `print()` function to display", TextType.TEXT)]
        result = split_nodes_delimiter(input_nodes, "`", TextType.TEXT)
        expected = [
            TextNode("Use ", TextType.TEXT),
            TextNode("print()", TextType.CODE),
            TextNode(" function to display", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_multiple_delimiters(self):
        """Test splitting with multiple delimited sections"""
        input_nodes = [TextNode("**bold1** and **bold2** text", TextType.TEXT)]
        result = split_nodes_delimiter(input_nodes, "**", TextType.TEXT)
        expected = [
            TextNode("bold1", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold2", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_unmatched_raises_exception(self):
        """Test that unmatched delimiters raise an exception"""
        input_nodes = [TextNode("This has **unmatched bold", TextType.TEXT)]
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter(input_nodes, "**", TextType.TEXT)
        self.assertIn("Unmatched delimiter", str(context.exception))


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text_node_to_html_node_text(self):
        """Test converting TEXT type TextNode to HTML"""
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_node_to_html_node_bold(self):
        """Test converting BOLD type TextNode to HTML"""
        node = TextNode("bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "bold text")

    def test_text_node_to_html_node_italic(self):
        """Test converting ITALIC type TextNode to HTML"""
        node = TextNode("italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "italic text")

    def test_text_node_to_html_node_code(self):
        """Test converting CODE type TextNode to HTML"""
        node = TextNode("print('hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello')")

    def test_text_node_to_html_node_link(self):
        """Test converting LINK type TextNode to HTML"""
        node = TextNode("click here", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "click here")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_text_node_to_html_node_image(self):
        """Test converting IMAGE type TextNode to HTML"""
        node = TextNode("alt text", TextType.IMAGE, "https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://example.com/image.png", "alt": "alt text"})


if __name__ == "__main__":
    unittest.main()

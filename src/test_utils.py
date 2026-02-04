from utils import text_node_to_html_node, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
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

class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        """Test extracting markdown images from text"""
        text = "Here is an image ![alt text](https://example.com/image.png) in the text."
        from utils import extract_markdown_images
        result = extract_markdown_images(text)
        expected = [("alt text", "https://example.com/image.png")]
        self.assertEqual(result, expected)
    
    def test_extract_markdown_images_multiple(self):
        """Test extracting multiple markdown images from text"""
        text = "Image one ![first](https://example.com/first.png) and image two ![second](https://example.com/second.png)."
        from utils import extract_markdown_images
        result = extract_markdown_images(text)
        expected = [("first", "https://example.com/first.png"), ("second", "https://example.com/second.png")]
        self.assertEqual(result, expected)
    
    def test_extract_markdown_images_none(self):
        """Test extracting markdown images when there are none"""
        text = "This text has no images."
        from utils import extract_markdown_images
        result = extract_markdown_images(text)
        expected = []
        self.assertEqual(result, expected)

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        """Test extracting markdown links from text"""
        text = "Here is a link [example](https://example.com) in the text."
        from utils import extract_markdown_links
        result = extract_markdown_links(text)
        expected = [("example", "https://example.com")]
        self.assertEqual(result, expected)
    
    def test_extract_markdown_links_multiple(self):
        """Test extracting multiple markdown links from text"""
        text = "Link one [first](https://example.com/first) and link two [second](https://example.com/second)."
        from utils import extract_markdown_links
        result = extract_markdown_links(text)
        expected = [("first", "https://example.com/first"), ("second", "https://example.com/second")]
        self.assertEqual(result, expected)
    
    def test_extract_markdown_links_none(self):
        """Test extracting markdown links when there are none"""
        text = "This text has no links."
        from utils import extract_markdown_links
        result = extract_markdown_links(text)
        expected = []
        self.assertEqual(result, expected)

class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_images_no_images(self):
        node = TextNode(
            "This is text without any images.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text without any images.", TextType.TEXT),
            ],
            new_nodes,
        )

class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://example.com) and another [second link](https://example.org)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://example.org"),
            ],
            new_nodes,
        )
    
    def test_split_links_no_links(self):
        node = TextNode(
            "This is text without any links.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text without any links.", TextType.TEXT),
            ],
            new_nodes,
        )

class TestTextToTextNodes(unittest.TestCase):
    def test_split_all_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
        )

    def test_text_to_textnodes_bold_only(self):
        """Test conversion of markdown with only bold text"""
        text = "This is **bold text** here"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold text", TextType.BOLD),
                TextNode(" here", TextType.TEXT),
            ],
            new_nodes
        )

    def test_text_to_textnodes_multiple_formats(self):
        """Test conversion of markdown with mixed formatting (bold, italic, code)"""
        text = "This is **bold**, _italic_, and `code` text"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(", ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(", and ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text", TextType.TEXT),
            ],
            new_nodes
        )

    def test_text_to_textnodes_image_and_link(self):
        """Test conversion of markdown with images and links"""
        text = "Check out ![python](https://example.com/python.png) and [click here](https://example.com)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("Check out ", TextType.TEXT),
                TextNode("python", TextType.IMAGE, "https://example.com/python.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("click here", TextType.LINK, "https://example.com"),
            ],
            new_nodes
        )

    def test_text_to_textnodes_plain_text_only(self):
        """Test conversion of plain text with no markdown formatting"""
        text = "This is just plain text with no formatting"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is just plain text with no formatting", TextType.TEXT),
            ],
            new_nodes
        )

if __name__ == "__main__":
    unittest.main()

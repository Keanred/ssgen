from enum import Enum

class TextType(Enum):
    """Enumeration of inline text formatting types in markdown.
    
    Values:
        TEXT: Plain unformatted text
        BOLD: Bold text (**text**)
        ITALIC: Italic text (_text_ or *text*)
        CODE: Inline code (`text`)
        LINK: Hyperlink ([text](url))
        IMAGE: Image (!text[](url))
    """
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    """Represents an inline text node with formatting information.
    
    TextNodes are used to represent runs of text with a specific type/formatting
    before they are converted to HTML nodes.
    
    Attributes:
        text (str): The actual text content.
        text_type (TextType): The type of formatting applied to this text.
        url (str | None): URL for links and images (optional).
    """

    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        """Initialize a TextNode.
        
        Args:
            text: The text content.
            text_type: The TextType enum indicating the text's formatting.
            url: URL for links/images (optional, required for LINK and IMAGE types).
        """
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: object) -> bool:
        """Check equality between two TextNode instances.
        
        Args:
            other: Object to compare with.
            
        Returns:
            bool: True if both nodes have identical text, type, and url.
        """
        if not isinstance(other, TextNode):
            return False
        return (self.text == other.text and
                self.text_type == other.text_type and
                self.url == other.url)
    
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
        
class HTMLNode:
    """Base class for HTML nodes in the document tree.
    
    Attributes:
        tag (str | None): The HTML tag name (e.g., 'div', 'p', 'a').
        value (str | None): The text content of the node.
        children (list[HTMLNode] | None): Child nodes for parent elements.
        props (dict[str, str | None] | None): HTML attributes as a dictionary.
    """
    
    def __init__(self, tag: str | None = None, value: str | None = None, 
                 children: list['HTMLNode'] | None = None, 
                 props: dict[str, str | None] | None = None) -> None:
        """Initialize an HTMLNode.
        
        Args:
            tag: HTML tag name (optional).
            value: Text content (optional).
            children: List of child HTMLNode objects (optional).
            props: Dictionary of HTML attributes (optional).
        """
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        """Convert the node to an HTML string.
        
        Returns:
            str: HTML representation of the node.
            
        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses should implement this method")
    
    def props_to_html(self) -> str:
        """Convert the node's properties to an HTML attribute string.
        
        Returns:
            str: A string of HTML attributes in the format ' key="value" ...'.
                 Returns empty string if no properties are set.
        """
        if self.props is None:
            return ""
        props_str = ""
        for prop in self.props:
            props_str += f' {prop}="{self.props[prop]}"'
        return props_str
    
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
        
class LeafNode(HTMLNode):
    """A leaf node representing an HTML element with no children.
    
    Leaf nodes are terminal nodes in the document tree that contain only text content.
    Examples: <b>, <i>, <span>, <a>, <img>, etc.
    Tag can be None for raw text nodes.
    
    Attributes:
        tag (str | None): The HTML tag name, or None for plain text.
        value (str): The text content of the leaf.
        props (dict[str, str | None] | None): HTML attributes (optional).
    """
    
    def __init__(self, tag: str | None, value: str, props: dict[str, str | None] | None = None) -> None:
        """Initialize a LeafNode.
        
        Args:
            tag: HTML tag name (required for most cases, None for plain text).
            value: Text content (required).
            props: Dictionary of HTML attributes (optional).
        """
        super().__init__(tag, value, None, props)
    
    def to_html(self) -> str:
        """Convert the leaf node to an HTML string.
        
        Returns:
            str: HTML representation. If tag is None, returns just the value.
                 Otherwise returns <tag>value</tag>.
                 
        Raises:
            ValueError: If value is None.
        """
        if self.value is None:
            raise ValueError("LeafNode must have a value to convert to HTML")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self) -> str:
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"

class ParentNode(HTMLNode):
    """A parent node representing an HTML element with children.
    
    Parent nodes can contain other HTML nodes as children.
    Examples: <div>, <p>, <ul>, <ol>, etc.
    
    Attributes:
        tag (str): The HTML tag name.
        children (list[HTMLNode]): List of child nodes.
        props (dict[str, str | None] | None): HTML attributes (optional).
    """
    
    def __init__(self, tag: str, children: list[HTMLNode], 
                 props: dict[str, str | None] | None = None) -> None:
        """Initialize a ParentNode.
        
        Args:
            tag: HTML tag name (required).
            children: List of child HTMLNode objects (required).
            props: Dictionary of HTML attributes (optional).
        """
        super().__init__(tag, None, children, props)
    
    def to_html(self) -> str:
        """Convert the parent node and its children to an HTML string.
        
        Returns:
            str: HTML representation in the form <tag>children</tag>.
            
        Raises:
            ValueError: If tag or children is None.
        """
        if self.tag is None:
            raise ValueError("ParentNode must have a tag to convert to HTML")
        if self.children is None:
            raise ValueError("ParentNode must have children to convert to HTML")
        child_tags = ""
        for child in self.children:
            child_tags += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{child_tags}</{self.tag}>"
    
    def __repr__(self) -> str:
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
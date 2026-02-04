from textnode import TextNode, TextType

def main():
    text_node = TextNode("Hello, World!", TextType.BOLD, "http://example.com")
    print(text_node)

if __name__ == "__main__":
    main()
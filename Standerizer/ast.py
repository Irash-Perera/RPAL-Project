class AST:
    def __init__(self, root = None):
        self.root = root

    def set_root(self, root):
        self.root = root

    def get_root(self):
        return self.root

    def standardize(self):
        # Check if the root node is already standardized
        if not self.root.is_standardized:
            # If not, call the standardize method on the root node
            self.root.standardize()

    def pre_order_traverse(self, node, i):
        # Print the node's data with indentation based on the level
        print("." * i + str(node.get_data()))
        # Traverse through each child node recursively
        for child in node.children:
            self.pre_order_traverse(child, i + 1)

    def print_ast(self):
        # Start the pre-order traversal from the root node with initial indentation level 0
        self.pre_order_traverse(self.get_root(), 0)

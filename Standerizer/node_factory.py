
class NodeFactory:
    def __init__(self):
        pass

    @staticmethod
    def get_node(data, depth):
        node = Node()
        node.set_data(data)
        node.set_depth(depth)
        node.children = []
        return node

    @staticmethod
    def get_node_with_parent(data, depth, parent, children, is_standardized):
        node = Node()
        node.set_data(data)
        node.set_depth(depth)
        node.set_parent(parent)
        node.children = children
        node.is_standardized = is_standardized
        return node

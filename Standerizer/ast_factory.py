from Standerizer.node import NodeFactory
from .ast import AST

class ASTFactory:
    def __init__(self):
        pass

    def get_abstract_syntax_tree(self, data):
        root = NodeFactory.get_node(data[0], 0)
        previous_node = root
        current_depth = 0

        for s in data[1:]:
            i = 0  # index of word
            d = 0  # depth of node

            while s[i] == '.':
                d += 1
                i += 1

            current_node = NodeFactory.get_node(s[i:], d)

            if current_depth < d:
                previous_node.children.append(current_node)
                current_node.set_parent(previous_node)
            else:
                while previous_node.get_depth() != d:
                    previous_node = previous_node.get_parent()
                previous_node.get_parent().children.append(current_node)
                current_node.set_parent(previous_node.get_parent())

            previous_node = current_node
            current_depth = d

        return AST(root)

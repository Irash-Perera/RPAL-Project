from Standarizing_AST.AST_node import ASTNode
from enum import Enum
class ASTNodeType(Enum):
    DELTA = "DELTA"

class Delta(ASTNode):
    def __init__(self):
        super().__init__()
        self.bound_vars = []
        self.linked_env = None
        self.body = []
        self.index = 0
        self.set_type(ASTNodeType.DELTA)

    def accept(self, node_copier):
        return node_copier.copy(self)

    def get_value(self):
        return "[lambda closure: {}: {}]".format(self.bound_vars[0], self.index)

    def get_bound_vars(self):
        return self.bound_vars

    def add_bound_var(self, bound_var):
        self.bound_vars.append(bound_var)

    def set_bound_vars(self, bound_vars):
        self.bound_vars = bound_vars

    def get_body(self):
        return self.body

    def set_body(self, body):
        self.body = body

    def get_index(self):
        return self.index

    def set_index(self, index):
        self.index = index

    def get_linked_env(self):
        return self.linked_env

    def set_linked_env(self, linked_env):
        self.linked_env = linked_env

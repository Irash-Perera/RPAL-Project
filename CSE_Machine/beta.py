from Standarizing_AST.AST_node import ASTNode
from enum import Enum

class ASTNodeType(Enum):
    BETA = "BETA"

class Beta(ASTNode):
    def __init__(self):
        super().__init__()
        self.then_body = []
        self.else_body = []
        self.set_type(ASTNodeType.BETA)

    def accept(self, node_copier):
        return node_copier.copy(self)

    def get_then_body(self):
        return self.then_body

    def get_else_body(self):
        return self.else_body

    def set_then_body(self, then_body):
        self.then_body = then_body

    def set_else_body(self, else_body):
        self.else_body = else_body

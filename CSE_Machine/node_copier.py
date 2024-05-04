from CSE_Machine.beta import Beta
from CSE_Machine.delta import Delta
from Standarizing_AST.AST_node import ASTNode


class NodeCopier:
    def copy(self, node):
        copy = ASTNode()
        if node.child is not None:
            copy.child = self.copy(node.child)
        if node.sibling is not None:
            copy.sibling = self.copy(node.sibling)
        copy.type = node.type
        copy.value = node.value
        copy.source_line_number = node.source_line_number
        return copy

    def copy_beta(self, beta):
        copy = Beta()
        if beta.child is not None:
            copy.child = self.copy(beta.child)
        if beta.sibling is not None:
            copy.sibling = self.copy(beta.sibling)
        copy.type = beta.type
        copy.value = beta.value
        copy.source_line_number = beta.source_line_number

        then_body_copy = [then_body_element.accept(self) for then_body_element in beta.then_body]
        copy.then_body = then_body_copy

        else_body_copy = [else_body_element.accept(self) for else_body_element in beta.else_body]
        copy.else_body = else_body_copy

        return copy

    def copy_eta(self, eta):
        copy = Eta()
        if eta.child is not None:
            copy.child = self.copy(eta.child)
        if eta.sibling is not None:
            copy.sibling = self.copy(eta.sibling)
        copy.type = eta.type
        copy.value = eta.value
        copy.source_line_number = eta.source_line_number

        copy.delta = eta.delta.accept(self)

        return copy

    def copy_delta(self, delta):
        copy = Delta()
        if delta.child is not None:
            copy.child = self.copy(delta.child)
        if delta.sibling is not None:
            copy.sibling = self.copy(delta.sibling)
        copy.type = delta.type
        copy.value = delta.value
        copy.index = delta.index
        copy.source_line_number = delta.source_line_number

        body_copy = [body_element.accept(self) for body_element in delta.body]
        copy.body = body_copy

        bound_vars_copy = delta.bound_vars.copy()
        copy.bound_vars = bound_vars_copy

        copy.linked_env = delta.linked_env

        return copy

    def copy_tuple(self, tuple):
        copy = Tuple()
        if tuple.child is not None:
            copy.child = self.copy(tuple.child)
        if tuple.sibling is not None:
            copy.sibling = self.copy(tuple.sibling)
        copy.type = tuple.type
        copy.value = tuple.value
        copy.source_line_number = tuple.source_line_number
        return copy

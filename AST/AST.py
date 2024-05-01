from AST_node_type import ASTNodeType
from AST_node import ASTNode
from AST_node import StandardizeException


class AST:
    def __init__(self, node):
        self.root = node
        self.pending_delta_body_queue = []
        self.standardized = False
        self.current_delta = None
        self.root_delta = None
        self.delta_index = 0

    def print(self):
        self.pre_order_print(self.root, "")

    def pre_order_print(self, node, print_prefix):
        if not node:
            return
        self.print_ast_node_details(node, print_prefix)
        self.pre_order_print(node.get_child(), print_prefix + ".")
        self.pre_order_print(node.get_sibling(), print_prefix)

    def print_ast_node_details(self, node, print_prefix):
        if node.get_type() == ASTNodeType.IDENTIFIER or node.get_type() == ASTNodeType.INTEGER:
            print(print_prefix + node.get_type().get_print_name(), node.get_value())
        elif node.get_type() == ASTNodeType.STRING:
            print(print_prefix + node.get_type().get_print_name(), node.get_value())
        else:
            print(print_prefix + node.get_type().get_print_name())

    def standardize(self):
        self.standardize_node(self.root)
        self.standardized = True

    def standardize_node(self, node):
        if not node:
            return
        if node.get_child():
            child_node = node.get_child()
            while child_node:
                self.standardize_node(child_node)
                child_node = child_node.get_sibling()

        # All children standardized, now standardize this node
        node_type = node.get_type()
        if node_type == ASTNodeType.LET:
            # Standardize LET node
            equal_node = node.get_child()
            if equal_node.get_type() != ASTNodeType.EQUAL:
                raise StandardizeException("LET/WHERE: left child is not EQUAL")  # Safety
            e = equal_node.get_child().get_sibling()
            equal_node.get_child().set_sibling(equal_node.get_sibling())
            equal_node.set_sibling(e)
            equal_node.set_type(ASTNodeType.LAMBDA)
            node.set_type(ASTNodeType.GAMMA)
        elif node_type == ASTNodeType.WHERE:
            # Standardize WHERE node
            equal_node = node.get_child().get_sibling()
            node.get_child().set_sibling(None)
            equal_node.set_sibling(node.get_child())
            node.set_child(equal_node)
            node.set_type(ASTNodeType.LET)
            self.standardize_node(node)
        elif node_type == ASTNodeType.FCNFORM:
            # Standardize FCNFORM node
            child_sibling = node.get_child().get_sibling()
            node.get_child().set_sibling(self.construct_lambda_chain(child_sibling))
            node.set_type(ASTNodeType.EQUAL)
        elif node_type == ASTNodeType.AT:
            # Standardize AT node
            e1 = node.get_child()
            n = e1.get_sibling()
            e2 = n.get_sibling()
            gamma_node = ASTNode()
            gamma_node.set_type(ASTNodeType.GAMMA)
            gamma_node.set_child(n)
            n.set_sibling(e1)
            e1.set_sibling(None)
            gamma_node.set_sibling(e2)
            node.set_child(gamma_node)
            node.set_type(ASTNodeType.GAMMA)
        elif node_type == ASTNodeType.WITHIN:
            # Standardize WITHIN node
            if node.get_child().get_type() != ASTNodeType.EQUAL or node.get_child().get_sibling().get_type() != ASTNodeType.EQUAL:
                raise StandardizeException("WITHIN: one of the children is not EQUAL")  # Safety
            x1 = node.get_child().get_child()
            e1 = x1.get_sibling()
            x2 = node.get_child().get_sibling().get_child()
            e2 = x2.get_sibling()
            lambda_node = ASTNode()
            lambda_node.set_type(ASTNodeType.LAMBDA)
            x1.set_sibling(e2)
            lambda_node.set_child(x1)
            lambda_node.set_sibling(e1)
            gamma_node = ASTNode()
            gamma_node.set_type(ASTNodeType.GAMMA)
            gamma_node.set_child(lambda_node)
            x2.set_sibling(gamma_node)
            node.set_child(x2)
            node.set_type(ASTNodeType.EQUAL)
        elif node_type == ASTNodeType.SIMULTDEF:
            # Standardize SIMULTDEF node
            comma_node = ASTNode()
            comma_node.set_type(ASTNodeType.COMMA)
            tau_node = ASTNode()
            tau_node.set_type(ASTNodeType.TAU)
            child_node = node.get_child()
            while child_node:
                self.populate_comma_and_tau_node(child_node, comma_node, tau_node)
                child_node = child_node.get_sibling()
            comma_node.set_sibling(tau_node)
            node.set_child(comma_node)
            node.set_type(ASTNodeType.EQUAL)
        elif node_type == ASTNodeType.REC:
            # Standardize REC node
            child_node = node.get_child()
            if child_node.get_type() != ASTNodeType.EQUAL:
                raise StandardizeException("REC: child is not EQUAL")  # Safety
            x = child_node.get_child()
            lambda_node = ASTNode()
            lambda_node.set_type(ASTNodeType.LAMBDA)
            lambda_node.set_child(x)  # x is already attached to e
            y_star_node = ASTNode()
            y_star_node.set_type(ASTNodeType.YSTAR)
            y_star_node.set_sibling(lambda_node)
            gamma_node = ASTNode()
            gamma_node.set_type(ASTNodeType.GAMMA)
            gamma_node.set_child(y_star_node)
            x_with_sibling_gamma = ASTNode()
            x_with_sibling_gamma.set_child(x.get_child())
            x_with_sibling_gamma.set_sibling(gamma_node)
            x_with_sibling_gamma.set_type(x.get_type())
            x_with_sibling_gamma.set_value(x.get_value())
            node.set_child(x_with_sibling_gamma)
            node.set_type(ASTNodeType.EQUAL)
        elif node_type == ASTNodeType.LAMBDA:
            # Standardize LAMBDA node
            child_sibling = node.get_child().get_sibling()
            node.get_child().set_sibling(self.construct_lambda_chain(child_sibling))

    def populate_comma_and_tau_node(self, equal_node, comma_node, tau_node):
        if equal_node.get_type() != ASTNodeType.EQUAL:
            raise StandardizeException("SIMULTDEF: one of the children is not EQUAL")  # Safety
        x = equal_node.get_child()
        e = x.get_sibling()
        self.set_child(comma_node, x)
        self.set_child(tau_node, e)

    def set_child(self, parent_node, child_node):
        if not parent_node.get_child():
            parent_node.set_child(child_node)
        else:
            last_sibling = parent_node.get_child()
            while last_sibling.get_sibling():
                last_sibling = last_sibling.get_sibling()
            last_sibling.set_sibling(child_node)
        child_node.set_sibling(None)

    def construct_lambda_chain(self, node):
        if not node.get_sibling():
            return node
        lambda_node = ASTNode()
        lambda_node.set_type(ASTNodeType.LAMBDA)
        lambda_node.set_child(node)
        if node.get_sibling().get_sibling():
            node.set_sibling(self.construct_lambda_chain(node.get_sibling()))
        return lambda_node

    def create_deltas(self):
        self.pending_delta_body_queue = []
        self.delta_index = 0
        self.current_delta = self.create_delta(self.root)
        self.process_pending_delta_stack()
        return self.root_delta

    def create_delta(self, start_body_node):
        # Create delta's body later
        pending_delta = PendingDeltaBody()
        pending_delta.start_node = start_body_node
        pending_delta.body = []
        self.pending_delta_body_queue.append(pending_delta)

        d = Delta()
        d.set_body(pending_delta.body)
        d.set_index(self.delta_index)
        self.current_delta = d

        if start_body_node == self.root:
            self.root_delta = self.current_delta

        return d

    def process_pending_delta_stack(self):
        while self.pending_delta_body_queue:
            pending_delta_body = self.pending_delta_body_queue.pop()
            self.build_delta_body(pending_delta_body.start_node, pending_delta_body.body)

    def build_delta_body(self, node, body):
        if node.get_type() == ASTNodeType.LAMBDA:
            # Create a new delta
            d = self.create_delta(node.get_child().get_sibling())  # New delta's body starts at the right child of the lambda
            if node.get_child().get_type() == ASTNodeType.COMMA:  # The left child of the lambda is the bound variable
                comma_node = node.get_child()
                child_node = comma_node.get_child()
                while child_node:
                    d.add_bound_vars(child_node.get_value())
                    child_node = child_node.get_sibling()
            else:
                d.add_bound_vars(node.get_child().get_value())
            body.append(d)  # Add this new delta to the existing delta's body
            return
        elif node.get_type() == ASTNodeType.CONDITIONAL:
            # To enable programming order evaluation, traverse the children in reverse order so the condition leads
            # cond -> then else becomes then else Beta cond
            condition_node = node.get_child()
            then_node = condition_node.get_sibling()
            else_node = then_node.get_sibling()

            # Add a Beta node
            beta_node = Beta()

            self.build_delta_body(then_node, beta_node.get_then_body())
            self.build_delta_body(else_node, beta_node.get_else_body())

            body.append(beta_node)

            self.build_delta_body(condition_node, body)
            return

        # Pre-order walk
        body.append(node)
        child_node = node.get_child()
        while child_node:
            self.build_delta_body(child_node, body)
            child_node = child_node.get_sibling()

    def is_standardized(self):
        return self.standardized

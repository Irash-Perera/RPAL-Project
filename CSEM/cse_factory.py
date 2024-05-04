from .nodes import *
from .csemachine import CSEMachine

class CSEMachineFactory:
    def __init__(self):
        self.e0 = E(0)
        self.i = 1
        self.j = 0

    def get_symbol(self, node):
        data = node.get_data()
        if data in ("not", "neg"):
            return Uop(data)
        elif data in ("+", "-", "*", "/", "**", "&", "or", "eq", "ne", "ls", "le", "gr", "ge", "aug"):
            return Bop(data)
        elif data == "gamma":
            return Gamma()
        elif data == "tau":
            return Tau(len(node.get_children()))
        elif data == "<Y*>":
            return Ystar()
        else:
            if data.startswith("<IDENTIFIER:"):
                return Id(data[12:-1])
            elif data.startswith("<INTEGER:"):
                return Int(data[9:-1])
            elif data.startswith("<STRING:"):
                return Str(data[9:-2])
            elif data.startswith("<nil"):
                return Tup()
            elif data.startswith("<true>"):
                return Bool("true")
            elif data.startswith("<false>"):
                return Bool("false")
            elif data.startswith("<dummy>"):
                return Dummy()
            else:
                print("Err node:", data)
                return Err()

    def get_b(self, node):
        b = B()
        b.symbols = self.get_pre_order_traverse(node)
        return b

    def get_lambda(self, node):
        lambda_expr = Lambda(self.i)
        self.i += 1
        lambda_expr.set_delta(self.get_delta(node.get_children()[1]))
        if node.get_children()[0].get_data() == ",":
            for identifier in node.get_children()[0].get_children():
                lambda_expr.identifiers.append(Id(identifier.get_data()[4:-1]))
        else:
            lambda_expr.identifiers.append(Id(node.get_children()[0].get_data()[4:-1]))
        return lambda_expr

    def get_pre_order_traverse(self, node):
        symbols = []
        if node.get_data() == "lambda":
            symbols.append(self.get_lambda(node))
        elif node.get_data() == "->":
            symbols.append(self.get_delta(node.get_children()[1]))
            symbols.append(self.get_delta(node.get_children()[2]))
            symbols.append(Beta())
            symbols.append(self.get_b(node.get_children()[0]))
        else:
            symbols.append(self.get_symbol(node))
            for child in node.get_children():
                symbols.extend(self.get_pre_order_traverse(child))
        return symbols

    def get_delta(self, node):
        delta = Delta(self.j)
        self.j += 1
        delta.symbols = self.get_pre_order_traverse(node)
        return delta

    def get_control(self, ast):
        control = [self.e0, self.get_delta(ast.get_root())]
        return control

    def get_stack(self):
        return [self.e0]

    def get_environment(self):
        return [self.e0]

    def get_cse_machine(self, ast):
        control = self.get_control(ast)
        stack = self.get_stack()
        environment = self.get_environment()
        return CSEMachine(control, stack, environment)

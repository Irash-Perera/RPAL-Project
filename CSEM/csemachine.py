from .nodes import *

class CSEMachine:
    def __init__(self, control, stack, environment):
        self.control = control
        self.stack = stack
        self.environment = environment

    def execute(self):
        current_environment = self.environment[0]
        j = 1
        while self.control:
            current_symbol = self.control.pop()
            if isinstance(current_symbol, Id):
                self.stack.insert(0, current_environment.lookup(current_symbol))
            elif isinstance(current_symbol, Lambda):
                current_symbol.set_environment(current_environment.get_index())
                self.stack.insert(0, current_symbol)
            elif isinstance(current_symbol, Gamma):
                next_symbol = self.stack.pop(0)
                if isinstance(next_symbol, Lambda):
                    lambda_expr = next_symbol
                    e = E(j)
                    if len(lambda_expr.identifiers) == 1:
                        e.values[lambda_expr.identifiers[0]] = self.stack.pop(0)
                    else:
                        tup = self.stack.pop(0)
                        for i, id in enumerate(lambda_expr.identifiers):
                            e.values[id] = tup.symbols[i]
                    for env in self.environment:
                        if env.get_index() == lambda_expr.get_environment():
                            e.set_parent(env)
                    current_environment = e
                    self.control.append(e)
                    self.control.append(lambda_expr.get_delta())
                    self.stack.insert(0, e)
                    self.environment.append(e)
                elif isinstance(next_symbol, Tup):
                    tup = next_symbol
                    i = int(self.stack.pop(0).get_data())
                    self.stack.insert(0, tup.symbols[i - 1])
                elif isinstance(next_symbol, Ystar):
                    lambda_expr = self.stack.pop(0)
                    eta = Eta()
                    eta.set_index(lambda_expr.get_index())
                    eta.set_environment(lambda_expr.get_environment())
                    eta.set_identifier(lambda_expr.identifiers[0])
                    eta.set_lambda(lambda_expr)
                    self.stack.insert(0, eta)
                elif isinstance(next_symbol, Eta):
                    eta = next_symbol
                    lambda_expr = eta.get_lambda()
                    self.control.append(Gamma())
                    self.control.append(Gamma())
                    self.stack.insert(0, eta)
                    self.stack.insert(0, lambda_expr)
                else:
                    if next_symbol.get_data() == "Print":
                        pass
                    elif next_symbol.get_data() == "Stem":
                        s = self.stack.pop(0)
                        s.set_data(s.get_data()[0])
                        self.stack.insert(0, s)
                    elif next_symbol.get_data() == "Stern":
                        s = self.stack.pop(0)
                        s.set_data(s.get_data()[1:])
                        self.stack.insert(0, s)
                    elif next_symbol.get_data() == "Conc":
                        s1 = self.stack.pop(0)
                        s2 = self.stack.pop(0)
                        s1.set_data(s1.get_data() + s2.get_data())
                        self.stack.insert(0, s1)
                    elif next_symbol.get_data() == "Order":
                        tup = self.stack.pop(0)
                        n = Int(str(len(tup.symbols)))
                        self.stack.insert(0, n)
                    elif next_symbol.get_data() == "Isinteger":
                        if isinstance(self.stack[0], Int):
                            self.stack.insert(0, Bool("true"))
                        else:
                            self.stack.insert(0, Bool("false"))
                        self.stack.pop(1)
                    # Implement other built-in functions similarly
            elif isinstance(current_symbol, E):
                self.stack.pop(1)
                self.environment[current_symbol.get_index()].set_is_removed(True)
                y = len(self.environment)
                while y > 0:
                    if not self.environment[y - 1].get_is_removed():
                        current_environment = self.environment[y - 1]
                        break
                    else:
                        y -= 1
            elif isinstance(current_symbol, Rator):
                if isinstance(current_symbol, Uop):
                    rator = current_symbol
                    rand = self.stack.pop(0)
                    self.stack.insert(0, self.apply_unary_operation(rator, rand))
                if isinstance(current_symbol, Bop):
                    rator = current_symbol
                    rand1 = self.stack.pop(0)
                    rand2 = self.stack.pop(0)
                    self.stack.insert(0, self.apply_binary_operation(rator, rand1, rand2))
            elif isinstance(current_symbol, Beta):
                if bool(self.stack[0].get_data()):
                    self.control.pop()
                else:
                    self.control.pop(-2)
                self.stack.pop(0)
            elif isinstance(current_symbol, Tau):
                tau = current_symbol
                tup = Tup()
                for _ in range(tau.get_n()):
                    tup.symbols.append(self.stack.pop(0))
                self.stack.insert(0, tup)
            elif isinstance(current_symbol, Delta):
                self.control.extend(current_symbol.symbols)
            elif isinstance(current_symbol, B):
                self.control.extend(current_symbol.symbols)
            else:
                self.stack.insert(0, current_symbol)

    def print_control(self):
        print("Control: ", end="")
        for symbol in self.control:
            print(symbol.get_data(), end="")
            if isinstance(symbol, (Lambda, Delta, E, Eta)):
                print(symbol.get_index(), end="")
            print(",", end="")
        print()

    def print_stack(self):
        print("Stack: ", end="")
        for symbol in self.stack:
            print(symbol.get_data(), end="")
            if isinstance(symbol, (Lambda, Delta, E, Eta)):
                print(symbol.get_index(), end="")
            print(",", end="")
        print()

    def print_environment(self):
        for symbol in self.environment:
            print(f"e{symbol.get_index()} --> ", end="")
            if symbol.get_index() != 0:
                print(f"e{symbol.get_parent().get_index()}")
            else:
                print()

    def apply_unary_operation(self, rator, rand):
        if rator.get_data() == "neg":
            val = int(rand.get_data())
            return Int(str(-1 * val))
        elif rator.get_data() == "not":
            val = bool(rand.get_data())
            return Bool(str(not val))
        else:
            return Err()

    def apply_binary_operation(self, rator, rand1, rand2):
        if rator.get_data() == "+":
            val1 = int(rand1.get_data())
            val2 = int(rand2.get_data())
            return Int(str(val1 + val2))
        # Implement other binary operations similarly

    def get_tuple_value(self, tup):
        temp = "("
        for symbol in tup.symbols:
            if isinstance(symbol, Tup):
                temp += self.get_tuple_value(symbol) + ", "
            else:
                temp += symbol.get_data() + ", "
        temp = temp[:-2] + ")"
        return temp

    def get_answer(self):
        self.execute()
        if isinstance(self.stack[0], Tup):
            return str(sum(int(symbol.get_data()) for symbol in self.stack[0].symbols))
        return self.stack[0].get_data()

class Symbol:
    def __init__(self, data):
        self.data = data

    def set_data(self, data):
        self.data = data

    def get_data(self):
        return self.data
    
class Rand(Symbol):
    def __init__(self, data):
        super().__init__(data)

    def get_data(self):
        return super().get_data()

class Rator(Symbol):
    def __init__(self, data):
        super().__init__(data)

class B(Symbol):
    def __init__(self):
        super().__init__("b")
        self.symbols = []

class Beta(Symbol):
    def __init__(self):
        super().__init__("beta")
        
class Bool(Rand):
    def __init__(self, data):
        super().__init__(data)

class Bop(Rator):
    def __init__(self, data):
        super().__init__(data)
        
class Delta(Symbol):
    def __init__(self, i):
        super().__init__("delta")
        self.index = i
        self.symbols = []

    def set_index(self, i):
        self.index = i

    def get_index(self):
        return self.index

class Dummy(Rand):
    def __init__(self):
        super().__init__("dummy")

class E(Symbol):
    def __init__(self, i):
        super().__init__("e")
        self.index = i
        self.parent = None
        self.is_removed = False
        self.values = {}

    def set_parent(self, e):
        self.parent = e

    def get_parent(self):
        return self.parent

    def set_index(self, i):
        self.index = i

    def get_index(self):
        return self.index

    def set_is_removed(self, is_removed):
        self.is_removed = is_removed

    def get_is_removed(self):
        return self.is_removed

    def lookup(self, id):
        for key in self.values:
            if key.get_data() == id.get_data():
                return self.values[key]
        if self.parent is not None:
            return self.parent.lookup(id)
        else:
            return Symbol(id.get_data())

class Err(Symbol):
    def __init__(self):
        super().__init__("")

class Eta(Symbol):
    def __init__(self):
        super().__init__("eta")
        self.index = None
        self.environment = None
        self.identifier = None
        self.lambda_ = None

    def set_index(self, i):
        self.index = i

    def get_index(self):
        return self.index

    def set_environment(self, e):
        self.environment = e

    def get_environment(self):
        return self.environment

    def set_identifier(self, identifier):
        self.identifier = identifier

    def set_lambda(self, lambda_):
        self.lambda_ = lambda_

    def get_lambda(self):
        return self.lambda_

class Gamma(Symbol):
    def __init__(self):
        super().__init__("gamma")

class Id(Rand):
    def __init__(self, data):
        super().__init__(data)
    
    def get_data(self):
        return super().get_data()

class Int(Rand):
    def __init__(self, data):
        super().__init__(data)

class Lambda(Symbol):
    def __init__(self, i):
        super().__init__("lambda")
        self.index = i
        self.environment = None
        self.identifiers = []
        self.delta = None

    def set_environment(self, n):
        self.environment = n

    def get_environment(self):
        return self.environment

    def set_delta(self, delta):
        self.delta = delta

    def get_delta(self):
        return self.delta
    def get_index(self):
        return self.index

class Str(Rand):
    def __init__(self, data):
        super().__init__(data)


class Tau(Symbol):
    def __init__(self, n):
        super().__init__("tau")
        self.set_n(n)

    def set_n(self, n):
        self.n = n

    def get_n(self):
        return self.n

class Tup(Rand):
    def __init__(self):
        super().__init__("tup")
        self.symbols = []


class Uop(Rator):
    def __init__(self, data):
        super().__init__(data)

class Ystar(Symbol):
    def __init__(self):
        super().__init__("<Y*>")




class ASTNode:
    def __init__(self):
        self.type = None
        self.value = None
        self.child = None
        self.sibling = None
        self.source_line_number = 0

    def get_name(self):
        return self.type.name()

    def get_type(self):
        return self.type

    def set_type(self, type):
        self.type = type

    def get_child(self):
        return self.child

    def set_child(self, child):
        self.child = child

    def get_sibling(self):
        return self.sibling

    def set_sibling(self, sibling):
        self.sibling = sibling

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    def accept(self, node_copier):
        return node_copier.copy(self)

    def get_source_line_number(self):
        return self.source_line_number

    def set_source_line_number(self, source_line_number):
        self.source_line_number = source_line_number

class StandardizeException(Exception):
    def __init__(self, message):
        super().__init__(message)
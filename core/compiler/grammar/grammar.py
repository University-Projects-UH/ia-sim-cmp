class Symbol:
    
    def __init__(self, name):
        self.name = name

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.__str__()


class NonTerminal(Symbol):

    def __init__(self, name):
        super().__init__(name)

        

class Terminal(Symbol):

    def __init__(self, name):
        super().__init__(name)
        

class Production:

    def __init__(self, left, right) -> None:
        self.right = right
        self.left = left


class Epsilon(Symbol):

    def __init__(self):
        super().__init__("e")


class End(Symbol):

    def __init__(self):
        super().__init__("$")
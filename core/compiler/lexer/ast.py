from .automaton.utils import union_automatas, concat_automatas, closure_automaton
from .automaton.automaton import Automaton
from .automaton.dfa import DFA

class Node:
    def evaluate(self):
        raise NotImplementedError()

class AtomicNode(Node):
    def __init__(self, lex):
        self.lex = lex

    def __str__(self) -> str:
        return "AtomicNode(" + str(self.lex +")")

class UnaryNode(Node):
    def __init__(self, node):
        self.node = node

    def evaluate(self):
        value = self.node.evaluate()
        return self.operate(value)

    def __str__(self) -> str:
        return "UnaryNode(" + str(self.node) + ")"

    @staticmethod
    def operate(value):
        raise NotImplementedError()

class BinaryNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self):
        lvalue = self.left.evaluate()
        rvalue = self.right.evaluate()
        return self.operate(lvalue, rvalue)

    @staticmethod
    def operate(lvalue, rvalue):
        raise NotImplementedError()

    def __str__(self) -> str:
        return "BinaryNode(" + str(self.left) + ", " + str(self.right) + ")"

EPSILON = 'ε'

class EpsilonNode(AtomicNode):
    def evaluate(self):
        return Automaton(1, 0, [0], [])

    def __str__(self) -> str:
        return "ε"

class SymbolNode(AtomicNode):
    def evaluate(self):
        s = self.lex
        return Automaton(2, 0, [1], [(0, s, [1])])

    def __str__(self) -> str:
        return "SymbolNode(" + str(self.lex +")" + str(type(self.lex)))

class ClosureNode(UnaryNode):
    @staticmethod
    def operate(value):
        return closure_automaton(value)
    
    def __str__(self) -> str:
        return "ClosureNode(" + str(self.node) + ")"

class UnionNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return union_automatas(lvalue, rvalue)

    def __str__(self) -> str:
        return "UniocNode(" + str(self.left) + ", " + str(self.right) + ")"

class ConcatNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return concat_automatas(lvalue, rvalue)

    def __str__(self) -> str:
        return "ConcatNode(" + str(self.left) + ", " + str(self.right) + ")"

from mimetypes import init

class Node():
    pass

class ProgramNode():

    def __init__(self, statements):
        self.statements = statements


class StatementNode(Node):
    pass

class ExpressionNode(Node):
    pass


class UnaryNode(ExpressionNode):

    def __init__(self, expression):
        self.expression = expression


class AtomicNode(ExpressionNode):

    def __init__(self, lex):
        self.lex = lex


class BinaryNode(ExpressionNode):

    def __init__(self, left, right) -> None:

        self.right = right
        self.left = left


class BotDeclaration(StatementNode):

    def __init__(self, id, params):

        self.id = id
        self.params = params


class GridBotDeclarationNode(BotDeclaration):

    def __init__(self, id, params):
        super().__init__(id, params)


class RebalanceBotDeclarationNode(BotDeclaration):

    def __init__(self, id, params):
        super().__init__(id, params)


class SmartBotDeclarationNode(BotDeclaration):

    def __init__(self, id, params):
        super().__init__(id, params)


class AssetDeclarationNode(StatementNode):

    def __init__(self, id, asset):

        self.id = id
        self.asset = asset


class IntDeclarationNode(StatementNode):

    def __init__(self, id, expression):

        self.id = id
        self.expression = expression


class FloatDeclarationNode(StatementNode):

    def __init__(self, id, expression):

        self.id = id
        self.expression = expression


class BoolDeclarationNode(StatementNode):

    def __init__(self, id, boolean):

        self.id = id
        self.boolean = boolean


class DateDeclarationNode(StatementNode):

    def __init__(self, id, date):

        self.id = id
        self.date = date


class StringDeclarationNode(StatementNode):

    def __init__(self, id, string):

        self.id = id
        self.string = string


class ArrayDeclarationNode(StatementNode):

    def __init__(self, id, elements):

        self.id = id
        self.elements = elements

class ArrayNode(Node):

    def __init__(self, elements):
        self.elements = elements


class ReAssignNode(StatementNode):

    def __init__(self, id, value):

        self.id = id
        self.value = value


class NegateBooleanNode(UnaryNode):

    def __init__(self, node):
        super().__init__(node)


class AndNode(BinaryNode):

    def __init__(self, left, right):
        super().__init__(left, right)


class OrNode(BinaryNode):

    def __init__(self, left, right):
        super().__init__(left, right)


class ParenthesisNode(UnaryNode):

    def __init__(self, node):
        super().__init__(node)


class EqualNode(BinaryNode):

    def __init__(self, left, right):
        super().__init__(left, right)

class NotEqualNode(BinaryNode):

    def __init__(self, left, right):
        super().__init__(left, right)

class GreatEqNode(BinaryNode):

    def __init__(self, left, right):
        super().__init__(left, right)

class LessEqNode(BinaryNode):

    def __init__(self, left, right):
        super().__init__(left, right)


class LessNode(BinaryNode):

    def __init__(self, left, right):
        super().__init__(left, right)


class GreatNode(BinaryNode):

    def __init__(self, left, right):
        super().__init__(left, right)


class PrintNode(StatementNode):

    def __init__(self, elem):
        self.elem = elem


class FuncCallNode(AtomicNode):

    def __init__(self, id, params):

        super().__init__(id)
        self.params = params


class PlusNode(BinaryNode):

    def __init__(self, right, left) -> None:
        super().__init__(right, left)


class MinusNode(BinaryNode):

    def __init__(self, right, left) -> None:
        super().__init__(right, left)


class MulNode(BinaryNode):

    def __init__(self, right, left) -> None:
        super().__init__(right, left)


class DivNode(BinaryNode):

    def __init__(self, right, left) -> None:
        super().__init__(right, left)


class IntNode(AtomicNode):

    def __init__(self, lex, neg=False):

        super().__init__(lex)
        self.neg = neg


class FloatNode(AtomicNode):

    def __init__(self, lex, neg=False):

        super().__init__(lex)
        self.neg = neg


class BoolNode(AtomicNode):

    def __init__(self, lex):
        super().__init__(lex)


class DateNode(AtomicNode):

    def __init__(self, lex):
        super().__init__(lex)


class VariableNode(AtomicNode):

    def __init__(self, lex):
        super().__init__(lex)


class StringNode(AtomicNode):

    def __init__(self, lex):
        super().__init__(lex)

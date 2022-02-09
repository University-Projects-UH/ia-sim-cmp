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

    def __init__(self, right, left) -> None:

        self.right = right
        self.left = left


class BotDeclaration(StatementNode):

    def __init__(self, id, params):

        self.id = id
        self.params = params


class GridBotDeclaration(BotDeclaration):

    def __init__(self, id, params):
        super().__init__(id, params)


class RebalanceBotDeclaration(BotDeclaration):

    def __init__(self, id, params):
        super().__init__(id, params)


class SmartBotDeclaration(BotDeclaration):

    def __init__(self, id, params):
        super().__init__(id, params)


class AssetDeclaration(StatementNode):

    def __init__(self, id, asset):

        self.id = id
        self.asset = asset


class AssetsDeclaration(StatementNode):

    def __init__(self, id, assets):

        self.id = id
        self.assets = assets


class IntDeclaration(StatementNode):

    def __init__(self, id, expression):

        self.id = id
        self.expression = expression


class FloatDeclaration(StatementNode):

    def __init__(self, id, expression):

        self.id = id
        self.expression = expression


class BoolDeclaration(StatementNode):

    def __init__(self, id, boolean):

        self.id = id
        self.boolean = boolean


class PortfolioDeclaration(StatementNode):

    def __init__(self, id, params):
        
        self.id = id
        self.params = params


class NegateBooleanNode(UnaryNode):

    def __init__(self, node):
        super().__init__(node)


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

    def __init__(self, lex):
        super().__init__(lex)


class FloatNode(AtomicNode):

    def __init__(self, lex):
        super().__init__(lex)


class BoolNode(AtomicNode):

    def __init__(self, lex):
        super().__init__(lex)


class VariableNode(AtomicNode):

    def __init__(self, lex):
        super().__init__(lex)


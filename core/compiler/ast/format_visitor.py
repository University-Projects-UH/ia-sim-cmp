from . import visitor as visitor
from .ast import *

class FormatVisitor(object):
    @visitor.on('node')
    def visit(self, node, tabs):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ProgramNode'
        statements = '\n'.join(self.visit(child, tabs + 1) for child in node.statements)
        return f'{ans}\n{statements}'

    @visitor.when(BotDeclaration)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__BotDeclarationNode: {node.id}'
        return f'{ans}'

    @visitor.when(GridBotDeclarationNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__GridBotDeclarationNode: {node.id}'
        params = '\n'.join(self.visit(param, tabs + 1) for param in node.params)
        return f'{ans}\n{params}'

    @visitor.when(RebalanceBotDeclarationNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__RebalanceBotDeclarationNode: {node.id}'
        params = '\n'.join(self.visit(param, tabs + 1) for param in node.params)
        return f'{ans}\n{params}'

    @visitor.when(SmartBotDeclarationNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__SmarteBotDeclarationNode: {node.id}'
        params = '\n'.join(self.visit(param, tabs + 1) for param in node.params)
        return f'{ans}\n{params}'

    @visitor.when(AssetDeclarationNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__AssetDeclarationNode: {node.id} = {node.asset}'
        return f'{ans}'

    @visitor.when(IntDeclarationNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ IntDeclarationNode: {node.id}'
        exp = self.visit(node.expression, tabs + 1)
        return f'{ans}\n{exp}'

    @visitor.when(FloatDeclarationNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ FloatDeclarationNode: {node.id}'
        exp = self.visit(node.expression, tabs + 1)
        return f'{ans}\n{exp}'

    @visitor.when(BoolDeclarationNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ BoolDeclarationNode: {node.id}'
        boolean = self.visit(node.boolean, tabs + 1)
        return f'{ans}\n{boolean}'

    @visitor.when(StringDeclarationNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ StringDeclarationNode: {node.id}'
        string = self.visit(node.string, tabs + 1)
        return f'{ans}\n{string}'

    @visitor.when(ArrayDeclarationNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ ArrayDeclarationNode: {node.id}'
        params = self.visit(node.elements, tabs + 1)
        return f'{ans}\n{params}'

    @visitor.when(ArrayNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ ArrayNode'
        elements = '\n'.join(self.visit(elem, tabs + 1) for elem in node.elements)
        return f'{ans}\n{elements}'

    @visitor.when(ReAssignNode)
    def visit(self, node, tabs=0):
        #ans = '\t' * tabs + f'\\__ ReAssignNode: id-{node.id} value-{node.value}'
        ans = '\t' * tabs + f'\\__ ReAssignNode: id-{node.id}'
        value = self.visit(node.value, tabs + 1)
        return f'{ans}\n{value}'

    @visitor.when(NegateBooleanNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ NegateBooleanNode'
        exp = self.visit(node.expression, tabs + 1)
        return f'{ans}\n{exp}'

    @visitor.when(AndNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ AndNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(OrNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ OrNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(ParenthesisNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ ParenthesisNode'
        exp = self.visit(node.expression, tabs + 1)
        return f'{ans}\n{exp}'

    @visitor.when(EqualNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__EqualNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(NotEqualNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__NotEqualNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(GreatEqNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__GreatEqNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(LessEqNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__LessEqNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(GreatNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__GreatNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(LessNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__LessNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(PrintNode)
    def visit(self, node, tabs=0):
        #ans = '\t' * tabs + f'\\__PrintNode ${node.elem}'
        ans = '\t' * tabs + f'\\__PrintNode'
        elem = self.visit(node.elem, tabs + 1)
        return f'{ans}\n{elem}'

    @visitor.when(FuncCallNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__FuncCallNode'
        params = '\n'.join(self.visit(param, tabs + 1) for param in node.params)
        return f'{ans}\n{params}'

    @visitor.when(PlusNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__PlusNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(MinusNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__MinusNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(MulNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__MulNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(DivNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__DivNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(IntNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__IntNode: {"-" if node.neg else ""}{node.lex}'
        return f'{ans}'

    @visitor.when(FloatNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__FloatNode: {"-" if node.neg else ""}{node.lex}'
        return f'{ans}'

    @visitor.when(BoolNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__BoolNode: {node.lex}'
        return f'{ans}'

    @visitor.when(StringNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__StringNode: {node.lex}'
        return f'{ans}'

    @visitor.when(VariableNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__VariableNode: {node.lex}'
        return f'{ans}'

    @visitor.when(DateDeclarationNode)
    def visit(self, node, tabs = 0):
        ans = '\t' * tabs + f'\\__ DateDeclarationNode: {node.id}'
        date = self.visit(node.date, tabs + 1)
        return f'{ans}\n{date}'

    @visitor.when(DateNode)
    def visit(self, node, tabs = 0):
        ans = '\t' * tabs + f'\\__DateNode: {node.lex}'
        return f'{ans}'
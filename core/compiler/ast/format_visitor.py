import .visitor as visitor
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
        return f'{ans}'

    @visitor.when(RebalanceBotDeclarationNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__RebalanceBotDeclarationNode: {node.id}'
        return f'{ans}'

    @visitor.when(SmartBotDeclarationNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__SmarteBotDeclarationNode: {node.id}'
        return f'{ans}'

    @visitor.when(AssetBotDeclarationNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__AssetDeclarationNode: {node.id}'
        return f'{ans}'

    @visitor.when(AssetsBotDeclarationNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__assetsdeclarationnode: {node.id}'
        return f'{ans}'

    @visitor.when(IntDeclarationNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ IntDeclarationNode: {node.id}'
        return ans

    @visitor.when(FloatDeclarationNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ FloatDeclarationNode: {node.id}'
        return ans

    @visitor.when(BoolDeclarationNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ BoolDeclarationNode: {node.id}'
        return ans

    @visitor.when(PortfolioDeclarationNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ PortfolioDeclarationNode: {node.id}'
        return ans

    @visitor.when(ReAssignNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ ReAssignNode: id-{node.id} value-{node.value}'
        return ans

    @visitor.when(NegateBooleanNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ NegateBooleanNode'
        return ans

    @visitor.when(ParenthesisNode)
    def visit(self, node, tabs=0):
        return '\t' * tabs + f'\\__ ParenthesisNode'

    @visitor.when(EqualNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__EqualNode'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(NoEqualNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__NoEqualNode'
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
        ans = '\t' * tabs + f'\\__PrintNode ${node.elem}'
        return ans

    @visitor.when(FuncCallNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__FuncCallNode'
        return ans

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
        ans = '\t' * tabs + f'\\__IntNode: {node.lex}'
        return f'{ans}'

    @visitor.when(FloatNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__FloatNode: {node.lex}'
        return f'{ans}'

    @visitor.when(BoolNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__BoolNode: {node.lex}'
        return f'{ans}'

    @visitor.when(VariableNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__VariableNode: {node.lex}'
        return f'{ans}'


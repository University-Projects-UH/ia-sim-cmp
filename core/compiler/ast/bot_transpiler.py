from . import visitor as visitor
from .ast import *

class BotTranspiler(object):
    @visitor.on('node')
    def visit(self, node, tabs):
        pass

    #terminar
    @visitor.when(ProgramNode)
    def visit(self, node, tabs=0):

        ans = "aqui viene los imports de los bots y demás\n\n"

        for stat in node.statements:
            ans += self.visit(stat) + '\n'
        
        # Aqui hay que crear un out.py y adentro copiarle ans
        

    @visitor.when(BotDeclaration)
    def visit(self, node, tabs=0):
        pass

    #falta
    @visitor.when(GridBotDeclarationNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__GridBotDeclarationNode: {node.id}'
        params = '\n'.join(self.visit(param, tabs + 1) for param in node.params)
        return f'{ans}\n{params}'

    #falta
    @visitor.when(RebalanceBotDeclarationNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__RebalanceBotDeclarationNode: {node.id}'
        params = '\n'.join(self.visit(param, tabs + 1) for param in node.params)
        return f'{ans}\n{params}'

    #falta
    @visitor.when(SmartBotDeclarationNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__SmarteBotDeclarationNode: {node.id}'
        params = '\n'.join(self.visit(param, tabs + 1) for param in node.params)
        return f'{ans}\n{params}'

    #falta
    @visitor.when(AssetDeclarationNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__AssetDeclarationNode: {node.id} = {node.asset}'
        return f'{ans}'

    #falta
    @visitor.when(AssetsDeclarationNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__AssetsDeclarationNode: {node.id}'
        assets = '\n'.join(self.visit(asset, tabs + 1) for asset in node.assets)
        return f'{ans}'

    @visitor.when(IntDeclarationNode)
    def visit(self, node, tabs=0):
        ans = str(node.id) + " = " + self.visit(node.expression)
        return ans

    @visitor.when(FloatDeclarationNode)
    def visit(self, node, tabs=0):
        ans = str(node.id) + " = " + self.visit(node.expression)
        return ans

    @visitor.when(BoolDeclarationNode)
    def visit(self, node, tabs=0):
        ans = str(node.id) + " = " + self.visit(node.boolean)
        return ans

    #falta
    @visitor.when(PortfolioDeclarationNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ PortfolioDeclarationNode: {node.id}'
        params = '\n'.join(self.visit(param, tabs + 1) for param in node.params)
        return f'{ans}\n{params}'

    @visitor.when(ReAssignNode)
    def visit(self, node, tabs=0):
        ans = str(node.id) + " = " + self.visit(node.value)
        return ans

    @visitor.when(NegateBooleanNode)
    def visit(self, node, tabs=0):
        ans = "not " + self.visit(node.expression)
        return ans

    @visitor.when(ParenthesisNode)
    def visit(self, node, tabs=0):
        ans = "( " + self.visit(node.expression) + " )"
        return ans

    @visitor.when(EqualNode)
    def visit(self, node, tabs=0):
        ans = self.visit(node.left) + " == " + self.visit(node.right)
        return ans

    @visitor.when(NotEqualNode)
    def visit(self, node, tabs=0):
        ans = self.visit(node.left) + " != " + self.visit(node.right)
        return ans

    @visitor.when(GreatEqNode)
    def visit(self, node, tabs=0):
        ans = self.visit(node.left) + " >= " + self.visit(node.right)
        return ans

    @visitor.when(LessEqNode)
    def visit(self, node, tabs=0):
        ans = self.visit(node.left) + " <= " + self.visit(node.right)
        return ans

    @visitor.when(GreatNode)
    def visit(self, node, tabs=0):
        ans = self.visit(node.left) + " > " + self.visit(node.right)
        return ans

    @visitor.when(LessNode)
    def visit(self, node, tabs=0):
        ans = self.visit(node.left) + " < " + self.visit(node.right)
        return ans

    @visitor.when(PrintNode)
    def visit(self, node, tabs=0):
        ans = "print( " + self.visit(node.elem) + " )"
        return ans

    @visitor.when(FuncCallNode)
    def visit(self, node, tabs=0):
        ans = self.visit(node.id) + "( "
        for param in node.params:
            ans += self.visit(param) + ", "
        ans += " )"
        return ans

    @visitor.when(PlusNode)
    def visit(self, node, tabs=0):
        ans = self.visit(node.left) + " + " + self.visit(node.right)
        return ans

    @visitor.when(MinusNode)
    def visit(self, node, tabs=0):
        ans = self.visit(node.left) + " - " + self.visit(node.right)
        return ans

    @visitor.when(MulNode)
    def visit(self, node, tabs=0):
        ans = self.visit(node.left) + " * " + self.visit(node.right)
        return ans

    @visitor.when(DivNode)
    def visit(self, node, tabs=0):
        ans = self.visit(node.left) + " / " + self.visit(node.right)
        return ans

    @visitor.when(IntNode)
    def visit(self, node, tabs=0):
        ans = str(node.lex)
        return ans

    @visitor.when(FloatNode)
    def visit(self, node, tabs=0):
        ans = str(node.lex)
        return ans

    @visitor.when(BoolNode)
    def visit(self, node, tabs=0):
        ans = str(node.lex)
        return ans

    @visitor.when(VariableNode)
    def visit(self, node, tabs=0):
        ans = str(node.lex)
        return ans


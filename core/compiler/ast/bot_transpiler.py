from . import visitor as visitor
from .ast import *

class BotTranspiler(object):
    @visitor.on('node')
    def visit(self, node, tabs):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, tabs=0):

        ans = "from core import GridBot, RebalanceBot, SmartBot\n"
        ans += "from core import Asset\n"
        ans += "from datetime import datetime\n"
        ans += "from core import PortfolioSdMin, PortfolioSharpeRatio\n\n"

        for stat in node.statements:
            print(self.visit(stat))
            ans += self.visit(stat) + '\n'

        f = open("code_transpiled.py", "w")
        f.write(ans)
        f.close()

    @visitor.when(GridBotDeclarationNode)
    def visit(self, node, tabs=0):
        ans = str(node.id) + " = " + "GridBot(" + ", ".join(self.visit(param) for param in node.params) + ")"
        return ans

    @visitor.when(RebalanceBotDeclarationNode)
    def visit(self, node, tabs=0):
        ans = str(node.id) + " = " + "RebalanceBot(" + ", ".join(self.visit(param) for param in node.params) + ")"
        return ans

    @visitor.when(SmartBotDeclarationNode)
    def visit(self, node, tabs=0):
        ans = str(node.id) + " = " + "SmartBot(" + ", ".join(self.visit(param) for param in node.params) + ")"
        return ans

    @visitor.when(AssetDeclarationNode)
    def visit(self, node, tabs=0):
        ans = str(node.id) + " = " + "Asset(" + node.asset + ")"
        return ans

    @visitor.when(AssetsDeclarationNode)
    def visit(self, node, tabs=0):
        ans = str(node.id) + " = " + "[" + ", ".join(self.visit(asset) for asset in node.assets) + "]"
        return ans

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

    @visitor.when(DateDeclarationNode)
    def visit(self, node, tabs=0):
        ans = str(node.id) + " = datetime.strptime(\"" + self.visit(node.date) + "\", \"%Y-%m-%d\")"
        return ans

    @visitor.when(PortfolioDeclarationNode)
    def visit(self, node, tabs=0):
        ans = str(node.id) + " = " + "[" + ", ".join(self.visit(param) for param in node.params) + "]"
        return ans

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

    @visitor.when(DateNode)
    def visit(self, node, tabs=0):
        ans = str(node.lex)
        return ans


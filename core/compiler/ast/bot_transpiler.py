from . import visitor as visitor
from .ast import *

parse_function = {
    "CreateAsset": lambda params: f"Asset({', '.join(params)})",
    "PortfolioMSR": lambda params: f"PortfolioSharpeRatio({', '.join(params)}).run()",
    "PortfolioSDMin": lambda params: f"PortfolioSdMin({', '.join(params)}).run()",
    "StartBot": lambda params: f"{params[0]}.start_bot({', '.join(params[1:])})",
    "GridBotOpt": lambda params: f"grid_bot_optimization({', '.join(params)})",
    "RebalanceBotOpt": lambda params: f"RebalanceBotOpt({', '.join(params)}).optimize()"
}

class BotTranspiler(object):
    @visitor.on('node')
    def visit(self, node, tabs):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, tabs=0):

        ans = "from core import GridBot, RebalanceBot, SmartBot\n"
        ans += "from core import Asset\n"
        ans += "from datetime import datetime\n"
        ans += "from core import PortfolioSdMin, PortfolioSharpeRatio\n"
        ans += "from core import grid_bot_optimization\n"
        ans += "from core import RebalanceBotOpt\n\n"

        for stat in node.statements:
            print(self.visit(stat))
            ans += self.visit(stat) + '\n'

        f = open("code_transpiled.py", "w")
        f.write(ans)
        f.close()

    @visitor.when(GridBotDeclarationNode)
    def visit(self, node, tabs=0):
        if(type(node.params).__name__ == "VariableNode"):
            ans = str(node.id) + " = " + str(node.params.lex)
        elif(type(node.params).__name__ == "FuncCallNode"):
            ans = str(node.id) + " = " + self.visit(node.params)
        else:
            ans = str(node.id) + " = " + "GridBot(" + ", ".join(self.visit(param) for param in node.params) + ")"
        return ans

    @visitor.when(RebalanceBotDeclarationNode)
    def visit(self, node, tabs=0):
        if(type(node.params).__name__ == "VariableNode"):
            ans = str(node.id) + " = " + str(node.params.lex)
        elif(type(node.params).__name__ == "FuncCallNode"):
            ans = str(node.id) + " = " + self.visit(node.params)
        else:
            ans = str(node.id) + " = " + "RebalanceBot(" + ", ".join(self.visit(param) for param in node.params) + ")"
        return ans

    @visitor.when(SmartBotDeclarationNode)
    def visit(self, node, tabs=0):
        if(type(node.params).__name__ == "VariableNode"):
            ans = str(node.id) + " = " + str(node.params.lex)
        else:
            ans = str(node.id) + " = " + "SmartBot(" + ", ".join(self.visit(param) for param in node.params) + ")"
        return ans

    @visitor.when(AssetDeclarationNode)
    def visit(self, node, tabs=0):
        ans = "Error declarando asset"
        if(type(node.asset).__name__ == "VariableNode"):
            ans = str(node.id) + " = " + str(node.asset.lex)
        elif(type(node.asset).__name__ == "FuncCallNode"):
            ans = str(node.id) + " = " + "Asset(" + ", ".join([self.visit(param) for param in node.asset.params]) + ")"
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
        ans = str(node.id) + " = " + self.visit(node.lex)
        return ans

    @visitor.when(StringDeclarationNode)
    def visit(self, node, tabs=0):
        ans = str(node.id) + " = " + self.visit(node.string)
        return ans

    @visitor.when(ArrayDeclarationNode)
    def visit(self, node, tabs=0):
        ans = str(node.id) + " = " + self.visit(node.elements)
        return ans

    @visitor.when(ArrayNode)
    def visit(self, node, tabs=0):
        ans = "[" + ", ".join(self.visit(elem) for elem in node.elements) + "]"
        return ans

    @visitor.when(ReAssignNode)
    def visit(self, node, tabs=0):
        ans = str(node.id) + " = " + self.visit(node.value)
        return ans

    @visitor.when(NegateBooleanNode)
    def visit(self, node, tabs=0):
        ans = "not " + self.visit(node.expression)
        return ans

    @visitor.when(AndNode)
    def visit(self, node, tabs=0):
        ans = self.visit(node.left) + " and " + self.visit(node.right)
        return ans

    @visitor.when(OrNode)
    def visit(self, node, tabs=0):
        ans = self.visit(node.left) + " or " + self.visit(node.right)
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
        ans = parse_function[node.lex]([self.visit(param) for param in node.params])
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
        ans = ("(-" if node.neg else "") + str(node.lex) + (")" if node.neg else "")
        return ans

    @visitor.when(FloatNode)
    def visit(self, node, tabs=0):
        ans = ("(-" if node.neg else "") + str(node.lex) + (")" if node.neg else "")
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
        ans = "datetime.strptime(\"" + node.lex + "\", \"%Y-%m-%d\")"
        return ans

    @visitor.when(StringNode)
    def visit(self, node, tabs=0):
        ans = str(node.lex)
        return ans


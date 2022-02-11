from . import visitor as visitor
from .ast import *

types_check = {
    "number": ["FloatNode", "IntNode", "FloatDeclarationNode", "IntDeclarationNode"],
    "int": ["IntNode", "IntDeclarationNode"],
    "float": ["FloatNode", "FloatDeclarationNode"],
    "list_asset": ["AssetsDeclarationNode"],
    "list_float": ["PortfolioDeclarationNode"],
    "asset": ["str", "AssetDeclarationNode"]
}

# list with the assets
assets_accepted = []

def check_param(param, _type, variables = {}):
    types_check_array = types_check[_type]
    param_type = type(param).__name__

    if(param_type == "VariableNode"):
        try:
            param = variables[param_type]
            param_type = type(param).__name__
        except KeyError:
            return f"Variable \"{param.lex}\" no declarada"

    if(_type.startswith("list")):
        list_type = _type[5:]
        if(list_type == "asset" or list_type == "float"):
            # The VariableNode already declared is AssetsDeclarationNode
            if(param_type in types_check_array):
                return None
            for elem in param:
                error = check_param(elem, list_type, variables)
                if(error is not None):
                    return error

        return None

    if(param_type in types_check_array):
        if(_type == "asset" and param_type == "str" and param not in assets_accepted):
            return f"El activo {param} no existe en nuestro registro"
        return None
    return "Tipo de variable incorrecto"


class SemanticChecker(object):
    @visitor.on('node')
    def visit(self, node, variables = {}):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, variables = {}):
        errors = []
        variables = {}
        for statement in node.statements:
            errors += self.visit(statement, variables)

    @visitor.when(GridBotDeclarationNode)
    def visit(self, node, variables = {}):
        if(len(node.params) != 7):
            return "Cantidad de parámetros distinto de lo esperado"
        types = ["number", "number", "number", "int", "number", "number", "list_asset"]
        cnt = 0
        for param in node.params:
            error = check_param(param, types[cnt], variables)
            if(error is not None):
                return error
            cnt += 1
        return None

    @visitor.when(RebalanceBotDeclarationNode)
    def visit(self, node, variables = {}):
        if(len(node.params) < 4 or len(node.params) > 6):
            return "Cantidad de parámetros distinto de lo esperado"
        types = ["number", "number", "number", "list_asset", "number", "list_float"]
        cnt = 0
        for param in node.params:
            error = check_param(param, types[cnt], variables)
            if(error is not None):
                return error
            cnt += 1
        return None

    @visitor.when(SmartBotDeclarationNode)
    def visit(self, node, variables = {}):
        if(len(node.params) != 4):
            return "Cantidad de parámetros distinto de lo esperado"
        types = ["number", "number", "number", "list_asset"]
        cnt = 0
        for param in node.params:
            error = check_param(param, types[cnt], variables)
            if(error is not None):
                return error
            cnt += 1
        return None

    @visitor.when(AssetDeclarationNode)
    def visit(self, node, variables = {}):
        return check_param(node.value, "asset", variables)

    @visitor.when(AssetsDeclarationNode)
    def visit(self, node, variables = {}):
        return check_param(node.assets, "list_asset", variables)

    @visitor.when(PortfolioDeclarationNode)
    def visit(self, node, variables = {}):
        return check_param(node.assets, "list_float", variables)

    @visitor.when(ReAssignNode)
    def visit(self, node, variables = {}):
        try:
            new_node = variables[node.id]
        except KeyError:
            return f"Variable {node.id} no declarada"

    @visitor.when(NegateBooleanNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ NegateBooleanNode'
        return ans

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

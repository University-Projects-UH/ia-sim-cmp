from . import visitor as visitor
from .ast import *
import re
from datetime import datetime

types_check = {
    "number": ["FloatNode", "IntNode"],
    "int": ["IntNode"],
    "float": ["FloatNode"],
    "string": ["StringNode"],
    "date": ["DateNode"],
    "boolean": ["BoolNode"],
    "array": ["ArrayNode"],
    "list_asset": ["AssetArray"],
    "list_float": ["FloatArray"],
    "asset": ["AssetNode"],
    "bot": ["GridBotDeclarationNode", "RebalanceBotDeclarationNode", "SmartBotDeclarationNode"]
}

map_nodes = {
    "IntDeclarationNode": "int",
    "DateDeclarationNode": "date",
    "StringDeclarationNode": "string",
    "FloatDeclarationNode": "float",
    "BoolDeclarationNode": "boolean",
    "ArrayDeclarationNode": "array",
}

defaultFunctionsReturn = {
    "PortfolioMSR": "FloatArray",
    "PortfolioSDMin": "FloatArray",
    "CreateAsset": "AssetNode",
    "StartBot": "None",
    "GridBotOpt": "GridBotDeclarationNode",
    "RebalanceBotOpt": "RebalanceBotDeclarationNode"
}

countFunctionsParams = {
    "PortfolioMSR": (2, 2),
    "PortfolioSDMin": (2, 2),
    "CreateAsset": (1, 1),
    "StartBot": (2, 2),
    "GridBotOpt": (1, 4),
    "RebalanceBotOpt": (1, 3)
}

defaultFunctionsParams = {
    "PortfolioMSR": ["date", "list_asset"],
    "PortfolioSDMin": ["date", "list_asset"],
    "CreateAsset": ["string"],
    "StartBot": ["bot", "boolean"],
    "GridBotOpt": ["list_asset", "number", "int", "int"],
    "RebalanceBotOpt": ["list_asset", "float", "number"]
}

class SemanticChecker(object):

    def __init__(self, assets_accepted):
        self.assets_accepted = assets_accepted

    def get_undeclared_error(self, id):
        return f"Variable '{id}' no declarada"

    def get_declared_twice_error(self, id):
        return f"La variable '{id}' ya ha sido declarada antes"

    def get_compare_type_error(self):
        return "No puedes comparar dos tipos diferentes"

    def get_compare_undefined_error(self, _type):
        return f"Comparación no soportada por el tipo {_type}"

    def get_operation_type_error(self):
        return "No puedes realizar una operación entre  dos tipos diferentes"

    def get_operation_undefined_error(self, _type):
        return f"Operación no soportada por el tipo {_type}"

    def get_assign_error(self):
        return "No puedes asignar un tipo diferente a otro"

    def get_param_error(self):
        return "El tipo de parámetro es incorrecto"

    def get_function_error(self, id):
        return f"El función '{id}' no existe"

    def get_different_params_len(self):
        return "Cantidad de parámetros distinto a lo esperado"

    def get_asset_undefined_error(self, lex):
        return f"El activo {lex} no existe"

    def check_func_call(self, node, variables):
        function_return_type = defaultFunctionsReturn[node.lex]
        function_params_types = defaultFunctionsParams[node.lex]
        count_params = countFunctionsParams[node.lex]

        if(len(node.params) < count_params[0] or len(node.params) > count_params[1]):
            return self.get_different_params_len(), None

        for i, param in enumerate(node.params):
            type_expected = function_params_types[i]
            error, _type = self.visit(param, variables)
            if(error is not None):
                return error
            if(_type not in types_check[type_expected]):
                return self.get_param_error(), None
            if(_type == "asset" and param.lex[1:-1] not in self.assets_accepted):
                return self.get_asset_undefined_error(param.lex), None

        return None, function_return_type

    def check_bot(self, node, types, params_expected, variables):
        bot_type = type(node).__name__
        params_type = type(node.params).__name__

        if(params_type == "VariableNode" or params_type == "FuncCallNode"):
            error, _type = self.visit(node.params, variables)
            if(error):
                return error, None
            if(_type != bot_type):
                return self.get_assign_error(), None
            variables[node.id] = bot_type
            return None, bot_type

        if(type(node.params).__name__ != "list"):
            return self.get_assign_error(), None

        if(len(node.params) not in params_expected):
            return self.get_different_params_len(), None

        for i, param in enumerate(node.params):
            error, _type = self.visit(param, variables)
            if(error is not None):
                return error, None
            if(_type not in types_check[types[i]]):
                return self.get_param_error(), None

        variables[node.id] = bot_type

        return None, bot_type

    def check_binary_node(self, node, variables, node_type = "compare"):
        left = node.left
        right = node.right

        error, left_type = self.visit(left, variables)
        if(error is not None):
            return error, None

        error, right_type = self.visit(right, variables)
        if(error is not None):
            return error, None

        if(left_type != right_type):
            if(node_type == "Compare"):
                return self.get_compare_type_error(), None
            else:
                return self.get_operation_type_error(), None

        if(node_type == "Compare"):
            types = ["IntNode", "FloatNode", "DateNode", "StringNode"]
            if(left_type not in types):
                return self.get_compare_undefined_error(left_type), None
            return None, "BoolNode"

        types = ["IntNode", "FloatNode"]
        if(left_type not in types):
            return self.get_operation_undefined_error(left_type), None
        return None, left_type


    @visitor.on('node')
    def visit(self, node, variables = {}):
        return None, None

    @visitor.when(ProgramNode)
    def visit(self, node, variables = {}):
        errors = []
        variables = {}
        for i, statement in enumerate(node.statements):
            error, _ = self.visit(statement, variables)
            if(error):
                errors += [(i + 1, error)]
        return errors

    @visitor.when(GridBotDeclarationNode)
    def visit(self, node, variables = {}):
        if(variables.__contains__(node.id)):
            return self.get_declared_twice_error(node.id), None
        types = ["string", "number", "number", "number", "int", "number", "number", "list_asset"]
        return self.check_bot(node, types, [8], variables)

    @visitor.when(RebalanceBotDeclarationNode)
    def visit(self, node, variables = {}):
        if(variables.__contains__(node.id)):
            return self.get_declared_twice_error(node.id), None
        types = ["string", "number", "number", "number", "list_asset", "number", "list_float"]
        return self.check_bot(node, types, [5, 6, 7], variables)

    @visitor.when(SmartBotDeclarationNode)
    def visit(self, node, variables = {}):
        if(variables.__contains__(node.id)):
            return self.get_declared_twice_error(node.id), None
        types = ["string", "number", "number", "number", "list_asset"]
        return self.check_bot(node, types, [5], variables)

    @visitor.when(AssetDeclarationNode)
    def visit(self, node, variables = {}):
        if(variables.__contains__(node.id)):
            return self.get_declared_twice_error(node.id), None

        if(type(node.asset).__name__ == "VariableNode"):
            error, _type = self.visit(node.asset, variables)
            if(error):
                return error, None
            if(_type != "AssetNode"):
                return self.get_assign_error(), None

            variables[node.id] = "AssetNode"
            return None, "AssetNode"

        error, _type = self.visit(node.asset, variables)
        if(error):
            return error, None
        if(_type != "AssetNode"):
            return self.get_assign_error(), None

        variables[node.id] = "AssetNode"

        return None, "AssetNode"


    @visitor.when(ArrayDeclarationNode)
    def visit(self, node, variables = {}):
        if(variables.__contains__(node.id)):
            return self.get_declared_twice_error(node.id), None

        if(type(node.elements).__name__ == "VariableNode"):
            error, _type = self.visit(node.elements, variables)
            if(error):
                return error, None
            if(re.search("Array", _type) is None):
                return self.get_assign_error(), None

            variables[node.id] = _type
            return None, _type

        error, _type = self.visit(node.elements, variables)

        if(error is not None):
            return error, None

        if(re.search("Array", _type) is None):
            return self.get_assign_error(), None

        variables[node.id] = _type
        return None, _type


    @visitor.when(ArrayNode)
    def visit(self, node, variables = {}):
        is_float = True
        is_asset = True
        for elem in node.elements:
            error, _type = self.visit(elem, variables)
            if(error is not None):
                return error, None
            if(_type != "FloatNode"):
                is_float = False
            if(_type != "AssetNode"):
                is_asset = False

        if(is_float is False and is_asset):
            return None, "AssetArray"
        if(is_asset is False and is_float):
            return None, "FloatArray"

        return None, "Array"


    @visitor.when(VariableNode)
    def visit(self, node, variables = {}):
        if(variables.__contains__(node.lex) == False):
            return self.get_undeclared_error(node.lex), None

        return None, variables[node.lex]

    @visitor.when(IntDeclarationNode)
    def visit(self, node, variables = {}):
        if(variables.__contains__(node.id)):
            return self.get_declared_twice_error(node.id), None

        if(type(node.expression).__name__ == "VariableNode"):
            error, _type = self.visit(node.expression, variables)
            if(error):
                return error, None
            if(_type != "IntNode"):
                return self.get_assign_error(), None

            variables[node.id] = "IntNode"
            return None, "IntNode"

        error, _type = self.visit(node.expression, variables)
        if(error is not None):
            return error, None
        if(_type != "IntNode"):
            return self.get_assign_error(), None

        variables[node.id] = "IntNode"
        return None, "IntNode"

    @visitor.when(FloatDeclarationNode)
    def visit(self, node, variables = {}):
        if(variables.__contains__(node.id)):
            return self.get_declared_twice_error(node.id), None

        if(type(node.expression).__name__ == "VariableNode"):
            error, _type = self.visit(node.expression, variables)
            if(error):
                return error, None
            if(_type != "FloatNode"):
                return self.get_assign_error(), None

            variables[node.id] = "FloatNode"
            return None, "FloatNode"

        error, _type = self.visit(node.expression, variables)
        if(error is not None):
            return error, None
        if(_type != "FloatNode"):
            return self.get_assign_error(), None

        variables[node.id] = "FloatNode"
        return None, "FloatNode"

    @visitor.when(BoolDeclarationNode)
    def visit(self, node, variables = {}):
        if(variables.__contains__(node.id)):
            return self.get_declared_twice_error(node.id), None

        if(type(node.boolean).__name__ == "VariableNode"):
            error, _type = self.visit(node.boolean, variables)
            if(error):
                return error, None
            if(_type != "BoolNode"):
                return self.get_assign_error(), None

            variables[node.id] = "BoolNode"
            return None, "BoolNode"

        error, _type = self.visit(node.boolean, variables)
        if(error is not None):
            return error, None
        if(_type != "BoolNode"):
            return self.get_assign_error(), None

        variables[node.id] = "BoolNode"
        return None, "BoolNode"


    @visitor.when(DateDeclarationNode)
    def visit(self, node, variables):
        if(variables.__contains__(node.id)):
            return self.get_declared_twice_error(node.id), None

        if(type(node.date).__name__ == "VariableNode"):
            error, _type = self.visit(node.date, variables)
            if(error):
                return error, None
            if(_type != "DateNode"):
                return self.get_assign_error(), None

            variables[node.id] = "DateNode"
            return None, "DateNode"

        error, _type = self.visit(node.date, variables)
        if(error is not None):
            return error, None
        if(_type != "DateNode"):
            return self.get_assign_error(), None

        variables[node.id] = "DateNode"
        return None, "DateNode"

    @visitor.when(StringDeclarationNode)
    def visit(self, node, variables = {}):
        if(variables.__contains__(node.id)):
            return self.get_declared_twice_error(node.id), None

        if(type(node.string).__name__ == "VariableNode"):
            error, _type = self.visit(node.string, variables)
            if(error):
                return error, None
            if(_type != "StringNode"):
                return self.get_assign_error(), None

            variables[node.id] = "StringNode"
            return None, "StringNode"

        error, _type = self.visit(node.string, variables)
        if(error is not None):
            return error, None
        if(_type != "StringNode"):
            return self.get_assign_error(), None

        variables[node.id] = "StringNode"
        return None, "StringNode"


    @visitor.when(ReAssignNode)
    def visit(self, node, variables = {}):
        if(variables.__contains__(node.id) == False):
            return self.get_undeclared_error(node.id), None

        error, _type = self.visit(node.value, variables)
        if(error is not None):
            return error, None
        if(_type != variables[node.id]):
            return self.get_assign_error(), None

        return None, "ReAssignNode"

    @visitor.when(FuncCallNode)
    def visit(self, node, variables = {}):
        if(node.lex in defaultFunctionsReturn.keys()):
            return self.check_func_call(node, variables)
        return self.get_function_error(node.lex), None

    @visitor.when(NegateBooleanNode)
    def visit(self, node, variables = {}):
        error, _type = self.visit(node.expression, variables)
        if(error is not None):
            return error, None
        if(_type != "BoolNode"):
           self.get_param_error(), None
        return None, "BoolNode"


    @visitor.when(AndNode)
    def visit(self, node, variables = {}):
        return self.check_binary_node(node, variables)

    @visitor.when(OrNode)
    def visit(self, node, variables = {}):
        return self.check_compare_node(node, variables)

    @visitor.when(ParenthesisNode)
    def visit(self, node, variables = {}):
        error, _type = self.visit(node.expression, variables)
        if(error is not None):
            return error, None
        return None, _type

    @visitor.when(EqualNode)
    def visit(self, node, variables = {}):
        return self.check_compare_node(node, variables)

    @visitor.when(GreatEqNode)
    def visit(self, node, variables = {}):
        return self.check_compare_node(node, variables)

    @visitor.when(LessEqNode)
    def visit(self, node, variables = {}):
        return self.check_compare_node(node, variables)

    @visitor.when(GreatNode)
    def visit(self, node, variables = {}):
        return self.check_compare_node(node, variables)

    @visitor.when(LessNode)
    def visit(self, node, variables = {}):
        return self.check_compare_node(node, variables)

    @visitor.when(PrintNode)
    def visit(self, node, variables = {}):
        error, _ = self.visit(node.elem, variables)
        if(error is not None):
            return error, None
        return None, None

    @visitor.when(PlusNode)
    def visit(self, node, variables = {}):
        return self.check_binary_node(node, variables, "Operation")

    @visitor.when(MinusNode)
    def visit(self, node, variables = {}):
        return self.check_binary_node(node, variables, "Operation")

    @visitor.when(MulNode)
    def visit(self, node, variables = {}):
        return self.check_binary_node(node, variables, "Operation")

    @visitor.when(DivNode)
    def visit(self, node, variables = {}):
        return self.check_binary_node(node, variables, "Operation")

    @visitor.when(IntNode)
    def visit(self, node, variables = {}):
        return None, "IntNode"

    @visitor.when(FloatNode)
    def visit(self, node, variables = {}):
        return None, "FloatNode"

    @visitor.when(BoolNode)
    def visit(self, node, variables = {}):
        return None, "BoolNode"

    @visitor.when(DateNode)
    def visit(self, node, variables = {}):
        try:
            datetime.strptime(node.lex, "%Y-%m-%d")
            return None, "DateNode"
        except ValueError:
            return "Formato de fecha incorrecto", "None"

    @visitor.when(StringNode)
    def visit(self, node, variables = {}):
        return None, "StringNode"


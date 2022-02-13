from . import visitor as visitor
from .ast import *

types_check = {
    "number": ["FloatNode", "IntNode", "FloatDeclarationNode", "IntDeclarationNode", \
               "DivNode", "MulNode", "MinusNode", "PlusNode"],
    "int": ["IntNode", "IntDeclarationNode", "DivNode", "MulNode", "MinusNode", \
            "PlusNode"],
    "float": ["FloatNode", "FloatDeclarationNode", "DivNode", "MulNode", "MinusNode", \
              "PlusNode"],
    "string": ["StringNode", "StringDeclarationNode"],
    "date": ["DateNode", "DateDeclarationNode"],
    "boolean": ["BoolNode", "GreatNode", "LessNode", "GreatEqNode", "LessEqNode", \
                "NotEqualNode", "EqualNode"],
    "array": ["ArrayDeclarationNode", "list"]
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
    "PortfolioMSR": "array_float",
    "PortfolioSDMin": "array_float",
    "CreateAsset": "asset"
}

defaultFunctionsParams = {
    "PortfolioMSR": ["list_asset", "date"],
    "PortfolioSDMin": ["list_asset", "date"],
    "CreateAsset": ["string"]
}

# list with the assets
assets_accepted = []

class SemanticChecker(object):

    def get_undeclared_error(self, id):
        return f"Variable '{id}' no declarada"

    def get_compare_error(self):
        return "No puedes comparar dos tipos diferentes"

    def get_assign_error(self):
        return "No puedes asignar un tipo diferente a otro"

    def get_param_error(self):
        return "El tipo de parámetro es incorrecto"

    def get_function_error(self, id):
        return f"El función '{id}' no existe"

    def get_different_params_len(self):
        return "Cantidad de parámetros distinto a lo esperado"

    def check_func_call(self, func_call_node, _type, variables):
        try:
            function_return_type = defaultFunctionsReturn[func_call_node.id]
            function_params_types = defaultFunctionsParams[func_call_node.id]

            if(len(function_params_types) != len(func_call_node.params)):
                return self.get_different_params_len()

            if(_type != function_return_type):
                return self.get_param_error()

            for i, param in enumerate(func_call_node.params):
                type_expected = function_params_types[i]
                error = self.check_param(param, type_expected, variables)
                if(error is not None):
                    return error

        except KeyError:
            return self.get_function_error(func_call_node.id)


    def check_param(self, param, _type, variables = {}):
        types_check_array = types_check[_type]
        param_type = type(param).__name__

        if(param_type == "VariableNode"):
            try:
                param = variables[param_type]
                param_type = type(param).__name__
            except KeyError:
                return self.get_undeclared_error(param.lex)

        if(param_type == "FuncCallNode"):
            return self.check_func_call(param, _type, variables)

        # check if the param should be a list
        if(_type.startswith("list")):
            list_type = _type[5:]
            if(list_type == "asset" or list_type == "float"):
                if(param_type != "ArrayDeclarationNode" and param_type != "list"):
                    return self.get_param_error()
                for elem in param:
                    error = self.check_param(elem, list_type, variables)
                    if(error is not None):
                        return error

            return None

        if(param_type in types_check_array):
            return None
        return self.get_param_error()

    def check_bot(self, node, types, params_expected, variables):
        bot_type = type(node).__name__
        params_type = type(node.params).__name__
        if(params_type == "VariableNode"):
            try:
                params_type = type(variables[node.params.lex])
            except KeyError:
                return self.get_undeclared_error(node.params.lex)
            if(params_type != bot_type):
                return self.get_assign_error()
            return None

        if(len(node.params) not in params_expected):
            return self.get_different_params_len()

        for i, param in enumerate(node.params):
            error = self.check_param(param, types[i], variables)
            if(error is not None):
                return error

        variables[node.id] = node

        return None

    def check_binary_node(self, node, variables = {}):
        left = node.left
        left_type = type(left).__name__
        if(left_type == "VariableNode"):
            try:
                left_type = type(variables[left.lex]).__name__
            except KeyError:
                return self.get_undeclared_error(left.lex)

        right = node.right
        right_type = type(right).__name__
        if(right_type == "VariableNode"):
            try:
                right_type = type(variables[right.lex]).__name__
            except KeyError:
                return self.get_undeclared_error(right.lex)

        if(left_type != right_type):
            return self.get_compare_error()

        error = self.visit(left)
        if(error is not None):
            return error

        return self.visit(right)

    @visitor.on('node')
    def visit(self, node, variables = {}):
        return None

    @visitor.when(ProgramNode)
    def visit(self, node, variables = {}):
        errors = []
        variables = {}
        for i, statement in enumerate(node.statements):
            error = self.visit(statement, variables)
            if(error):
                errors += [(i, error)]
        return errors

    @visitor.when(GridBotDeclarationNode)
    def visit(self, node, variables = {}):
        types = ["number", "number", "number", "int", "number", "number", "list_asset"]
        return self.check_bot(node, types, [7], variables)

    @visitor.when(RebalanceBotDeclarationNode)
    def visit(self, node, variables = {}):
        types = ["number", "number", "number", "list_asset", "number", "list_float"]
        return self.check_bot(node, types, [4, 5, 6], variables)

    @visitor.when(SmartBotDeclarationNode)
    def visit(self, node, variables = {}):
        types = ["number", "number", "number", "list_asset"]
        return self.check_bot(node, types, [4], variables)

    @visitor.when(AssetDeclarationNode)
    def visit(self, node, variables = {}):
        if(type(node.asset).__name__ == "VariableNode"):
            try:
                new_node = variables[node.asset.lex]
            except KeyError:
                return self.get_undeclared_error(node.asset.lex)
        if(type(new_node).__name__ == "FuncCallNode"):
            return self.get_assign_error()
        error = self.check_func_call(new_node, "asset", variables)
        if(error is None):
            variables[node.id] = new_node

    @visitor.when(ArrayDeclarationNode)
    def visit(self, node, variables = {}):
        new_node = node
        if(type(node.elements).__name__ == "VariableNode"):
            try:
                new_node = variables[node.elements.lex]
            except KeyError:
                return self.get_undeclared_error(node.elements.lex)
        if(type(new_node).__name__ != "ArrayDeclarationNode"):
            return self.get_assign_error()
        variables[node.id] = new_node
        return None

    @visitor.when(IntDeclarationNode)
    def visit(self, node, variables = {}):
        new_node = node
        if(type(node.expression).__name__ == "VariableNode"):
            try:
                new_node = variables[node.expression.lex]
            except KeyError:
                return self.get_undeclared_error(node.expression.lex)
        if(type(new_node).__name__ not in types_check["int"]):
            return self.get_assign_error()
        variables[node.id] = new_node
        return None

    @visitor.when(FloatDeclarationNode)
    def visit(self, node, variables = {}):
        new_node = node
        if(type(node.expression).__name__ == "VariableNode"):
            try:
                new_node = variables[node.expression.lex]
            except KeyError:
                return self.get_undeclared_error(node.expression.lex)
        if(type(new_node).__name__ not in types_check["float"]):
            return self.get_assign_error()
        variables[node.id] = new_node
        return None

    @visitor.when(BoolDeclarationNode)
    def visit(self, node, variables = {}):
        new_node = node
        if(type(node.boolean).__name__ == "VariableNode"):
            try:
                new_node = variables[node.boolean.lex]
            except KeyError:
                return self.get_undeclared_error(node.boolean.lex)
        if(type(new_node).__name__ not in types_check["boolean"]):
            return self.get_assign_error()
        variables[node.id] = new_node
        return None

    @visitor.when(StringDeclarationNode)
    def visit(self, node, variables = {}):
        new_node = node
        if(type(node.string).__name__ == "VariableNode"):
            try:
                new_node = variables[node.string.lex]
            except KeyError:
                return self.get_undeclared_error(node.string.lex)
        if(type(new_node).__name__ not in types_check["string"]):
            return self.get_assign_error()
        variables[node.id] = new_node
        return None

    @visitor.when(DateDeclarationNode)
    def visit(self, node, variables = {}):
        new_node = node
        if(type(node.date).__name__ == "VariableNode"):
            try:
                new_node = variables[node.date.lex]
            except KeyError:
                return self.get_undeclared_error(node.date.lex)
        if(type(new_node).__name__ not in types_check["date"]):
            return self.get_assign_error()
        variables[node.id] = new_node
        return None

    @visitor.when(ReAssignNode)
    def visit(self, node, variables = {}):
        node_type = None
        new_node = None
        try:
            new_node = variables[node.id]
            node_type = type(new_node).__name__
        except KeyError:
            return self.get_undeclared_error(node.id)

        new_value = node.value
        value_type = type(new_value).__name__

        if(value_type == "VariableNode"):
            try:
                new_value = variables[node.value.lex]
                value_type = type(new_value).__name__
            except KeyError:
                return self.get_undeclared_error(node.value.lex)

        if(value_type == "FuncCallNode"):
            if(node.value.id not in defaultFunctionsReturn.keys()):
                return self.get_function_error(node.value.id)
            value_type = defaultFunctionsReturn[node.value.id][:5]

        if(node_type not in map_nodes.keys()):
            return self.get_assign_error()
        type_mapped = map_nodes[node_type]
        if(value_type not in types_check[type_mapped]):
            return self.get_assign_error()
        variables[node.id] = new_node

        return None

    @visitor.when(FuncCallNode)
    def visit(self, node, variables = {}):
        if(node.id in defaultFunctionsReturn.keys()):
            return None
        return self.get_function_error(node.id)

    @visitor.when(NegateBooleanNode)
    def visit(self, node, variables = {}):
        return self.check_param(node.expression, "boolean", variables)

    @visitor.when(EqualNode)
    def visit(self, node, variables = {}):
        return self.check_binary_node(node, variables)

    @visitor.when(GreatEqNode)
    def visit(self, node, variables = {}):
        return self.check_binary_node(node, variables)

    @visitor.when(LessEqNode)
    def visit(self, node, variables = {}):
        return self.check_binary_node(node, variables)

    @visitor.when(GreatNode)
    def visit(self, node, variables = {}):
        return self.check_binary_node(node, variables)

    @visitor.when(LessNode)
    def visit(self, node, variables = {}):
        return self.check_binary_node(node, variables)

    @visitor.when(PrintNode)
    def visit(self, node, variables = {}):
        pass

    @visitor.when(PlusNode)
    def visit(self, node, variables = {}):
        return self.check_binary_node(node, variables)

    @visitor.when(MinusNode)
    def visit(self, node, variables = {}):
        return self.check_binary_node(node, variables)

    @visitor.when(MulNode)
    def visit(self, node, variables = {}):
        return self.check_binary_node(node, variables)

    @visitor.when(DivNode)
    def visit(self, node, variables = {}):
        return self.check_binary_node(node, variables)

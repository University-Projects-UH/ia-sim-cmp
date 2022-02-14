from core import Grammar, Production
from .ast.ast import DateNode, ProgramNode, GridBotDeclarationNode, RebalanceBotDeclarationNode, SmartBotDeclarationNode
from .ast.ast import AssetDeclarationNode
from .ast.ast import IntDeclarationNode, BoolDeclarationNode, FloatDeclarationNode, ReAssignNode, DateDeclarationNode
from .ast.ast import NegateBooleanNode, ParenthesisNode
from .ast.ast import EqualNode, NotEqualNode, GreatEqNode, GreatNode, LessEqNode, LessNode
from .ast.ast import PrintNode, FuncCallNode, ArrayNode
from .ast.ast import PlusNode, MinusNode, MulNode, DivNode
from .ast.ast import IntNode, FloatNode, BoolNode, VariableNode, StringNode
from .ast.ast import StringDeclarationNode, ArrayDeclarationNode

class BotGrammar:

    def __init__(self):
        self.grammar = self.build_grammar()
        

    def build_grammar(self):

        ###############################################
        #                   GRAMMAR
        ###############################################

        G = Grammar()


        ###############################################
        #                   NON TERMINALS   
        ###############################################

        program = G.add_non_terminal('<program>', True) # initial non terminal

        stat_list, stat = G.add_non_terminals('<stat_list> <stat>')

        grid_bot_declaration = G.add_non_terminal('<grid_bot_declaration>')
        rebalance_bot_declaration = G.add_non_terminal('<rebalance_bot_declaration>')
        smart_bot_declaration = G.add_non_terminal('<smart_bot_declaration>')

        asset_declaration = G.add_non_terminal('<asset_declaration>')

        int_decalaration = G.add_non_terminal('<int_declaration>')
        float_declaration = G.add_non_terminal('<float_declaration>')
        bool_declaration = G.add_non_terminal('<bool_declaration>')
        date_declaration = G.add_non_terminal('<date_declaration>')

        boolean = G.add_non_terminal('<boolean>')

        array = G.add_non_terminal('<array>')

        elem_list = G.add_non_terminal('<elem_list>')

        elem = G.add_non_terminal('<elem>')

        print_elem = G.add_non_terminal('<print_elem>')
        func_call = G.add_non_terminal('<func_call>')

        expression, term, factor, atom = G.add_non_terminals('<expression> <term> <factor> <atom>')

        portfolio_declaration = G.add_non_terminal('<portfolio_declaration>')

        asset_array_declaration = G.add_non_terminal('<asset_array_declaration>')

        re_assign = G.add_non_terminal('<re_assign>')

        string_declaration = G.add_non_terminal('<string_declaration>')

        array_declaration = G.add_non_terminal('<array_declaration>')


        ###############################################
        #               TERMINALS
        ###############################################

        semicolon, colon = G.add_terminals('; ,')
        intt, floatt, boolt = G.add_terminals('int float bool')
        grid_bot, rebalance_bot, smart_bot = G.add_terminals('grid_bot rebalance_bot smart_bot')
        asset = G.add_terminal('asset')
        negate, equal, not_equal, great_eq, less_eq, great, less = G.add_terminals('! ==  != >= <= > <')
        truet, falset = G.add_terminals('True False')
        assign = G.add_terminal('=')
        obracket, cbracket, opar, cpar = G.add_terminals('[ ] ( )')
        printt = G.add_terminal('print')
        plus, minus, div, mul = G.add_terminals('+ - / *')
        ID = G.add_terminal('id')
        int_number, float_number = G.add_terminals('int_number float_number')
        datet, date_type = G.add_terminals('date date_type')
        stringt = G.add_terminal('string')
        string_exp = G.add_terminal('string_exp')
        arrayt = G.add_terminal('array')


        ###############################################
        #               PRODUCTIONS
        ###############################################

        program %= stat_list, lambda h, s: ProgramNode(s[1])

        stat_list %= stat + semicolon, lambda h, s: [s[1]]
        stat_list %= stat + semicolon + stat_list, lambda h, s: [s[1]] + s[3]

        stat %= grid_bot_declaration, lambda h, s: s[1]
        stat %= rebalance_bot_declaration, lambda h, s: s[1]
        stat %= smart_bot_declaration, lambda h, s: s[1]
        stat %= asset_declaration, lambda h, s: s[1]
        stat %= int_decalaration, lambda h, s: s[1]
        stat %= float_declaration, lambda h, s: s[1]
        stat %= bool_declaration, lambda h, s: s[1]
        stat %= portfolio_declaration, lambda h, s: s[1]
        stat %= asset_array_declaration, lambda h, s: s[1]
        stat %= print_elem, lambda h, s: s[1]
        stat %= re_assign, lambda h, s: s[1]
        stat %= func_call, lambda h, s: s[1]
        stat %= date_declaration, lambda h, s: s[1]
        stat %= string_declaration, lambda h, s: s[1]
        stat %= array_declaration, lambda h, s: s[1]

        string_declaration %= stringt + ID + assign + string_exp, lambda h, s: StringDeclarationNode(s[2], StringNode(s[4]))
        string_declaration %= stringt + ID + assign + ID, lambda h, s: StringDeclarationNode(s[2], VariableNode(s[4]))

        grid_bot_declaration %= grid_bot + ID + assign + grid_bot + opar + elem_list + cpar, lambda h, s: GridBotDeclarationNode(s[2], s[6])
        grid_bot_declaration %= grid_bot + ID + assign + ID, lambda h, s: GridBotDeclarationNode(s[2], VariableNode(s[4]))

        rebalance_bot_declaration %= rebalance_bot + ID + assign + rebalance_bot + opar + elem_list + cpar, lambda h, s: RebalanceBotDeclarationNode(s[2], s[6])
        rebalance_bot_declaration %= rebalance_bot + ID + assign + ID, lambda h, s: RebalanceBotDeclarationNode(s[2], VariableNode(s[4]))

        smart_bot_declaration %= smart_bot + ID + assign + smart_bot + opar + elem_list + cpar, lambda h, s: SmartBotDeclarationNode(s[2], s[6])
        smart_bot_declaration %= smart_bot + ID + assign + ID, lambda h, s: SmartBotDeclarationNode(s[2], VariableNode(s[4]))

        asset_declaration %= asset + ID + assign + func_call, lambda h, s: AssetDeclarationNode(s[2], s[4])
        asset_declaration %= asset + ID + assign + ID, lambda h, s: AssetDeclarationNode(s[2], VariableNode(s[4]))

        int_decalaration %= intt + ID + assign + expression, lambda h, s: IntDeclarationNode(s[2], s[4])

        float_declaration %= floatt + ID + assign + expression, lambda h, s: FloatDeclarationNode(s[2], s[4])

        bool_declaration %= boolt + ID + assign + elem, lambda h, s: BoolDeclarationNode(s[2], s[4])

        date_declaration %= datet + ID + assign + expression, lambda h, s: DateDeclarationNode(s[2], s[4]) 

        array_declaration %= arrayt + ID + assign + array, lambda h, s: ArrayDeclarationNode(s[2], s[4])
        array_declaration %= arrayt + ID + assign + func_call, lambda h, s: ArrayDeclarationNode(s[2], s[4])
        array_declaration %= arrayt + ID + assign + ID, lambda h, s: ArrayDeclarationNode(s[2], VariableNode(s[4]))

        re_assign %= ID + assign + elem, lambda h, s: ReAssignNode(s[1], s[3])

        boolean %= opar + boolean + cpar, lambda h, s: s[2]
        boolean %= negate + boolean, lambda h, s: NegateBooleanNode(s[2])
        boolean %= expression + equal + expression, lambda h, s: EqualNode(s[1], s[3])
        boolean %= expression + not_equal + expression, lambda h, s: NotEqualNode(s[1], s[3])
        boolean %= expression + great_eq + expression, lambda h, s: GreatEqNode(s[1], s[3])
        boolean %= expression + less_eq + expression, lambda h, s: LessEqNode(s[1], s[3])
        boolean %= expression + less + expression, lambda h, s: LessNode(s[1], s[3])
        boolean %= expression + great + expression, lambda h, s: GreatNode(s[1], s[3])
        boolean %= truet, lambda h, s: BoolNode(s[1])
        boolean %= falset, lambda h, s: BoolNode(s[1])

        array %= obracket + elem_list + cbracket, lambda h, s: ArrayNode(s[2])

        elem_list %= elem, lambda h, s: [s[1]]
        elem_list %= elem + colon + elem_list, lambda h, s: [s[1]] + s[3]

        elem %= expression, lambda h, s: s[1]
        elem %= boolean, lambda h, s: s[1]
        elem %= array, lambda h, s: s[1]
        elem %= string_exp, lambda h, s: StringNode(s[1])

        print_elem %= printt + elem, lambda h, s: PrintNode(s[2])

        func_call %= ID + opar + elem_list + cpar, lambda h, s: FuncCallNode(s[1], s[3])

        expression %= expression + plus + term, lambda h, s: PlusNode(s[1], s[3])
        expression %= expression + minus + term, lambda h, s: MinusNode(s[1], s[3])
        expression %= term, lambda h, s: s[1]

        term %= term + mul + factor, lambda h, s: MulNode(s[1], s[3])
        term %= term + div + factor, lambda h, s: DivNode(s[1], s[3])
        term %= factor, lambda h, s: s[1]

        factor %= opar + expression + cpar, lambda h, s: s[2]
        factor %= atom, lambda h, s: s[1]

        atom %= int_number, lambda h, s: IntNode(s[1])
        atom %= float_number, lambda h, s: FloatNode(s[1])
        atom %= ID, lambda h, s: VariableNode(s[1])
        atom %= func_call, lambda h, s: s[1]
        atom %= date_type, lambda h, s: DateNode(s[1])

        return G

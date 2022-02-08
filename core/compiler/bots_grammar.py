from core import Grammar, Production

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

        boolean = G.add_non_terminal('<boolean>')

        array = G.add_non_terminal('<array>')

        elem_list = G.add_non_terminal('<elem_list>')

        elem = G.add_non_terminal('<elem>')

        print_elem = G.add_non_terminal('<print_elem>')
        func_call = G.add_non_terminal('<func_call>')

        expression, term, factor, atom = G.add_non_terminals('<expression> <term> <factor> <atom>')


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


        ###############################################
        #               PRODUCTIONS
        ###############################################

        program %= stat_list

        stat_list %= stat + semicolon
        stat_list %= stat + semicolon + stat_list

        stat %= grid_bot_declaration
        stat %= rebalance_bot_declaration
        stat %= smart_bot_declaration
        stat %= asset_declaration
        stat %= int_decalaration
        stat %= float_declaration
        stat %= bool_declaration

        grid_bot_declaration %= grid_bot + ID + elem_list

        rebalance_bot_declaration %= rebalance_bot + ID + elem_list

        smart_bot_declaration %= smart_bot + ID + elem_list

        asset_declaration %= asset + ID + ID

        int_decalaration %= intt + ID + assign + expression

        float_declaration %= floatt + ID + assign + expression

        bool_declaration %= boolt + ID + assign + boolean

        boolean %= opar + boolean + cpar
        boolean %= negate + boolean
        boolean %= expression + equal + expression
        boolean %= expression + not_equal + expression
        boolean %= expression + great_eq + expression
        boolean %= expression + less_eq + expression
        boolean %= expression + less + expression
        boolean %= expression + great + expression
        boolean %= truet
        boolean %= falset

        array %= obracket + elem_list + cbracket

        elem_list %= elem
        elem_list %= elem + colon + elem_list

        elem %= expression
        elem %= boolean
        elem %= array

        print_elem %= printt + elem

        func_call %= ID + opar + elem_list + cpar

        expression %= expression + plus + term
        expression %= expression + minus + term
        expression %= term

        term %= term + mul + factor
        term %= term + div + factor
        term %= factor

        factor %= opar + expression + cpar
        factor %= atom

        atom %= int_number
        atom %= float_number
        atom %= ID
        atom %= func_call

        return G

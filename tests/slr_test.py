from core import Grammar, Sentence, Production
from core.compiler.parser.slr1 import SLR1Parser
from core.compiler.parser.parser_shift_reduce import ShiftReduceParser
from pandas import DataFrame

def encode_value(value):
    try:
        action, tag = value
        if action == ShiftReduceParser.SHIFT:
            return 'S' + str(tag)
        elif action == ShiftReduceParser.REDUCE:
            return repr(tag)
        elif action ==  ShiftReduceParser.OK:
            return action
        else:
            return value
    except TypeError:
        return value

def table_to_dataframe(table):
    d = {}
    for (state, symbol), value in table.items():
        value = encode_value(value)
        try:
            d[state][symbol] = value
        except KeyError:
            d[state] = { symbol: value }

    return DataFrame.from_dict(d, orient='index', dtype=str)

def test_answer():

    G = Grammar()
    E = G.add_non_terminal('E', True)
    T,F = G.add_non_terminals('T F')
    plus, minus, star, div, opar, cpar, num = G.add_terminals('+ - * / ( ) int')

    E %= E + plus + T | T # | E + minus + T 
    T %= T + star + F | F # | T + div + F
    F %= num | opar + E + cpar

    parser = SLR1Parser(G)
    

    assert True == False
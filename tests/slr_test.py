from core import Grammar, Sentence, Production
from core.compiler.parser.slr1 import SLR1Parser
from core.compiler.parser.parser_shift_reduce import ShiftReduceParser

def test_slr():

    G = Grammar()
    E = G.add_non_terminal('E', True)
    T,F = G.add_non_terminals('T F')
    plus, minus, star, div, opar, cpar, num = G.add_terminals('+ - * / ( ) int')

    E %= E + plus + T | T # | E + minus + T
    T %= T + star + F | F # | T + div + F
    F %= num | opar + E + cpar

    parser = SLR1Parser(G)
    parser = SLR1Parser(G)
    derivation = parser([num, plus, num, star, num, G.eof])
    assert str(derivation) == '[F -> int, T -> F, E -> T, F -> int, T -> F, F -> int, T -> T * F, E -> E + T]'

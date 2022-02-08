
from core.compiler.parser.parser_lr import LR1Parser
from core import Grammar
from core.compiler.bots_grammar import BotGrammar

from pandas import DataFrame
from core.compiler.parser.parser_shift_reduce import ShiftReduceParser

G = Grammar()
E = G.add_non_terminal('E', True)
A = G.add_non_terminal('A')
equal, plus, num = G.add_terminals('= + int')

E %=  A + equal + A | num
A %= num + plus + A | num


parser = LR1Parser(G)

derivation = parser([num, plus, num, equal, num, plus, num, G.eof])

assert str(derivation) == '[A -> int, A -> int + A, A -> int, A -> int + A, E -> A = A]'

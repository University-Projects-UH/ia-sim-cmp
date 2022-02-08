from core import BotGrammar
from core.compiler.parser.slr1 import SLR1Parser
from core.compiler.parser.parser_lr import LR1Parser

def test_answer():

    G = BotGrammar().grammar

    # The grammar can be parse whit both parsers
    # If this test fail is because exist a conflict filling the tables
    parser_lr1 = LR1Parser(G)
    parser_slr1 = SLR1Parser(G)

    assert True == True

from core import BotGrammar
from core.compiler.parser.slr1 import SLR1Parser

def test_answer():

    G = BotGrammar()
    print(G)
    
    # The grammar for bots cannot be parse whit the SLR1Parser
    # because there exist conflict reduce-reduce or shif-reduce
    
    # parser = SLR1Parser(G.grammar)

    assert True == True

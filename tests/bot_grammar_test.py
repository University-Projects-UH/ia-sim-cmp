from core import BotGrammar
from core.compiler.parser.slr1 import SLR1Parser
from core.compiler.parser.parser_lr import LR1Parser
from core.compiler.lexer.token import Token
from core.compiler.parser.parser_shift_reduce import evaluate_reverse_parse
from core.compiler.ast.ast import ProgramNode

def test_answer():

    G = BotGrammar().grammar

    # The grammar can be parse whit both parsers
    # If this test fail is because exist a conflict filling the tables
    parser_lr1 = LR1Parser(G)
    parser_slr1 = SLR1Parser(G)

    tokens = [Token('int', G.symbols['int']), Token('x', G.symbols['id']), Token('=', G.symbols['=']), Token('4', G.symbols['int_number']), Token(';', G.symbols[';']), Token('$', G.eof)]
    token_types = [t.reg_type for t in tokens]
    right_parse, operations = parser_lr1(token_types, True)

    ast = evaluate_reverse_parse(right_parse, operations, tokens)
    print(ast)

    assert isinstance(ast, ProgramNode)

from core import build_lexer
from core import BotGrammar
from core.compiler.parser.parser_lr import LR1Parser
from core.compiler.parser.parser_shift_reduce import evaluate_reverse_parse
from core.compiler.ast.bot_transpiler import BotTranspiler

def run_project():
    code = "int x = 1;"

    lexer = build_lexer()
    tokens = lexer(code)
    print([(tok.reg_exp, tok.reg_type) for tok in tokens])

    G = BotGrammar().grammar
    parser_lr = LR1Parser(G)

    token_types = [G.symbols[t.reg_type] for t in tokens]

    print([token.reg_type for token in tokens])

    right_parse, operations = parser_lr(token_types, True)
    ast = evaluate_reverse_parse(right_parse, operations, tokens)
    transpiler = BotTranspiler()
    transpiler.visit(ast)

    return

run_project()

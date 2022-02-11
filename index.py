from core import build_lexer
from core import BotGrammar
from core.compiler.parser.parser_lr import LR1Parser
from core.compiler.parser.parser_shift_reduce import evaluate_reverse_parse
from core.compiler.ast.bot_transpiler import BotTranspiler

def run_project():
    code = "int x = 1;"

    lexer = build_lexer()
    tokens = lexer(code)
    print([(tok.reg_type, tok.reg_exp) for tok in tokens])

    G = BotGrammar().grammar
    parser_lr = LR1Parser(G)

    right_parse, operations = parser_lr(tokens, True)
    ast = evaluate_reverse_parse(right_parse, operations, tokens)
    transpiler = BotTranspiler()
    transpiler.visit(ast)

    return

run_project()

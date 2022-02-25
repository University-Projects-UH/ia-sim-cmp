from core import build_lexer
from core import BotGrammar
from core.compiler.parser.parser_lr import LR1Parser
from core.compiler.parser.parser_shift_reduce import evaluate_reverse_parse
from core.compiler.ast.bot_transpiler import BotTranspiler
from core.compiler.ast.semantic_check import SemanticChecker
from os import walk

import sys
import string

def get_assets_availables():
    source_path = "csv/assets_data"
    text_arr = []
    for _, _, filenames in walk(source_path):
        text_arr.extend(filenames)

    return text_arr


def run_project():
    try:
        file_name = sys.argv[1]
    except:
        print("Es necesario que se ponga \"python index.py name_codigo_a_compilar\"")
        print("Ejemplo: \"python index.py code.botlang\"")
        sys.exit()

    assets_availables = get_assets_availables()

    code = open(file_name,'r').read()

    # print(code)

    lexer = build_lexer()
    tokens = lexer(code)
    # print([(tok.reg_exp, tok.reg_type) for tok in tokens])

    G = BotGrammar().grammar
    parser_lr = LR1Parser(G)

    token_types = [G.symbols[t.reg_type] for t in tokens]

    # print([token.reg_type for token in tokens])

    right_parse, operations = parser_lr(token_types, True)
    ast = evaluate_reverse_parse(right_parse, operations, tokens)

    semantic = SemanticChecker(assets_availables)
    errors = semantic.visit(ast)
    if(len(errors) > 0):
        print("Errores encontrados: ")
        print(errors)
        return

    transpiler = BotTranspiler()
    transpiler.visit(ast)

    exec(open("code_transpiled.py").read())

run_project()

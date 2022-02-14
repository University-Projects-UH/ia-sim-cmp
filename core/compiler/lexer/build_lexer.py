from .lexer import Lexer
import functools

digit = '|'.join(str(n) for n in range(0, 10))
lower = '|'.join(chr(n) for n in range(ord('a'), ord('z') + 1))
mayus = '|'.join(chr(n) for n in range(ord('A'), ord('Z') + 1))
letter = lower + '|' + mayus

INTEGER = '{0}|{1|2|3|4|5|6|7|8|9}{' + digit + '}^'
FLOAT = '{0}{.}{' + digit + '}{' + digit + '}^|{1|2|3|4|5|6|7|8|9}{' + digit + '}^{.}{' + digit + '}{' + digit + '}^'
DATE = '{' + digit + '}{' + digit + '}{' + digit + '}{' + digit + '}' + \
    '{-}{0|1}{' + digit + '}{-}{0|1|2|3}{' + digit + '}'

KEYWORDS = [
    'grid_bot',
    'rebalance_bot',
    'smart_bot',
    'asset',
    'assets',
    'int',
    'float',
    'bool',
    'date',
    'string',
    'if',
    'then',
    'else',
    'end',
    'print',
    'True',
    'False',
    'portfolio',
    'portfolio_max_sharpe_ratio',
    'portfolio_min_sd',
    'array'
]
SYMBOLS = [
    '+', '-', '/', '*', '(', ')', '!', ',',
    '<', '>', '[', ']', '<=', '=>', '=', '==', ';'
]
symbols = ['+', " ", '-', '/', '*', '(', ')', '!', '<', '>', '[', ']', ';', '=', "."]
symbols = digit + "|" + letter + "|" + "|".join(symbols)

SPACE = '{ |\n|\t|\f|\r|\v}{ |\n|\t|\f|\r|\v}^'
ID = '{' + letter + '}{' + INTEGER + "|" + letter + '}^'
STRING = '{"}{' + symbols + '}^{"}'

def build_lexer():
    table = [(INTEGER, 'int_number')]
    table.append((FLOAT, 'float_number'))
    table.append((DATE, 'date_type'))
    table.append((STRING, 'string_exp'))
    for key in KEYWORDS:
        table.append((key, key))
    for regex in SYMBOLS:
        table.append((regex, regex))
    table.append((SPACE, 'space'))
    table.append((ID, 'id'))

    return Lexer(table, '$')

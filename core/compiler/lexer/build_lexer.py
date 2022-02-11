from .lexer import Lexer

digit = '|'.join(str(n) for n in range(0, 10))
lower = '|'.join(chr(n) for n in range(ord('a'), ord('z') + 1))
mayus = '|'.join(chr(n) for n in range(ord('A'), ord('Z') + 1))
letter = lower + '|' + mayus
symbol = digit + '|' + letter + '|' + '|'.join({
    '_', '<', '>', '=', '+', '-', '/', '!', ';', ',', ' ', '*', '(', ')', '[', ']', '\''
})

INTEGER = '{0}|{1|2|3|4|5|6|7|8|9}{' + digit + '}^'
FLOAT = '{0}{.}{' + digit + '}{' + digit + '}^|{1|2|3|4|5|6|7|8|9}{' + digit + '}^{.}{' + digit + '}{' + digit + '}^'
KEYWORDS = {
    'grid_bot': '{g}{r}{i}{d}{_}{b}{o}{t}',
    'rebalance_bot': '{r}{e}{b}{a}{l}{a}{n}{c}{e}{_}{b}{o}{t}',
    'smart_bot': '{s}{m}{a}{r}{t}{_}{b}{o}{t}',
    'asset': '{a}{s}{s}{e}{t}',
    'int': '{i}{n}{t}',
    'float': '{f}{l}{o}{a}{t}',
    'bool': '{b}{o}{o}{l}',
    'string': '{s}{t}{r}{i}{n}{g}',
    'if': '{i}{f}',
    'then': '{t}{h}{e}{n}',
    'else': '{e}{l}{s}{e}',
    'end': '{e}{n}{d}',
    'print': '{p}{r}{i}{n}{t}',
    'true': '{t}{r}{u}{e}',
    'false': '{f}{a}{l}{s}{e}'
}
SYMBOLS = {
    '+', '-', '/', '*', '(', ')', '!',
    '<', '<=', '=>', '=', '==', ';'
}
SPACE = '{ |\n|\t|\f|\r|\v}{ |\n|\t|\f|\r|\v}^'

def build_lexer():
    table = [('integer', INTEGER)]
    table.append(('float_n', FLOAT))
    for key in KEYWORDS:
        table.append((key, KEYWORDS[key]))
    for regex in SYMBOLS:
        table.append((regex, regex))
    table.append(('space', SPACE))

    return Lexer(table, '$')

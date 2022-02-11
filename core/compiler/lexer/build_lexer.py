from .lexer import Lexer

digit = '|'.join(str(n) for n in range(0, 10))
lower = '|'.join(chr(n) for n in range(ord('a'), ord('z') + 1))
mayus = '|'.join(chr(n) for n in range(ord('A'), ord('Z') + 1))
letter = lower + '|' + mayus

INTEGER = '{0}|{1|2|3|4|5|6|7|8|9}{' + digit + '}^'
FLOAT = '{0}{.}{' + digit + '}{' + digit + '}^|{1|2|3|4|5|6|7|8|9}{' + digit + '}^{.}{' + digit + '}{' + digit + '}^'
KEYWORDS = {
    'grid_bot': '{g}{r}{i}{d}{_}{b}{o}{t}',
    'rebalance_bot': '{r}{e}{b}{a}{l}{a}{n}{c}{e}{_}{b}{o}{t}',
    'smart_bot': '{s}{m}{a}{r}{t}{_}{b}{o}{t}',
    'asset': '{a}{s}{s}{e}{t}',
    'assets': '{a}{s}{s}{e}{t}{s}',
    'int': '{i}{n}{t}',
    'float': '{f}{l}{o}{a}{t}',
    'bool': '{b}{o}{o}{l}',
    'string': '{s}{t}{r}{i}{n}{g}',
    'if': '{i}{f}',
    'then': '{t}{h}{e}{n}',
    'else': '{e}{l}{s}{e}',
    'end': '{e}{n}{d}',
    'print': '{p}{r}{i}{n}{t}',
    'True': '{T}{r}{u}{e}',
    'False': '{F}{a}{l}{s}{e}',
    'portfolio': '{p}{o}{r}{t}{f}{o}{l}{i}{o}',
    'portfolio_max_sharpe_ratio': '{p}{o}{r}{t}{f}{o}{l}{i}{o}{_}{m}{a}{x}{_}{s}{h}{a}{r}{p}{e}{_}{r}{a}{t}{i}{o}',
    'portfolio_min_sd': '{p}{o}{r}{t}{f}{o}{l}{i}{o}{_}{m}{i}{n}{_}{s}{d}'
}
SYMBOLS = {
    '+', '-', '/', '*', '(', ')', '!',
    '<', '>', '[', ']', '<=', '=>', '=', '==', ';'
}
SPACE = '{ |\n|\t|\f|\r|\v}{ |\n|\t|\f|\r|\v}^'
ID = '{' + letter + '}{' + INTEGER + "|" + letter + '}^'

def build_lexer():
    table = [(INTEGER, 'int_number')]
    table.append((FLOAT, 'float_number'))
    for key in KEYWORDS:
        table.append((KEYWORDS[key], key))
    for regex in SYMBOLS:
        table.append((regex, regex))
    table.append((SPACE, 'space'))
    table.append((ID, 'id'))

    return Lexer(table, '$')

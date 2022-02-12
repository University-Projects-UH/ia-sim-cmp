from core import Lexer, Regex
from core import build_lexer

def test_date_type():
    lexer = build_lexer()
    tokens = lexer("date alg = 2022-02-12")
    assert [token.reg_type for token in tokens] == ['date', 'id', '=', 'date_type', '$']

def test_lexer():
    nonzero_digits = '|'.join(str(n) for n in range(1,10))
    letters = '|'.join(chr(n) for n in range(ord('a'),ord('z')+1))

    print('Non-zero digits:', nonzero_digits)
    print('Letters:', letters)

    lexer = Lexer([
        ('{' + nonzero_digits + '}{0|' + nonzero_digits + '}^', 'num'),
        ('for' , 'for'),
        ('foreach' , 'foreach'),
        ('  ^', 'space'),
        ('{' + letters + '}{' + letters + '|0|' + nonzero_digits + '}^', 'id')
    ], 'eof')

    tokens = lexer("5465")
    assert [t.reg_type for t in tokens] == ['num', 'eof']

    text = '5465 for 45foreach fore'
    print(f'\n>>> Tokenizando: "{text}"')
    tokens = lexer(text)
    print(tokens)
    assert [t.reg_type for t in tokens] == ['num', 'for', 'num', 'foreach', 'id', 'eof']
    assert [t.reg_exp for t in tokens] == ['5465', 'for', '45', 'foreach', 'fore', '$']

    text = '4forense forforeach for4foreach foreach 4for'
    print(f'\n>>> Tokenizando: "{text}"')
    tokens = lexer(text)
    print(tokens)
    assert [t.reg_type for t in tokens] == ['num', 'id', 'id', 'id', 'foreach', 'num', 'for', 'eof']
    assert [t.reg_exp for t in tokens] == ['4', 'forense', 'forforeach', 'for4foreach', 'foreach', '4', 'for', '$']

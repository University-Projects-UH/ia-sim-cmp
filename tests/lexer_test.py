from core import Asset, GridBot
from datetime import datetime
"""
netflix = Asset("NETFLIX", "./karel/asset/assets_data/NFLX.csv")
btc = Asset("BTC", "./karel/asset/assets_data/BTC-USD.csv")
ETH = Asset("ETH", "./karel/asset/assets_data/ETH-USD.csv")
ADA = Asset("ADA", "./karel/asset/assets_data/ADA-USD.csv")
MSFT = Asset("MSFT", "./karel/asset/assets_data/MSFT.csv")

assetAB = build_AB_assets_combination(netflix, btc)
vv = GridBot("Karel", 0, 1.2, 1000, 20, 0.001, 1, assetAB)
vv.insert_operation("2:34", 41, "buy", 10, "BTC/USD")
vv.insert_operation("2:50", 10, "sell", 11, "BTC/USD")
vv.insert_operation("10:50", 41, "sell", 8, "BTC/USD")
#vv.print_bot_info()
#vv.start_bot()
smart_bot = SmartBot("Smart Karel", None, None, 1000, btc)
smart_bot.start_bot()

#rebalance_bot = RebalanceBot("Karelito", -1000, 1000, 1000, [netflix, btc, ETH, ADA, MSFT])
#datea = datetime.strptime("2060-05-10", "%Y-%m-%d")

#rebalance_bot.start_bot()

grid_bot = GridBot("Karelito", -1, 1000000, 1000, 100, 5000, 10000, [btc])

grid_bot.start_bot()
"""

from core import Lexer
nonzero_digits = '|'.join(str(n) for n in range(1,10))
letters = '|'.join(chr(n) for n in range(ord('a'),ord('z')+1))

print('Non-zero digits:', nonzero_digits)
print('Letters:', letters)

from core import Regex
reg = Regex(f'[{nonzero_digits}][0|{nonzero_digits}]^')

exit(0)

lexer = Lexer([
    ('num', f'({nonzero_digits})(0|{nonzero_digits})*'),
    ('for' , 'for'),
    ('foreach' , 'foreach'),
    ('space', '  *'),
    ('id', f'({letters})({letters}|0|{nonzero_digits})*')
], 'eof')

text = '5465 for 45foreach fore'
print(f'\n>>> Tokenizando: "{text}"')
tokens = lexer(text)
print(tokens)
assert [t.token_type for t in tokens] == ['num', 'space', 'for', 'space', 'num', 'foreach', 'space', 'id', 'eof']
assert [t.lex for t in tokens] == ['5465', ' ', 'for', ' ', '45', 'foreach', ' ', 'fore', '$']

text = '4forense forforeach for4foreach foreach 4for'
print(f'\n>>> Tokenizando: "{text}"')
tokens = lexer(text)
print(tokens)
assert [t.token_type for t in tokens] == ['num', 'id', 'space', 'id', 'space', 'id', 'space', 'foreach', 'space', 'num', 'for', 'eof']
assert [t.lex for t in tokens] == ['4', 'forense', ' ', 'forforeach', ' ', 'for4foreach', ' ', 'foreach', ' ', '4', 'for', '$']

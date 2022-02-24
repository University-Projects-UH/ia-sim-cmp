from core import Asset
from core import GridBot
from datetime import datetime
from core import grid_bot_optimization

def test_answer():

    # "btc-usd_2021-01-01_2021-03-31.csv"

    # a1 = Asset("BTC-USD.csv")

    a1 = Asset("btc-usd_2021-01-01_2021-03-31.csv")

    assets = [a1]
    
    best = grid_bot_optimization(assets, 100, 10, 10)

    assert isinstance(best, GridBot)

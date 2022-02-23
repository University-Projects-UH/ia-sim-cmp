from core import Asset
from datetime import datetime
from core import grid_bot_optimization

def test_answer():

    a1 = Asset("BTC-USD.csv")

    assets = [a1]
    
    best = grid_bot_optimization(assets)

    assert True == True

import pandas as pd
from core import Asset, GridBot

def test_answer():
    data = {
        'Date': ["2022-01-01", "2022-01-02", "2022-01-03", "2022-01-04", "2022-01-05", "2022-01-06", \
                 "2022-01-07"],
        'Close': [1500, 1300, 1100, 900, 1400, 850, 1900]
    }

    my_asset = Asset("Testercoin", pd.DataFrame(data))

    grid_bot = GridBot("Calamardo", 800, 2100, 100, 5, 1000, 2000, [my_asset])
    assert grid_bot.investment_per_grid == 20
    assert grid_bot.grid_len == 200

    grid_bot.start_bot()
    history_array = [["buy", 1500], ["buy", 1500], ["buy", 1400], ["buy", 1200], ["buy", 1000], \
                     ["sell", 1200], ["sell", 1400], ["buy", 1200], ["buy", 1000], ["sell", 1200], \
                     ["sell", 1400], ["sell", 1600], ["sell", 1800]]

    grid_bot.print_operation_history()
    assert len(grid_bot.operation_history) == len(history_array)
    for i in range(len(grid_bot.operation_history)):
        order = grid_bot.operation_history[i]
        expected_order = history_array[i]
        volumen, price, order_type = order.volumen, order.price, order.order_type
        assert(price == expected_order[1])
        assert(order_type == expected_order[0])
        if(order_type == "buy"):
            assert price * volumen == 20

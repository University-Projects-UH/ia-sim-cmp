import pandas as pd
from core import Asset, SmartBot

def test_answer():
    data = {
        'Date': ["2022-01-01", "2022-01-02", "2022-01-03", "2022-01-04", "2022-01-05", "2022-01-06", \
                 "2022-01-07","2022-01-08","2022-01-09"],
        'Close': [1500, 1300, 1100, 900, 1400, 850, 1900, 2500, 3000],
        'Open' : [1500, 1500, 1300, 1100, 900, 1400, 850, 1900, 2500]
    }

    my_asset = Asset("Testercoin", None, pd.DataFrame(data))

    smart_bot = SmartBot("TesterBot", 800, 2700, 100, [my_asset])

    assert len(smart_bot.assets_array) == 1

    smart_bot.start_bot()

    # history_array = [["buy", 1500], ["buy", 1500], ["buy", 1400], ["buy", 1200], ["buy", 1000], \
    #                  ["sell", 1200], ["sell", 1400], ["buy", 1200], ["buy", 1000], ["sell", 1200], \
    #                  ["sell", 1400], ["sell", 1600], ["sell", 1800]]

    smart_bot.print_operation_history()
    assert len(smart_bot.operation_history) == 6

    open_orders = 0
    for i in range(len(smart_bot.operation_history)):
        order = smart_bot.operation_history[i]
        volumen, price, order_type = order.volumen, order.price, order.order_type


        if(order_type == "buy"):
            open_orders += 1
            assert round(price * volumen) == smart_bot.investment / smart_bot.max_open_orders
        else:
            open_orders -= 1
        
        assert open_orders <= smart_bot.max_open_orders
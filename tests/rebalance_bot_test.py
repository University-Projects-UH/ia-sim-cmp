import pandas as pd
from core import Asset, RebalanceBot
EPS = 0.000001

def test_answer():
    data = {
        'Date': ["2022-01-01", "2022-01-02", "2022-01-03", "2022-01-04", "2022-01-05"],
        'Close': [1000, 1500, 1500, 1500, 1500]
    }
    testercoin = Asset("Testercoin", None, pd.DataFrame(data))

    data = {
        'Date': ["2022-01-01", "2022-01-02", "2022-01-03", "2022-01-04", "2022-01-05"],
        'Close': [1000, 1000, 1000, 1000, 660]
    }
    esponjabot = Asset("BobEsponja", None, pd.DataFrame(data))

    rebalance_bot = RebalanceBot("Rebalance", -100, 100, 2000, [testercoin, esponjabot], 0.1)

    rebalance_bot.start_bot()
    history_array = [["buy", 1000, "Testercoin", 1.0], ["buy", 1000, "BobEsponja", 1.0], \
                     ["sell", 1500, "Testercoin", 0.1666666667], ["buy", 1000, "BobEsponja", 0.25], \
                     ["sell", 1500, "Testercoin", 0.141666665], ["buy", 660, "BobEsponja", 0.321969696969]]

    rebalance_bot.print_operation_history()
    assert len(rebalance_bot.operation_history) == len(history_array)
    for i in range(len(rebalance_bot.operation_history)):
        order = rebalance_bot.operation_history[i]
        expected_order = history_array[i]
        volumen, price, order_type, name = order.volumen, order.price, order.order_type, order.name
        assert(price == expected_order[1])
        assert(order_type == expected_order[0])
        assert(name == expected_order[2])
        assert(abs(volumen - expected_order[3]) < EPS)

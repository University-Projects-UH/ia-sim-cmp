from bot import Bot

class GridBot(Bot):
    def __init__(self, name, take_profit, stop_loss, investment, grids, limit_high, limit_low, asset_pair, ):
        super().__init__(name, take_profit, stop_loss, investment)
        self.grids = grids
        self.limit_low = limit_low
        self.limit_high = limit_high
        self.asset_pair = asset_pair

    def print_bot_info(self):
        super().print_bot_info()
        print("Pair: " + "/".join(self.asset_pair))
        print("Limit low: " + str(self.limit_low))
        print("Limit high: " + str(self.limit_high))

        self.print_operation_history()

vv = GridBot("Karel", 100, 10, 1000, 10, 100, 5, ["BTC", "USD"])
vv.insert_operation("2:34", 41, "buy", 10, "BTC/USD")
vv.insert_operation("2:50", 10, "sell", 11, "BTC/USD")
vv.insert_operation("10:50", 41, "sell", 8, "BTC/USD")
vv.print_bot_info()

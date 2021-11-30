from .bot import Bot

class Order:
    def __init__(self, price, volumen):
        self.price = price
        self.volumen = volumen

class SmartBot(Bot):
    def __init__(self, name, stop_loss, take_profit, investment, assetAB, stacking = False):
        super().__init__(name, stop_loss, take_profit, investment)
        self.assetAB = assetAB
        self.opened_orders = []
        self.count_rows = len(assetAB.asset_data.index)

    def print_bot_info(self):
        super().print_bot_info()
        print("Pair: " + self.assetAB.name)
        super().print_operation_history()

    def get_simple_MA(self, days = 20, position = None):
        if position is None:
            position = len(self.asset_data.index) - 1
        count = days
        price_sum = 0
        close_prices = self.asset_data['Close']
        while count > 0 and position > 0:
            price_sum += close_prices[position]
            count -= 1
            position -= 1

        return price_sum / days

    def start_bot(self, position = 0):
        while position < self.count_rows:
           day_prices = self.assetAB.get_day_prices(position)
           position += 1
